import logging.handlers

import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(cur_dir))

logs_dir = os.path.join(root_dir, "logs")


def logging_config(logging_name='./recommender.log', stream_log=False, relative_path="."):
    """
    :param logging_name:  log名
    :param stream_log: 是否把log信息输出到屏幕,标准输出
    :param relative_path: 相对路径，log文件相对于logs的位置（父目录，当前目录等）
    :return: None
    """
    log_dir = os.path.join(logs_dir, relative_path, os.path.basename(logging_name))
    if not os.path.exists(logs_dir):
        os.makedirs(log_dir)
    log_handles = [logging.handlers.RotatingFileHandler(
        log_dir,
        maxBytes=20 * 1024 * 1024, backupCount=5, encoding='utf-8')]
    if stream_log:
        log_handles.append(logging.StreamHandler())
    logging.basicConfig(
        handlers=log_handles,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s %(filename)s %(funcName)s %(lineno)s - %(message)s"
    )
