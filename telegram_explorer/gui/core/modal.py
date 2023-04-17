from tkinter import Tk
from tkinter import Toplevel


class ModalForm(Toplevel):
    def __init__(self, parent: Tk) -> None:
        super().__init__(parent, bg=parent.cget("bg"))
        self.resizable(False, False)

        self.wait_visibility()
        self.grab_set()
        self.transient(parent)

    def show_modal(self) -> None:
        self._center()
        self.master.wait_window(self)

    def close(self) -> None:
        self.grab_release()
        self.destroy()

    def _center(self) -> None:
        width = self.winfo_width()
        height = self.winfo_height()

        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        # Calculate Starting X and Y coordinates for Window
        x = master_x + (master_width - width) // 2
        y = master_y + (master_height - height) // 2

        self.geometry(f"+{x}+{y}")
