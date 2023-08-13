import re
from functools import wraps

from loguru import logger


def log_io(func):
    """Decorator to log the input and output of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Logging the start and input
        logger.info(f"####### Start {func.__name__} #######")
        logger.info(f"Inputs: args: {args}, kwargs: {kwargs}")

        # Call the actual function
        result = func(*args, **kwargs)

        # Logging the output
        logger.info(f"Output: {result}")
        logger.info(f"####### End {func.__name__} #######")

        return result

    return wrapper
