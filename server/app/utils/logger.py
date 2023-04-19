# 配置 logger
import logging
import logging.config
import os

FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s' # 配置日志格式
logging.basicConfig(format=FORMAT)# basicConfig函数对日志的输出格式及方式做相关配置
logger = logging.getLogger('server')# getLogger函数通过指定的名称获取日志器

