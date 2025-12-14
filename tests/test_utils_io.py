"""
Tests for modules/utils/io.py - JSON/JSONL IO utilities.
"""
import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from modules.utils.io import read_json, read_jsonl, write_json, write_jsonl


class TestReadJsonl:
    """Tests for read_jsonl function."""

    def test_read_valid_jsonl(
        self,
        sample_jsonl_file: Path,
        sample_kg_data: List[Dict[str, Any]]
    ) -> None:
        """Test reading a valid JSONL file."""
        result = read_jsonl(sample_jsonl_file)
        assert len(result) == len(sample_kg_data)
        assert result[0]["id"] == 0
        assert result[0]["sentText"] == sample_kg_data[0]["sentText"]

    def test_read_empty_jsonl(self, temp_dir: Path) -> None:
        """Test reading an empty JSONL file."""
        empty_file = temp_dir / "empty.jsonl"
        empty_file.touch()
        result = read_jsonl(empty_file)
        assert result == []

    def test_read_jsonl_with_blank_lines(self, temp_dir: Path) -> None:
        """Test reading JSONL file with blank lines."""
        file_path = temp_dir / "with_blanks.jsonl"
        with open(file_path, 'w') as f:
            f.write('{"id": 0}\n')
            f.write('\n')
            f.write('{"id": 1}\n')
            f.write('   \n')
            f.write('{"id": 2}\n')
        result = read_jsonl(file_path)
        assert len(result) == 3
        assert [item["id"] for item in result] == [0, 1, 2]

    def test_read_nonexistent_file(self) -> None:
        """Test reading a file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            read_jsonl("/nonexistent/path/file.jsonl")

    def test_read_jsonl_string_path(
        self,
        sample_jsonl_file: Path,
        sample_kg_data: List[Dict[str, Any]]
    ) -> None:
        """Test reading with string path instead of Path object."""
        result = read_jsonl(str(sample_jsonl_file))
        assert len(result) == len(sample_kg_data)


class TestWriteJsonl:
    """Tests for write_jsonl function."""

    def test_write_valid_jsonl(
        self,
        temp_dir: Path,
        sample_kg_data: List[Dict[str, Any]]
    ) -> None:
        """Test writing valid JSONL data."""
        output_path = temp_dir / "output.jsonl"
        write_jsonl(sample_kg_data, output_path)

        assert output_path.exists()
        result = read_jsonl(output_path)
        assert len(result) == len(sample_kg_data)

    def test_write_empty_list(self, temp_dir: Path) -> None:
        """Test writing empty list creates empty file."""
        output_path = temp_dir / "empty_output.jsonl"
        write_jsonl([], output_path)

        assert output_path.exists()
        result = read_jsonl(output_path)
        assert result == []

    def test_write_creates_parent_dirs(self, temp_dir: Path) -> None:
        """Test that writing creates parent directories."""
        output_path = temp_dir / "nested" / "dir" / "output.jsonl"
        write_jsonl([{"test": 1}], output_path)

        assert output_path.exists()
        result = read_jsonl(output_path)
        assert result == [{"test": 1}]

    def test_write_unicode_content(self, temp_dir: Path) -> None:
        """Test writing Unicode content (Chinese characters)."""
        data = [
            {"id": 0, "text": "北京是中国的首都"},
            {"id": 1, "text": "上海是经济中心"}
        ]
        output_path = temp_dir / "unicode.jsonl"
        write_jsonl(data, output_path, ensure_ascii=False)

        result = read_jsonl(output_path)
        assert result[0]["text"] == "北京是中国的首都"


class TestReadJson:
    """Tests for read_json function."""

    def test_read_valid_json(self, sample_json_file: Path) -> None:
        """Test reading a valid JSON file."""
        result = read_json(sample_json_file)
        assert result["name"] == "test_project"
        assert result["version"] == 1
        assert len(result["instances"]) == 3

    def test_read_nonexistent_json(self) -> None:
        """Test reading a JSON file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            read_json("/nonexistent/path/file.json")


class TestWriteJson:
    """Tests for write_json function."""

    def test_write_valid_json(self, temp_dir: Path) -> None:
        """Test writing valid JSON data."""
        data = {"key": "value", "number": 42}
        output_path = temp_dir / "output.json"
        write_json(data, output_path)

        assert output_path.exists()
        result = read_json(output_path)
        assert result == data

    def test_write_json_pretty_print(self, temp_dir: Path) -> None:
        """Test that JSON is written with indentation."""
        data = {"a": 1, "b": 2}
        output_path = temp_dir / "pretty.json"
        write_json(data, output_path, indent=2)

        content = output_path.read_text()
        assert "\n" in content  # Should have newlines for pretty printing

    def test_write_json_creates_parent_dirs(self, temp_dir: Path) -> None:
        """Test that writing creates parent directories."""
        output_path = temp_dir / "nested" / "output.json"
        write_json({"test": True}, output_path)

        assert output_path.exists()
