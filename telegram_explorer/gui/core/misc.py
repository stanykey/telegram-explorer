"""Set of helpful utilities."""
from asyncio import AbstractEventLoop
from asyncio import get_event_loop_policy
from collections.abc import Callable
from collections.abc import Coroutine
from functools import wraps
from typing import Any


def get_event_loop() -> AbstractEventLoop:
    """Wrapper to get the current event loop."""
    return get_event_loop_policy().get_event_loop()


def async_handler(async_function: Callable[..., Coroutine[Any, Any, None]]) -> Callable[..., None]:
    """Helper function to pass async functions as command handlers (e.g. button click handlers) or event handlers."""

    @wraps(async_function)
    def wrapper(*handler_args: Any) -> None:
        event_loop = get_event_loop()
        event_loop.create_task(async_function(*handler_args))

    return wrapper
