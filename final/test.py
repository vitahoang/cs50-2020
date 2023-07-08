import multiprocessing
import time
from functools import wraps


def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""

    def timeout_decorator(func):
        """Wrap the original function."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Closure for function."""
            # start 1 worker processes
            with multiprocessing.Pool(processes=1) as pool:
                # evaluate "f(10)" asynchronously in a single process
                result = pool.apply_async(func, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return result.get(timeout=max_timeout)

        return wrapper

    return timeout_decorator


@timeout(5)
def pri(x):
    for i in range(x):
        print("counting ", i)
        time.sleep(1)


pri(5)
