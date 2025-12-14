"""
UIE-based relation extraction processing module.

Provides functions for extracting relation triples from text using
PaddleNLP's UIE (Universal Information Extraction) model.
"""
from typing import Any, Dict, List

from paddlenlp import Taskflow

from data.schema import schema_v4
from modules.utils.logger import logger


def paddle_relation_ie(content: List[str]) -> List[Dict[str, Any]]:
    """
    Extract relations from text using PaddleNLP UIE.

    Args:
        content: List of text segments to process.

    Returns:
        UIE extraction results with entity-relation structures.
    """
    relation_ie = Taskflow(
        "information_extraction",
        schema=schema_v4.schema,
        batch_size=2
    )
    return relation_ie(content)


def rel_json(content: str) -> List[Dict[str, str]]:
    """
    Extract relation triples from a single text segment.

    Args:
        content: Text to extract relations from.

    Returns:
        List of relation triples with em1Text, em2Text, and label.
    """
    all_relations: List[Dict[str, str]] = []
    res_relation = paddle_relation_ie([content])

    for rel in res_relation:
        for sub_type, sub_rel in rel.items():
            for sub in sub_rel:
                if sub.get("relations") is None:
                    continue
                for rel_type, rel_obj in sub["relations"].items():
                    for obj in rel_obj:
                        if not sub['text'] or not obj['text']:
                            continue
                        rel_triple = {
                            "em1Text": sub['text'],
                            "em2Text": obj['text'],
                            "label": rel_type
                        }
                        all_relations.append(rel_triple)

    return all_relations


def uie_execute(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Execute UIE extraction on multiple text segments.

    Args:
        texts: List of text segments to process.

    Returns:
        List of items with id, sentText, and relationMentions.
    """
    logger.info(f"Starting UIE extraction on {len(texts)} segments")

    all_items: List[Dict[str, Any]] = []

    for sent_id, line in enumerate(texts):
        line = line.strip()
        all_relations = rel_json(line)

        item: Dict[str, Any] = {
            "id": sent_id,
            "sentText": line,
            "relationMentions": all_relations
        }

        all_items.append(item)

        if (sent_id + 1) % 10 == 0:
            logger.info(f"Processed {sent_id + 1}/{len(texts)} segments")

    logger.success(f"UIE extraction complete: {len(all_items)} items")
    return all_items
