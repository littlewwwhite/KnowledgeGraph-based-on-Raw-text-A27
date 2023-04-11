import argparse

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["MKL_SERVICE_FORCE_INTEL"] = "1"
os.environ["MKL_THREADING_LAYER"] = "GNU"

from modules.knowledge_graph_builder import KnowledgeGraphBuilder


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="project_v1")
    parser.add_argument("--resume", type=str, default=None, help="resume from a checkpoint")# 作用是从一个checkpoint恢复
    parser.add_argument("--gpu", type=str, default="1", help="gpu id")  # 修改 GPU 在这里
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arg_parser()

    kg_builder = KnowledgeGraphBuilder(args)

    if args.resume is not None:
        kg_builder.load(args.resume)
        kg_builder.gpu = args.gpu # 这个是要换掉的

    else:
        # startup
        kg_builder.get_base_kg_from_txt()  # 预计用时：

    # iteration
    max_iteration = 10

    while kg_builder.version < max_iteration:
        kg_builder.run_iteration() # 迭代过程中会自动保存
        extend_ratio = kg_builder.extend_ratio()
        print(f"Extend Ratio: {extend_ratio}")

        if extend_ratio < 0.01:
            print("Extend Ratio is too low, stop iteration.")
            break

    print("done!")