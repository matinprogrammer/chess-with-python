import logging
import os
from functools import wraps
from typing import Callable
from unittest import TestCase
from unittest.mock import patch


class CustomFormatter(logging.Formatter):
    def format(self, record):
        original_message = super().format(record)
        # return original_message + '\n'
        return original_message


def stop_logging_mock(obj: TestCase) -> None:
    """
        called in setUp() to stop logging
        :params => self in method of unittest
    """
    module_path = os.path.abspath(__file__)
    patcher = patch(module_path)
    obj.mock_logger = patcher.start()
    obj.addCleanup(patcher.stop)


class CustomLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)


def create_logger(name: str, path: str, *, file_level=logging.DEBUG, console_level=logging.WARNING,
                  logger_level=logging.DEBUG) -> logging.Logger:
    try:
        with open(path, "a") as f:
            f.write("\n" + "-" * 60 + "\n")
    except FileNotFoundError:
        os.makedirs("logs")
        with open(path, "w") as f:
            f.write("")

    file_handler = logging.FileHandler(path)
    file_handler.setLevel(file_level)  # Log all levels to the file
    file_formatter = CustomFormatter(
        '%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)  # Only log errors and above to the console
    console_formatter = CustomFormatter('%(asctime)s - %(pathname)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger_ = CustomLogger(name)
    logger_.setLevel(logger_level)  # Set the overall logging level
    logger_.addHandler(file_handler)
    logger_.addHandler(console_handler)

    return logger_


def function_logger(func: Callable):
    logger = create_logger("func_log", "logs/func_log.log")

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(
            f"func '{func.__name__}' "
            f"args {args} "
            f"kwargs {kwargs} "
            f"return {result}"
        )
        return result
    return wrapper


core_logger = create_logger("core", "logs/core.log")
windows_gui_logger = create_logger("windows_gui", "logs/windows_gui.log")
