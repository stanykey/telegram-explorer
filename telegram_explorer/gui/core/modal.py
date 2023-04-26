from asyncio import sleep
from enum import auto
from enum import IntEnum
from tkinter import TclError
from tkinter import Tk
from tkinter import Toplevel
from typing import cast

from telegram_explorer.gui.core.window import centralize_window


class FormResult(IntEnum):
    Ok = auto()
    Cancel = auto()


class ModalForm(Toplevel):
    def __init__(self, parent: Tk | Toplevel, title: str = "") -> None:
        super().__init__(parent)
        self.title(title if title else parent.title())
        self.resizable(False, False)
        self.geometry("")

        self._modal_result = FormResult.Cancel
        self.protocol("WM_DELETE_WINDOW", self.close)

    def show_modal(self) -> FormResult:
        self._make_modal()
        self.master.wait_window(self)
        return self._modal_result

    async def async_show_modal(self) -> FormResult:
        self._make_modal()
        await self._run_waiting_loop()
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

    def _make_modal(self) -> None:
        self.wait_visibility()
        self.grab_set()

        if not isinstance(self.master, Tk):
            self.transient(cast(Toplevel, self.master))

        centralize_window(self, self.master)

    async def _run_waiting_loop(self) -> None:
        """Wait until modality is end."""
        while True:
            try:
                self.winfo_id()  # Will throw TclError if the window is destroyed
            except TclError:
                break

            self.update()
            await sleep(0.01)
