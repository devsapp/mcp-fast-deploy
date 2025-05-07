import logging
import sys

logging.basicConfig(
    stream=sys.stdout,  # 指定输出到 stdout
    level=logging.INFO,  # 设置日志级别
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
LOGGER = logging.getLogger()
