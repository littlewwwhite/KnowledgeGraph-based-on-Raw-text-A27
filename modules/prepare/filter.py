"""
Filter module for knowledge graph data validation.

Validates extracted triples against BERT tokenization to ensure
entities are properly tokenizable and within sentence bounds.
"""
from typing import Any, Dict, List

from transformers import AutoTokenizer

from modules.utils.logger import logger


def auto_filter(
    items: List[Dict[str, Any]],
    model_name_or_path: str
) -> List[Dict[str, Any]]:
    """
    Filter invalid triples based on BERT tokenization.

    Removes triples where:
    - Entity tokens are empty after tokenization
    - Entity tokens exceed 15 tokens
    - Entity tokens don't appear in tokenized sentence

    Args:
        items: List of knowledge graph items with relationMentions.
        model_name_or_path: BERT model name or path for tokenization.

    Returns:
        Filtered items with invalid relations removed.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

    filtered_count = 0
    total_relations = 0

    for example in items:
        sent_tokens = tokenizer.tokenize(example["sentText"])

        relations: List[Dict[str, Any]] = []
        for relation in example["relationMentions"]:
            total_relations += 1
            sub_tokens = tokenizer.tokenize(relation["em1Text"])
            obj_tokens = tokenizer.tokenize(relation["em2Text"])

            # Skip empty or overly long entities
            if len(sub_tokens) == 0 or len(obj_tokens) == 0:
                filtered_count += 1
                continue

            if len(sub_tokens) > 15 or len(obj_tokens) > 15:
                filtered_count += 1
                continue

            # Find subject position in sentence
            sub_start = _find_token_position(sent_tokens, sub_tokens)
            if sub_start == -1:
                logger.debug(f"Subject not in sentence: {relation['em1Text']}")
                filtered_count += 1
                continue

            # Find object position in sentence
            obj_start = _find_token_position(sent_tokens, obj_tokens)
            if obj_start == -1:
                logger.debug(f"Object not in sentence: {relation['em2Text']}")
                filtered_count += 1
                continue

            relations.append({
                "em1Text": relation["em1Text"],
                "em2Text": relation["em2Text"],
                "label": relation["label"],
                "em1Start": sub_start,
                "em1End": sub_start + len(sub_tokens) - 1,
                "em2Start": obj_start,
                "em2End": obj_start + len(obj_tokens) - 1
            })

        example["relationMentions"] = relations

    if filtered_count > 0:
        logger.info(f"Filtered {filtered_count}/{total_relations} invalid relations")

    return items


def _find_token_position(
    sentence_tokens: List[str],
    entity_tokens: List[str]
) -> int:
    """
    Find the starting position of entity tokens within sentence tokens.

    Args:
        sentence_tokens: Tokenized sentence.
        entity_tokens: Tokenized entity to find.

    Returns:
        Starting index if found, -1 otherwise.
    """
    for i in range(len(sentence_tokens) - len(entity_tokens) + 1):
        if sentence_tokens[i:i + len(entity_tokens)] == entity_tokens:
            return i
    return -1
