"""
Unified I/O utilities for JSON file operations.

This module provides consistent interfaces for reading and writing JSON/JSONL files,
replacing scattered inline implementations throughout the codebase.
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Union, Iterator


PathLike = Union[str, Path]


def read_jsonl(file_path: PathLike) -> List[Dict[str, Any]]:
    """
    Read a JSON Lines file (one JSON object per line).

    Args:
        file_path: Path to the JSONL file.

    Returns:
        List of parsed JSON objects.

    Raises:
        FileNotFoundError: If file does not exist.
        json.JSONDecodeError: If JSON parsing fails.
    """
    path = Path(file_path)
    with path.open('r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def read_jsonl_iter(file_path: PathLike) -> Iterator[Dict[str, Any]]:
    """
    Read a JSON Lines file lazily (memory efficient for large files).

    Args:
        file_path: Path to the JSONL file.

    Yields:
        Parsed JSON objects one at a time.
    """
    path = Path(file_path)
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def write_jsonl(
    data: List[Dict[str, Any]],
    file_path: PathLike,
    ensure_ascii: bool = False
) -> None:
    """
    Write a list of objects to a JSON Lines file.

    Args:
        data: List of JSON-serializable objects.
        file_path: Output file path.
        ensure_ascii: If True, escape non-ASCII characters.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=ensure_ascii) + '\n')


def append_jsonl(
    item: Dict[str, Any],
    file_path: PathLike,
    ensure_ascii: bool = False
) -> None:
    """
    Append a single object to a JSON Lines file.

    Args:
        item: JSON-serializable object.
        file_path: Output file path.
        ensure_ascii: If True, escape non-ASCII characters.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=ensure_ascii) + '\n')


def read_json(file_path: PathLike) -> Dict[str, Any]:
    """
    Read a standard JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Parsed JSON object.
    """
    path = Path(file_path)
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def write_json(
    data: Any,
    file_path: PathLike,
    ensure_ascii: bool = False,
    indent: int = 2
) -> None:
    """
    Write an object to a JSON file.

    Args:
        data: JSON-serializable object.
        file_path: Output file path.
        ensure_ascii: If True, escape non-ASCII characters.
        indent: Indentation level for pretty printing.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=indent)
