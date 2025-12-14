"""
Tests for modules/utils/state.py - KGState dataclass.
"""
import json
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock

import pytest

from modules.utils.state import KGState


class TestKGStateCreation:
    """Tests for KGState creation and defaults."""

    def test_default_values(self) -> None:
        """Test that KGState has correct default values."""
        state = KGState()
        assert state.version == 0
        assert state.data_dir == ""
        assert state.kg_paths == []
        assert state.model_name_or_path == "bert-base-chinese"
        assert state.gpu == "0"
        assert state.text_path == ""
        assert state.base_kg_path == ""
        assert state.refined_kg_path == ""
        assert state.filtered_kg_path == ""

    def test_custom_values(self) -> None:
        """Test KGState with custom values."""
        state = KGState(
            version=3,
            data_dir="/path/to/data",
            kg_paths=["/path/1.json", "/path/2.json"],
            model_name_or_path="custom-bert",
            gpu="1",
            text_path="/path/to/text.txt"
        )
        assert state.version == 3
        assert state.data_dir == "/path/to/data"
        assert len(state.kg_paths) == 2
        assert state.model_name_or_path == "custom-bert"
        assert state.gpu == "1"
        assert state.text_path == "/path/to/text.txt"

    def test_kg_paths_not_shared(self) -> None:
        """Test that kg_paths default is not shared between instances."""
        state1 = KGState()
        state2 = KGState()
        state1.kg_paths.append("test.json")
        assert state2.kg_paths == []


class TestKGStateSerialization:
    """Tests for KGState save/load functionality."""

    def test_save_and_load(self, temp_dir: Path) -> None:
        """Test saving and loading state."""
        original = KGState(
            version=5,
            data_dir="/data/project",
            kg_paths=["/data/kg1.json", "/data/kg2.json"],
            model_name_or_path="bert-base-uncased"
        )

        save_path = temp_dir / "state.json"
        original.save(str(save_path))

        loaded = KGState.load(str(save_path))

        assert loaded.version == original.version
        assert loaded.data_dir == original.data_dir
        assert loaded.kg_paths == original.kg_paths
        assert loaded.model_name_or_path == original.model_name_or_path

    def test_save_creates_file(self, temp_dir: Path) -> None:
        """Test that save creates the file."""
        state = KGState(version=1)
        save_path = temp_dir / "new_state.json"

        state.save(str(save_path))

        assert save_path.exists()

    def test_load_nonexistent_file(self) -> None:
        """Test loading from nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            KGState.load("/nonexistent/state.json")

    def test_save_creates_parent_dirs(self, temp_dir: Path) -> None:
        """Test that save creates parent directories."""
        state = KGState(version=1)
        save_path = temp_dir / "nested" / "dir" / "state.json"

        state.save(str(save_path))

        assert save_path.exists()


class TestKGStateBuilderIntegration:
    """Tests for KGState integration with KnowledgeGraphBuilder."""

    def test_from_builder(self) -> None:
        """Test creating KGState from builder-like object."""
        # Mock a builder object
        mock_builder = MagicMock()
        mock_builder.version = 2
        mock_builder.data_dir = "/data/test"
        mock_builder.kg_paths = ["/kg/v1.json"]
        mock_builder.model_name_or_path = "bert-model"
        mock_builder.gpu = "0"
        mock_builder.text_path = "/text.txt"
        mock_builder.base_kg_path = "/base.json"
        mock_builder.refined_kg_path = "/refined.json"
        mock_builder.filtered_kg_path = "/filtered.json"

        state = KGState.from_builder(mock_builder)

        assert state.version == 2
        assert state.data_dir == "/data/test"
        assert state.kg_paths == ["/kg/v1.json"]
        assert state.model_name_or_path == "bert-model"

    def test_apply_to_builder(self) -> None:
        """Test applying state to builder-like object."""
        state = KGState(
            version=3,
            data_dir="/restored/data",
            kg_paths=["/kg/a.json", "/kg/b.json"],
            model_name_or_path="restored-bert",
            gpu="1",
            text_path="/restored/text.txt",
            base_kg_path="/restored/base.json",
            refined_kg_path="/restored/refined.json",
            filtered_kg_path="/restored/filtered.json"
        )

        mock_builder = MagicMock()
        state.apply_to_builder(mock_builder)

        assert mock_builder.version == 3
        assert mock_builder.data_dir == "/restored/data"
        assert mock_builder.kg_paths == ["/kg/a.json", "/kg/b.json"]
        assert mock_builder.model_name_or_path == "restored-bert"

    def test_roundtrip_via_builder(self, temp_dir: Path) -> None:
        """Test complete save/load roundtrip via builder pattern."""
        # Create initial state via builder
        mock_builder = MagicMock()
        mock_builder.version = 7
        mock_builder.data_dir = "/project/data"
        mock_builder.kg_paths = ["/v1.json", "/v2.json", "/v3.json"]
        mock_builder.model_name_or_path = "chinese-bert"
        mock_builder.gpu = "0"
        mock_builder.text_path = "/text.txt"
        mock_builder.base_kg_path = "/base.json"
        mock_builder.refined_kg_path = "/refined.json"
        mock_builder.filtered_kg_path = "/filtered.json"

        # Save from builder
        state = KGState.from_builder(mock_builder)
        save_path = temp_dir / "roundtrip.json"
        state.save(str(save_path))

        # Load and apply to new builder
        loaded_state = KGState.load(str(save_path))
        new_builder = MagicMock()
        loaded_state.apply_to_builder(new_builder)

        # Verify
        assert new_builder.version == 7
        assert len(new_builder.kg_paths) == 3


class TestKGStateToDict:
    """Tests for KGState dictionary conversion."""

    def test_to_dict(self) -> None:
        """Test converting state to dictionary."""
        state = KGState(
            version=1,
            data_dir="/test",
            kg_paths=["a.json"],
            model_name_or_path="bert"
        )

        result = state.to_dict()

        assert isinstance(result, dict)
        assert result["version"] == 1
        assert result["data_dir"] == "/test"
        assert result["kg_paths"] == ["a.json"]
        assert result["model_name_or_path"] == "bert"
        # Check all expected keys exist
        expected_keys = {
            "version", "data_dir", "kg_paths", "model_name_or_path",
            "gpu", "text_path", "base_kg_path", "refined_kg_path", "filtered_kg_path"
        }
        assert set(result.keys()) == expected_keys

    def test_from_dict(self) -> None:
        """Test creating state from dictionary."""
        data = {
            "version": 2,
            "data_dir": "/from/dict",
            "kg_paths": ["x.json", "y.json"],
            "model_name_or_path": "from-dict-bert",
            "gpu": "0",
            "text_path": "",
            "base_kg_path": "",
            "refined_kg_path": "",
            "filtered_kg_path": ""
        }

        state = KGState.from_dict(data)

        assert state.version == 2
        assert state.data_dir == "/from/dict"
        assert state.kg_paths == ["x.json", "y.json"]
