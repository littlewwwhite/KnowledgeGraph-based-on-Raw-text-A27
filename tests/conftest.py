"""
Pytest fixtures for KnowledgeGraph tests.
"""
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator, List

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_kg_data() -> List[Dict[str, Any]]:
    """Sample knowledge graph data for testing."""
    return [
        {
            "id": 0,
            "sentText": "Albert Einstein developed the theory of relativity.",
            "relationMentions": [
                {
                    "em1Text": "Albert Einstein",
                    "em2Text": "theory of relativity",
                    "label": "developed"
                }
            ]
        },
        {
            "id": 1,
            "sentText": "Python is a programming language created by Guido van Rossum.",
            "relationMentions": [
                {
                    "em1Text": "Python",
                    "em2Text": "programming language",
                    "label": "is_a"
                },
                {
                    "em1Text": "Python",
                    "em2Text": "Guido van Rossum",
                    "label": "created_by"
                }
            ]
        },
        {
            "id": 2,
            "sentText": "Beijing is the capital of China.",
            "relationMentions": [
                {
                    "em1Text": "Beijing",
                    "em2Text": "China",
                    "label": "capital_of"
                }
            ]
        }
    ]


@pytest.fixture
def sample_jsonl_file(temp_dir: Path, sample_kg_data: List[Dict[str, Any]]) -> Path:
    """Create a sample JSONL file for testing."""
    file_path = temp_dir / "sample.jsonl"
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in sample_kg_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    return file_path


@pytest.fixture
def sample_json_file(temp_dir: Path) -> Path:
    """Create a sample JSON file for testing."""
    file_path = temp_dir / "sample.json"
    data = {
        "name": "test_project",
        "version": 1,
        "instances": ["relation_a", "relation_b", "relation_c"]
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file_path


@pytest.fixture
def empty_kg_data() -> List[Dict[str, Any]]:
    """Empty knowledge graph data for edge case testing."""
    return []


@pytest.fixture
def kg_data_no_relations() -> List[Dict[str, Any]]:
    """Knowledge graph data with no relations."""
    return [
        {
            "id": 0,
            "sentText": "This sentence has no extracted relations.",
            "relationMentions": []
        }
    ]
