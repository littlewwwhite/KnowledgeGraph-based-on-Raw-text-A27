"""
State management for Knowledge Graph Builder.

Provides a type-safe, serializable state model to replace __dict__ serialization.
"""
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional
import json


@dataclass
class KGState:
    """
    Serializable state for KnowledgeGraphBuilder.

    This replaces the unsafe __dict__ serialization with a well-defined schema.

    Attributes:
        version: Current iteration version number.
        data_dir: Directory for storing generated data.
        kg_paths: List of knowledge graph file paths from each iteration.
        model_name_or_path: BERT model name or path.
        gpu: GPU ID for training.
        text_path: Path to raw text file.
        base_kg_path: Path to base knowledge graph.
        refined_kg_path: Path to refined knowledge graph.
        filtered_kg_path: Path to filtered knowledge graph.
    """
    version: int = 0
    data_dir: str = ""
    kg_paths: List[str] = field(default_factory=list)
    model_name_or_path: str = "bert-base-chinese"
    gpu: str = "0"
    text_path: str = ""
    base_kg_path: str = ""
    refined_kg_path: str = ""
    filtered_kg_path: str = ""

    def to_dict(self) -> dict:
        """Convert state to dictionary."""
        return asdict(self)

    def save(self, file_path: str) -> None:
        """
        Save state to a JSON file.

        Args:
            file_path: Output file path.
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    @classmethod
    def from_dict(cls, data: dict) -> "KGState":
        """
        Create state from a dictionary.

        Args:
            data: Dictionary with state fields.

        Returns:
            KGState instance.
        """
        return cls(**data)

    @classmethod
    def load(cls, file_path: str) -> "KGState":
        """
        Load state from a JSON file.

        Args:
            file_path: Input file path.

        Returns:
            Loaded KGState instance.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_builder(cls, builder: "KnowledgeGraphBuilder") -> "KGState":
        """
        Create state from KnowledgeGraphBuilder instance.

        Args:
            builder: KnowledgeGraphBuilder instance.

        Returns:
            KGState with builder's current state.
        """
        return cls(
            version=builder.version,
            data_dir=builder.data_dir,
            kg_paths=builder.kg_paths.copy(),
            model_name_or_path=builder.model_name_or_path,
            gpu=builder.gpu,
            text_path=builder.text_path,
            base_kg_path=builder.base_kg_path,
            refined_kg_path=builder.refined_kg_path,
            filtered_kg_path=builder.filtered_kg_path,
        )

    def apply_to_builder(self, builder: "KnowledgeGraphBuilder") -> None:
        """
        Apply state to a KnowledgeGraphBuilder instance.

        Args:
            builder: KnowledgeGraphBuilder instance to update.
        """
        builder.version = self.version
        builder.data_dir = self.data_dir
        builder.kg_paths = self.kg_paths.copy()
        builder.model_name_or_path = self.model_name_or_path
        builder.gpu = self.gpu
        builder.text_path = self.text_path
        builder.base_kg_path = self.base_kg_path
        builder.refined_kg_path = self.refined_kg_path
        builder.filtered_kg_path = self.filtered_kg_path
