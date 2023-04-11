# 配置 logger
import logging
import logging.config
import os

FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('server')

