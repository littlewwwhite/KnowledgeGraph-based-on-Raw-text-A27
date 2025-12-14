"""
Utility functions for knowledge graph data refinement.
"""
import json
import os
from typing import List

from modules.utils.logger import logger


def check_input(prompt: str, keys: List[str]) -> str:
    """
    Prompt user for input and validate against allowed keys.

    Args:
        prompt: The prompt message to display.
        keys: List of valid input values.

    Returns:
        The validated user input.
    """
    while True:
        user_input = input(f"{prompt} > ")
        if user_input in keys:
            return user_input
        print("Invalid input, please try again")


def refine_knowledge_graph(
    kg_path: str,
    refined_kg_path: str,
    fast_mode: bool = True
) -> str:
    """
    Manually refine knowledge graph by filtering relation triples.

    Args:
        kg_path: Path to original knowledge graph file.
        refined_kg_path: Path to save refined knowledge graph.
        fast_mode: If True, skip manual filtering and copy directly.

    Returns:
        Path to the refined knowledge graph file.

    Raises:
        FileNotFoundError: If source file does not exist.
        KeyboardInterrupt: If user cancels the operation.
    """
    logger.info(f"Source: {kg_path}")
    logger.info(f"Target: {refined_kg_path}")

    # Determine starting position for resume support
    start_pos = 0

    if os.path.exists(refined_kg_path):
        try:
            with open(kg_path, 'r', encoding='UTF-8') as f_src:
                kg_lines = [json.loads(line) for line in f_src if line.strip()]

            with open(refined_kg_path, 'r', encoding='UTF-8') as f_refined:
                refined_lines = [json.loads(line) for line in f_refined if line.strip()]

            # Find where to resume
            for i, (kg_line, ref_line) in enumerate(zip(kg_lines, refined_lines)):
                if kg_line.get("id") == ref_line.get("id"):
                    start_pos = i + 1
                else:
                    break

            if start_pos > 0:
                logger.info(f"Resuming from entry {start_pos + 1} ({start_pos} already processed)")

        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Could not parse existing refined file ({e}), starting fresh")
            start_pos = 0

    # Read source data
    with open(kg_path, 'r', encoding='UTF-8') as f_in:
        lines = [json.loads(line) for line in f_in if line.strip()]

    total = len(lines)

    # Open output file in append mode if resuming, write mode otherwise
    write_mode = 'a' if start_pos > 0 else 'w'

    with open(refined_kg_path, write_mode, encoding='UTF-8') as f_out:
        for pos in range(start_pos, total):
            line = lines[pos]

            if fast_mode:
                f_out.write(json.dumps(line, ensure_ascii=False) + "\n")
                if pos == start_pos:
                    logger.info("Fast mode enabled, copying data without manual filtering")
                continue

            # Manual filtering mode
            print(f"\n【 {pos+1}/{total} 】Processing sentence >>>>>>>>")
            print(line["sentText"])

            refined_triples = []
            for triple in line.get("relationMentions", []):
                print(f"\nSubject: 【{triple['em1Text']}】")
                print(f"Relation: 【{triple['label']}】")
                print(f"Object: 【{triple['em2Text']}】")

                user_input = check_input(
                    prompt="Keep this triple? [Y]es / [N]o / [Enter] to exit",
                    keys=["Y", "y", "N", "n", ""]
                )

                if user_input.lower() == "y":
                    refined_triples.append(triple)
                elif user_input == "":
                    logger.warning("User cancelled refinement process")
                    raise KeyboardInterrupt("User cancelled refinement")

            line["relationMentions"] = refined_triples
            f_out.write(json.dumps(line, ensure_ascii=False) + "\n")
            print("Saved!")

    logger.success("Refinement complete")
    return refined_kg_path
