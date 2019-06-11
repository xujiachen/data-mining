import logging
import traceback
from functools import wraps


def try_catch_with_logging(default_response=None):
    def out_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except Exception:
                res = default_response
                logging.error(traceback.format_exc())
            return res

        return wrapper

    return out_wrapper
