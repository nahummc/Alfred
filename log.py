# log.py
import logging


def setup_logger(file_path="discord.log", log_level=logging.INFO):
    """
    Setup logging configuration
    :param file_path: The file path where logs will be stored. Default is 'application.log'.
    :param log_level: The logging level. Default is logging.INFO.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Create file handler
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(log_level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create a formatter and set the formatter for the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
