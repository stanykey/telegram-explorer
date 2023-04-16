from tkinter import Button
from tkinter import Entry
from tkinter import Tk

from telegram_explorer.gui.core.modal import ModalForm


class SettingsForm(ModalForm):
    def __init__(self, parent: Tk) -> None:
        super().__init__(parent)
        self.title("SettingsForm")
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.data = Entry(self)
        self.data.pack()

        Button(self, text="ok", command=self.close).pack()
