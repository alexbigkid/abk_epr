#!/usr/bin/env python
"""Common functionality."""

# Standard library imports
import logging
import timeit


# Third party imports
from colorama import Fore


# Local application imports


def function_trace(original_function):
    """Decorator function to help to trace function call entry and exit.

    Args:
        original_function (_type_): function above which the decorater is defined
    """

    def function_wrapper(*args, **kwargs):
        _logger = logging.getLogger(original_function.__name__)
        _logger.debug(f"{Fore.CYAN}-> {original_function.__name__}{Fore.RESET}")
        result = original_function(*args, **kwargs)
        _logger.debug(f"{Fore.CYAN}<- {original_function.__name__}{Fore.RESET}\n")
        return result

    return function_wrapper


class PerformanceTimer:
    """Calculates time spent. Should be used as context manager."""

    def __init__(self, timer_name, logger):
        """Init for performance timer."""
        self._timer_name = timer_name
        self._logger = logger

    def __enter__(self):
        """Enter for performance timer."""
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit for performance timer."""
        time_took = (timeit.default_timer() - self.start) * 1000.0
        self._logger.info(f"Executing {self._timer_name} took {str(time_took)} ms")


if __name__ == "__main__":
    raise Exception(f"{__file__}: This module should not be executed directly. Only for imports.")
