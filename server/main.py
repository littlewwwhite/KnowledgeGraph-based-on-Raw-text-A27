import os
import sys

# Add project root to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings, load_dotenv
from modules.utils.logger import logger

# Load environment variables
load_dotenv()

# Setup CUDA before importing models
os.environ["CUDA_VISIBLE_DEVICES"] = settings.CUDA_VISIBLE_DEVICES

from app import apps
from app.utils.chat_glm import start_model


if __name__ == '__main__':
    logger.info("Starting ChatGLM model...")
    start_model()
    apps.secret_key = settings.SECRET_KEY
    logger.info(f"Server running on {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    apps.run(
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        debug=settings.DEBUG,
        threaded=True
    )

