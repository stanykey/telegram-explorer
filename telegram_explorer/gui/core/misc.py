"""Set of helpful utilities."""
from asyncio import AbstractEventLoop
from asyncio import get_event_loop_policy
from collections.abc import Callable
from collections.abc import Coroutine
from functools import wraps
from tkinter import Misc
from tkinter import Tk
from tkinter import Toplevel
from typing import Any


def centralize_window(window: Tk | Toplevel, parent: Tk | Toplevel | Misc | None = None) -> None:
    """Place the `window` in the middle of the `parent` or screen if omitted."""
    window.update()

    master_x = parent.winfo_x() if parent else 0
    master_y = parent.winfo_y() if parent else 0
    master_width = parent.winfo_width() if parent else window.winfo_screenwidth()
    master_height = parent.winfo_height() if parent else window.winfo_screenheight()

    # Calculate Starting X and Y coordinates for Window
    x = master_x + (master_width - window.winfo_width()) // 2
    y = master_y + (master_height - window.winfo_height()) // 2

    window.geometry(f"+{x}+{y}")


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
