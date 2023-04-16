from tkinter import Tk
from tkinter import Toplevel


class ModalForm(Toplevel):
    def __init__(self, parent: Tk) -> None:
        super().__init__(parent)
        self.wait_visibility()
        self.grab_set()
        self.transient(parent)

    def show_modal(self) -> None:
        self.master.wait_window(self)

    def close(self) -> None:
        self.grab_release()
        self.destroy()
