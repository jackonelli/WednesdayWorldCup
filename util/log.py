"""Logging module"""
import os
import logging

LOG_FORMAT = '%(asctime)-15s %(levelname)-5s %(name)-15s - %(message)s'
LOGGER = logging.getLogger(__name__)


def setup_logger(log_path=None, logger=None, debug=False, fmt=LOG_FORMAT):
    """Setup for a logger instance.

    Args:
        log_path (str, optional): full path
        debug (bool, optional): Log mode
        logger (logging.Logger, optional): logger to configure, root logger if None
        fmt (str, optional): message format

    """
    logger = logger if logger else logging.getLogger()
    fmt = logging.Formatter(fmt=fmt)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    log_level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(log_level)
    logger.handlers = []

    if log_path:
        directory = os.path.dirname(log_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        logger.info('Log at {}'.format(log_path))
