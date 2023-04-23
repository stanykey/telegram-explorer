"""Helpful set of window-related operations."""
from tkinter import Misc
from tkinter import Tk
from tkinter import Toplevel


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
