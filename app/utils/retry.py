import time
import functools
from app.utils.logger import get_logger

logger = get_logger(__name__)


def retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """
    Retry decorator with exponential backoff.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            attempt = 0

            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1

                    logger.warning(
                        f"Retry {attempt}/{max_retries} for {func.__name__} due to: {e}"
                    )

                    if attempt >= max_retries:
                        logger.error(
                            f"Max retries reached for {func.__name__}"
                        )
                        raise

                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator
