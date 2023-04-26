"""
Simple applications settings editor.

It can be used in the standalone form to edit settings.
"""
from tkinter import GROOVE
from tkinter import IntVar
from tkinter import StringVar
from tkinter import Tk
from tkinter import Toplevel
from tkinter.ttk import Button
from tkinter.ttk import Entry
from tkinter.ttk import Label
from tkinter.ttk import Labelframe

from telegram_explorer import Settings
from telegram_explorer.gui.core.modal import ModalForm


class SettingsForm(ModalForm):
    def __init__(self, parent: Tk | Toplevel, settings: Settings, *, title: str = "") -> None:
        super().__init__(parent, title)

        self._settings = settings

        self._session_name = StringVar(self, value=self._settings.session_name, name="session_name")
        self._phone_number = StringVar(self, value=self._settings.phone_number, name="phone_number")
        self._api_id = IntVar(self, value=self._settings.api_id, name="api_id")
        self._api_hash = StringVar(self, value=self._settings.api_hash, name="api_hash")
        self._create_controls()

    @property
    def setting(self) -> Settings:
        return self._settings

    def _create_controls(self) -> None:
        frame = Labelframe(self, text="Account", relief=GROOVE, borderwidth=5)
        Label(frame, text="Session name ").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        Entry(frame, textvariable=self._session_name).grid(row=0, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)
        Label(frame, text="Phone        ").grid(row=1, column=0, sticky="ewns", padx=5, pady=5)
        Entry(frame, textvariable=self._phone_number).grid(row=1, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)
        frame.grid(row=0, column=0, columnspan=3, sticky="ewns", padx=5, pady=5)

        frame = Labelframe(self, text="Api Info", relief=GROOVE, borderwidth=5)
        Label(frame, text="API ID       ").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        Entry(frame, textvariable=self._api_id).grid(row=0, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)
        Label(frame, text="API Hash     ").grid(row=1, column=0, sticky="ewns", padx=5, pady=5)
        Entry(frame, textvariable=self._api_hash).grid(row=1, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)
        frame.grid(row=1, column=0, columnspan=3, sticky="ewns", padx=5, pady=5)

        Button(self, text="Save", command=self._save).grid(row=2, column=1, sticky="ewns", padx=5, pady=5)
        Button(self, text="Cancel", command=self.cancel).grid(row=2, column=2, sticky="ewns", padx=5, pady=5)

    def _save(self) -> None:
        self._settings.session_name = self._session_name.get()
        self._settings.phone_number = self._phone_number.get()
        self._settings.api_id = self._api_id.get()
        self._settings.api_hash = self._api_hash.get()
        self._settings.save()
        self.ok()
