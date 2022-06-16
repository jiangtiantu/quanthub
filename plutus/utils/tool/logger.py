import logging
import os

from plutus.utils.tool.configer import Configer


def log_record(file_name, log_name):
    """
    日志记录
    :param file_name:
    :param log_name:
    :return:
    """
    config = Configer()
    log_fp = os.path.join(
        config.root_dir, "plutus", os.sep.join(["logs", f"{log_name}.log"])
    )
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)
    filing = logging.FileHandler(filename=log_fp)
    streaming = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    filing.setFormatter(formatter)
    streaming.setFormatter(formatter)
    logger.addHandler(filing)
    logger.addHandler(streaming)
    return logger
