import argparse

from config.settings import settings, load_dotenv
from modules.utils.logger import logger, green, yellow

# Load .env file if exists
load_dotenv()

# Setup CUDA environment
settings.setup_cuda()

from modules.knowledge_graph_builder import KnowledgeGraphBuilder


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="project_v1")
    parser.add_argument("--resume", type=str, default=None, help="resume from a checkpoint")
    parser.add_argument("--gpu", type=str, default=settings.DEFAULT_GPU, help="gpu id")
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
    max_iteration = settings.MAX_ITERATION

    while kg_builder.version < max_iteration:
        kg_builder.run_iteration()
        extend_ratio = kg_builder.extend_ratio()
        logger.info(f"{green('Extend Ratio:')} {yellow(f'{extend_ratio:.4f}')}")

        if extend_ratio < settings.EXTEND_RATIO_THRESHOLD:
            logger.warning("Extend ratio below threshold, stopping iteration")
            break

    logger.success("Knowledge graph construction complete")