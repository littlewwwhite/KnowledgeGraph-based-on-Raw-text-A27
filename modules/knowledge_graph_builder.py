"""
Knowledge Graph Builder module.

Provides iterative knowledge graph construction from raw text using UIE and SPN4RE.
"""
import os
import time
from argparse import Namespace
from typing import List, Optional

from config.settings import settings
from prepare.preprocess import process_text
from prepare.utils import refine_knowledge_graph
from prepare.process import uie_execute
from prepare.filter import auto_filter

from modules.model_trainer import ModelTrainer
from modules.utils.state import KGState
from modules.utils.io import read_jsonl, write_jsonl
from modules.utils.logger import logger, green, yellow, red, blue


class KnowledgeGraphBuilder:
    """
    Iterative knowledge graph builder.

    Constructs knowledge graphs from raw text through:
    1. UIE-based initial extraction
    2. SPN4RE model training and prediction
    3. Iterative graph expansion

    Attributes:
        data_dir: Directory for storing generated data.
        text_path: Path to raw text file.
        version: Current iteration version.
        kg_paths: List of knowledge graph paths from each iteration.
    """

    def __init__(self, args: Namespace) -> None:
        """
        Initialize KnowledgeGraphBuilder with project configuration.

        Args:
            args: Command line arguments containing project name and gpu settings.
        """
        self.data_dir: str = os.path.join(str(settings.DATA_DIR), args.project)
        self.text_path: str = str(settings.RAW_DATA_PATH)
        self.base_kg_path: str = os.path.join(self.data_dir, "base.json")
        self.refined_kg_path: str = os.path.join(self.data_dir, "base_refined.json")
        self.filtered_kg_path: str = os.path.join(self.data_dir, "base_filtered.json")

        self.model_name_or_path: str = settings.BERT_MODEL_NAME
        self.version: int = 0
        self.kg_paths: List[str] = []
        self.gpu: str = args.gpu

        os.makedirs(self.data_dir, exist_ok=True)

    def run_iteration(self) -> None:
        """
        Run one iteration of knowledge graph expansion.

        Steps:
        1. Load previous iteration results (or base KG for first iteration)
        2. Train SPN4RE model
        3. Align and extend knowledge graph
        4. Save results
        """
        logger.info(f"{green('Start Running Iteration:')} {yellow(f'v{self.version}')}")

        # Use refined_kg_path for first iteration, otherwise use last iteration's output
        cur_data_path = self.kg_paths[-1] if self.version > 0 else self.refined_kg_path
        cur_out_path = os.path.join(self.data_dir, f"iteration_v{self.version}")

        logger.info(f"{green('Current Data Path:')} {yellow(cur_data_path)}")
        logger.info(f"{green('Output Path:')} {yellow(cur_out_path)}")

        trainer = ModelTrainer(cur_data_path, cur_out_path, self.model_name_or_path, self.gpu)

        # Train if prediction doesn't exist
        if not os.path.exists(trainer.prediction):
            trainer.train_and_test()
            if not os.path.exists(trainer.prediction):
                raise RuntimeError(red("Prediction file not found! Training may have failed."))
            self.save()
        else:
            logger.warning("Prediction file already exists, skipping training.")

        trainer.relation_align()
        trainer.refine_and_extend()

        self.kg_paths.append(trainer.final_knowledge_graph)
        self.save()
        self.version += 1

    def extend_ratio(self) -> float:
        """
        Calculate the extension ratio to determine convergence.

        Returns:
            Ratio of new relations to total relations.
            Returns 1.0 if version < 2 or insufficient data.
        """
        if self.version < 2 or len(self.kg_paths) < 2:
            return 1.0

        pre_kg = self.kg_paths[-2]
        cur_kg = self.kg_paths[-1]

        pre_lines = read_jsonl(pre_kg)
        cur_lines = read_jsonl(cur_kg)

        if len(pre_lines) != len(cur_lines):
            logger.warning("Line count mismatch between iterations")
            return 0.0

        total_rel = 0
        extend_rel = 0
        for pre_line, cur_line in zip(pre_lines, cur_lines):
            pre_rels = pre_line.get('relationMentions', [])
            cur_rels = cur_line.get('relationMentions', [])

            total_rel += len(pre_rels)
            extend_rel += len(cur_rels) - len(pre_rels)

        return extend_rel / total_rel if total_rel > 0 else 0.0

    def get_base_kg_from_txt(self) -> None:
        """
        Build base knowledge graph from raw text using UIE.

        Steps:
        1. Clean and split text into sentences
        2. Extract relations using UIE
        3. Filter using BERT tokenizer
        4. Manual refinement (or fast mode copy)
        """
        logger.section("Building Base Knowledge Graph")

        # 1. Clean text and split into sentences
        logger.step(1, 4, "Processing raw text")
        texts = process_text(self.text_path, 480)
        logger.info(f"Processed {len(texts)} text segments")

        # 2. Execute UIE extraction (skip if base KG already exists)
        logger.step(2, 4, "UIE extraction")
        if not os.path.exists(self.base_kg_path):
            all_items = uie_execute(texts)
            write_jsonl(all_items, self.base_kg_path)
            logger.success(f"Extracted {len(all_items)} items to {self.base_kg_path}")
        else:
            logger.warning(f"Base KG already exists at {self.base_kg_path}, skipping UIE")

        # 3. Filter using BERT tokenizer
        logger.step(3, 4, "Filtering with BERT tokenizer")
        all_items = read_jsonl(self.base_kg_path)
        filtered_items = auto_filter(all_items, self.model_name_or_path)
        write_jsonl(filtered_items, self.filtered_kg_path)
        logger.success(f"Filtered to {len(filtered_items)} items")

        # 4. Manual refinement (with checkpoint support)
        logger.step(4, 4, "Knowledge graph refinement")
        refine_knowledge_graph(self.filtered_kg_path, self.refined_kg_path, fast_mode=True)
        logger.success("Base knowledge graph construction complete")

    def save(self, save_path: Optional[str] = None) -> None:
        """
        Save current state to a JSON file.

        Args:
            save_path: Optional custom path. If None, auto-generates timestamped path.
        """
        if save_path is None:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            history_dir = os.path.join(self.data_dir, "history")
            os.makedirs(history_dir, exist_ok=True)
            save_path = os.path.join(history_dir, f"{timestr}_iter_v{self.version}.json")

        state = KGState.from_builder(self)
        state.save(save_path)

        logger.success(f"State saved to {save_path}")
        logger.info(f"{blue(f'Current version: {self.version}')}")
        logger.info(f"Resume with: {green(f'--resume {save_path}')}")

    def load(self, load_path: str) -> None:
        """
        Load state from a JSON file.

        Args:
            load_path: Path to the state file.
        """
        state = KGState.load(load_path)
        state.apply_to_builder(self)
        logger.success(f"State loaded from {load_path}")
