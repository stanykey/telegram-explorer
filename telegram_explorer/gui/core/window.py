"""Helpful set of window-related operations."""
from tkinter import GROOVE
from tkinter import Misc
from tkinter import Tk
from tkinter import Toplevel
from tkinter.ttk import Frame
from tkinter.ttk import Label
from tkinter.ttk import Progressbar


def show_wait_window(parent: Toplevel, message: str, interval: int = 5) -> Toplevel:
    parent.attributes("-disabled", True)

    waiter = Toplevel(parent)
    waiter.resizable(False, False)
    waiter.transient(parent)

    def close() -> None:
        parent.attributes("-disabled", False)
        waiter.destroy()

    waiter.protocol("WM_DELETE_WINDOW", close)

    frame = Frame(waiter, relief=GROOVE, borderwidth=5)
    Label(frame, text=message).grid(row=0, column=0, sticky="ewns", padx=1, pady=1)

    progress = Progressbar(frame, orient="horizontal", mode="indeterminate")
    progress.grid(row=1, column=0, sticky="ewns", padx=1, pady=1)
    frame.pack()

    centralize_window(waiter, parent)
    waiter.overrideredirect(True)

    progress.start(interval)
    return waiter


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
