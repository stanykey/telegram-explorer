from tkinter import IntVar
from tkinter import StringVar
from tkinter import Tk
from tkinter.ttk import Button
from tkinter.ttk import Entry
from tkinter.ttk import Label

from telegram_explorer import Settings
from telegram_explorer.gui.core.modal import ModalForm


class SettingsForm(ModalForm):
    def __init__(self, parent: Tk, settings: Settings | None = None) -> None:
        super().__init__(parent)
        self.title("SettingsForm")

        self._settings = Settings.load_default() if settings is None else settings
        self._api_id = IntVar(self, value=self._settings.api_id, name="api_id")
        self._api_hash = StringVar(self, value=self._settings.api_hash, name="api_hash")
        self._setup_layout()

    @property
    def setting(self) -> Settings:
        return self._settings

    def _setup_layout(self) -> None:
        Label(self, text="API ID").grid(row=0, column=0, sticky="EW", padx=5, pady=5)
        Entry(self, textvariable=self._api_id).grid(row=0, column=1, columnspan=2, sticky="EW", padx=5, pady=5)

        Label(self, text="API Hash").grid(row=1, column=0, sticky="EW", padx=5, pady=5)
        Entry(self, textvariable=self._api_hash).grid(row=1, column=1, columnspan=2, sticky="EW", padx=5, pady=5)

        Button(self, text="Save", command=self._save).grid(row=2, column=1, sticky="EW", padx=5, pady=5)
        Button(self, text="Cancel", command=self.cancel).grid(row=2, column=2, sticky="EW", padx=5, pady=5)

    def _save(self) -> None:
        self._settings.api_id = self._api_id.get()
        self._settings.api_hash = self._api_hash.get()
        self._settings.save()
        self.ok()
