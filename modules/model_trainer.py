"""
Model Trainer module for SPN4RE.

Handles data splitting, model training, and result processing for relation extraction.
"""
import os
import random
import subprocess
from typing import Any, Dict, List, Union

from config.settings import settings
from prepare.filter import auto_filter
from prepare.utils import refine_knowledge_graph
from modules.utils.io import read_jsonl, write_jsonl, read_json
from modules.utils.logger import logger, green, purple


class ModelTrainer:
    """
    SPN4RE model trainer for knowledge graph expansion.

    Handles the complete training pipeline:
    1. Data splitting (train/valid/test)
    2. Model training via subprocess
    3. Prediction alignment with original data
    4. Knowledge graph refinement and extension

    Attributes:
        gpu: GPU device identifier for training.
        data_path: Path to source knowledge graph data.
        generated_data_directory: Output directory for generated files.
        model_name_or_path: BERT model path for SPN4RE.
        train_file: Path to training data split.
        valid_file: Path to validation data split.
        test_file: Path to test data split.
        prediction: Path to model prediction output.
        final_knowledge_graph: Path to extended knowledge graph.
    """

    def __init__(
        self,
        data_path: str,
        output_dir: str,
        model_name_or_path: str,
        gpu: str
    ) -> None:
        """
        Initialize ModelTrainer with data paths and configuration.

        Args:
            data_path: Path to unsplit knowledge graph data (JSONL format).
            output_dir: Directory for saving all generated files.
            model_name_or_path: BERT model name or path for SPN4RE.
            gpu: GPU device ID (e.g., "0" or "0,1").
        """
        self.gpu: str = gpu
        self.data_path: str = data_path
        self.generated_data_directory: str = output_dir + os.sep  # fix SPN dir bug
        self.model_name_or_path: str = model_name_or_path

        os.makedirs(output_dir, exist_ok=True)

        # Data split paths
        self.train_file: str = os.path.join(output_dir, "train.json")
        self.valid_file: str = os.path.join(output_dir, "valid.json")
        self.test_file: str = os.path.join(output_dir, "test.json")

        # Output paths
        self.prediction: str = os.path.join(output_dir, "prediction.json")
        self.test_result_format: str = os.path.join(output_dir, "test_result_format.json")
        self.test_result_refine: str = os.path.join(output_dir, "test_result_refine.json")
        self.data_instance_path: str = os.path.join(output_dir, "alphabet.json")
        self.final_knowledge_graph: str = os.path.join(output_dir, "knowledge_graph.json")

        self.split_data()
        self.params: str = self._generate_running_cmd()

    def _generate_running_cmd(self) -> str:
        """
        Generate SPN4RE training command string.

        Returns:
            Complete command string with all training parameters.
        """
        params = "python SPN4RE/main.py"
        params += f" --bert_directory {self.model_name_or_path}"
        params += f" --max_epoch {settings.MAX_EPOCH}"
        params += f" --max_span_length {settings.MAX_SPAN_LENGTH}"
        params += f" --num_generated_triples {settings.NUM_GENERATED_TRIPLES}"
        params += " --max_grad_norm 2.5"
        params += " --na_rel_coef 0.25"
        params += f" --train_file {self.train_file}"
        params += f" --valid_file {self.valid_file}"
        params += f" --test_file {self.test_file}"
        params += f" --visible_gpu {self.gpu}"
        params += f" --generated_data_directory {self.generated_data_directory}"
        params += f" --generated_param_directory {self.generated_data_directory}"
        return params

    def _save_data(
        self,
        data: Union[List[Dict[str, Any]], List[str]],
        trg_path: str
    ) -> None:
        """
        Save data to file based on extension.

        Args:
            data: List of items to save.
            trg_path: Target file path (.json for JSONL, .txt for text).

        Raises:
            ValueError: If file format is not supported.
        """
        if trg_path.endswith(".json"):
            write_jsonl(data, trg_path)
        elif trg_path.endswith(".txt"):
            with open(trg_path, 'w', encoding='utf-8') as f:
                for line in data:
                    f.write(str(line) + "\n")
        else:
            raise ValueError(f"Unsupported file format: {trg_path}")
        logger.info(f"Data saved to {trg_path}")

    def split_data(self) -> None:
        """
        Split knowledge graph data into train/valid/test sets.

        Uses ratios from settings (TRAIN_RATIO, VALID_RATIO).
        Remaining data goes to test set.

        Raises:
            AssertionError: If dataset is empty.
        """
        lines: List[Dict[str, Any]] = read_jsonl(self.data_path)
        lines_shuffled = random.sample(lines, len(lines))

        assert lines_shuffled, "Dataset is empty"

        train_end = int(len(lines_shuffled) * settings.TRAIN_RATIO)
        valid_end = int(len(lines_shuffled) * (settings.TRAIN_RATIO + settings.VALID_RATIO))

        train_lines = lines_shuffled[:train_end]
        valid_lines = lines_shuffled[train_end:valid_end]
        test_lines = lines_shuffled[valid_end:]

        self._save_data(train_lines, self.train_file)
        self._save_data(valid_lines, self.valid_file)
        self._save_data(test_lines, self.test_file)

        logger.info(f"Data split: train={len(train_lines)}, valid={len(valid_lines)}, test={len(test_lines)}")

    def train_and_test(self) -> None:
        """
        Train and test the SPN4RE model.

        Runs SPN4RE training via subprocess. Prediction results
        are saved to self.prediction file.

        Raises:
            RuntimeError: If training process fails.
        """
        logger.info(f"{green('Running:')} $ {self.params}")

        log_file = os.path.join(self.generated_data_directory, "running_log.log")
        logger.info(f"{purple('Log file:')} {log_file}")

        with open(log_file, 'w', encoding='utf-8') as log_f:
            result = subprocess.run(
                self.params.split(),
                stdout=log_f,
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            )

        if result.returncode != 0:
            raise RuntimeError(
                f"Training failed with exit code {result.returncode}. "
                f"Check log file: {log_file}"
            )

        logger.success("Training completed successfully")

    def relation_align(self) -> None:
        """
        Align model predictions with test data.

        Steps:
        1. Load test set and predictions
        2. Convert predictions to SPN format
        3. Remove duplicate relations from original data
        4. Filter invalid relations
        5. Save formatted results
        """
        logger.info("Aligning predictions with test data")

        # Load test set and predictions
        test_lines: List[Dict[str, Any]] = read_jsonl(self.test_file)
        prediction: Dict[str, List[Any]] = read_json(self.prediction)

        # Convert predictions to SPN training style
        test_pred_lines: Dict[str, List[List[int]]] = {}
        for key, values in prediction.items():
            pred_relation: List[List[int]] = []
            for value in values:
                pred_rel = value[0]
                head_start_index = value[2]
                head_end_index = value[3]
                tail_start_index = value[6]
                tail_end_index = value[7]
                pred_relation.append([
                    pred_rel,
                    head_start_index,
                    head_end_index,
                    tail_start_index,
                    tail_end_index
                ])
            test_pred_lines[key] = pred_relation

        assert len(test_lines) == len(prediction), \
            f"Mismatch: {len(test_lines)} test lines vs {len(prediction)} predictions"

        # Load relation id to label mapping
        id2rel: List[str] = read_json(self.data_instance_path)["instances"]

        # Align predictions with test set
        pred_lines: List[Dict[str, Any]] = []
        for test_line, pred in zip(test_lines, list(test_pred_lines.values())):
            triples: List[Dict[str, str]] = []

            for triple_pred in pred:
                assert triple_pred[1] <= triple_pred[2] and triple_pred[3] <= triple_pred[4], \
                    "Invalid prediction triple indices"

                triple: Dict[str, str] = {
                    "em1Text": test_line["sentText"][triple_pred[1]:triple_pred[2] + 1],
                    "em2Text": test_line["sentText"][triple_pred[3]:triple_pred[4] + 1],
                    "label": id2rel[triple_pred[0]]
                }

                # Deduplicate and filter empty entities
                if (triple not in triples and
                        len(triple["em1Text"].split()) > 0 and
                        len(triple["em2Text"].split()) > 0):
                    triples.append(triple)

            pred_lines.append({
                "id": test_line["id"],
                "relationMentions": triples,
                "sentText": test_line["sentText"]
            })

        # Remove relations that already exist in original data
        origin_lines: List[Dict[str, Any]] = read_jsonl(self.data_path)
        diff_lines: List[Dict[str, Any]] = []

        for pred_line in pred_lines:
            origin_line = origin_lines[pred_line["id"]]
            assert origin_line["id"] == pred_line["id"], "ID mismatch during alignment"

            diff_rels = [
                rel for rel in pred_line["relationMentions"]
                if rel not in origin_line["relationMentions"]
            ]

            diff_lines.append({
                "id": pred_line["id"],
                "relationMentions": diff_rels,
                "sentText": pred_line["sentText"]
            })

        # Filter invalid relations using BERT tokenizer
        diff_lines = auto_filter(diff_lines, settings.BERT_MODEL_NAME)

        self._save_data(diff_lines, self.test_result_format)
        logger.success(f"Aligned {len(diff_lines)} predictions")

    def refine_and_extend(self) -> str:
        """
        Refine predictions and merge with original knowledge graph.

        Steps:
        1. Refine test results (manual or fast mode)
        2. Merge refined results with original data
        3. Save extended knowledge graph

        Returns:
            Path to the final extended knowledge graph file.
        """
        logger.info("Refining and extending knowledge graph")

        refine_knowledge_graph(
            self.test_result_format,
            self.test_result_refine,
            fast_mode=True
        )

        # Merge with original data
        origin_lines: List[Dict[str, Any]] = read_jsonl(self.data_path)
        test_result_refine: List[Dict[str, Any]] = read_jsonl(self.test_result_refine)

        # Create lookup for faster merging
        refine_by_id: Dict[int, List[Dict[str, str]]] = {
            line["id"]: line["relationMentions"]
            for line in test_result_refine
        }

        extended_count = 0
        for origin_line in origin_lines:
            if origin_line["id"] in refine_by_id:
                new_rels = refine_by_id[origin_line["id"]]
                origin_line["relationMentions"].extend(new_rels)
                extended_count += len(new_rels)

        self._save_data(origin_lines, self.final_knowledge_graph)
        logger.success(f"Extended knowledge graph with {extended_count} new relations")

        return self.final_knowledge_graph
