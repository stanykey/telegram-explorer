"""Set of helpers to work with asynio."""
from asyncio import run
from collections.abc import Coroutine
from typing import Any


def execute_synchronously(coroutine: Coroutine[Any, Any, Any]) -> Any:
    """Run asynchronous `coroutine` and wait until it end."""
    return run(coroutine)
