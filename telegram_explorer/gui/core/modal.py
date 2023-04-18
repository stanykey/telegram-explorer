from enum import auto
from enum import IntEnum
from tkinter import Tk
from tkinter import Toplevel


class FormResult(IntEnum):
    Ok = auto()
    Cancel = auto()


class ModalForm(Toplevel):
    def __init__(self, parent: Tk | Toplevel) -> None:
        super().__init__(parent, bg=parent.cget("bg"))
        self.resizable(False, False)

        self._modal_result = FormResult.Ok

        self.wait_visibility()
        self.grab_set()
        self.transient(parent)

    def show_modal(self) -> FormResult:
        self._center()
        self.master.wait_window(self)
        return self._modal_result

    def ok(self) -> None:
        self._modal_result = FormResult.Ok
        self.close()

    def cancel(self) -> None:
        self._modal_result = FormResult.Cancel
        self.close()

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
