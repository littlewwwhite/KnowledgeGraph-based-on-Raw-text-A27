import argparse

from modules.knowledge_graph_builder import KnowledgeGraphBuilder


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="project_v1")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arg_parser()

    kg_builder = KnowledgeGraphBuilder(args)

    # startup
    kg_builder.get_base_kg_from_txt()  # 预计用时：

    # iteration
    max_iteration = 10

    for i in range(max_iteration):
        kg_builder.iteration()
        kg_builder.save()
        extend_ratio = kg_builder.extend_ratio()
        print(f"Extend Ratio: {extend_ratio}")

        if extend_ratio < 0.1:
            print("Extend Ratio is too low, stop iteration.")
            break
