from functools import wraps
import logging


def wrapexception(func, logger=logging):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                r = func(*args, **kwargs)
            except IndexError as e:
                if self.debug:
                    logging.error("Bounds Error: "+str(e))
                    raise e

        return wrapper

    return decorator
