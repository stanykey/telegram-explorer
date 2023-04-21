"""
Encapsulate the login process into the Telegram account.

It can be used in the standalone form to log in because it depends on the `telegram` module only, which stores the
session data in the file.
"""
from tkinter import StringVar
from tkinter import Tk
from tkinter import Toplevel
from tkinter.ttk import Button
from tkinter.ttk import Entry
from tkinter.ttk import Label

from telegram_explorer import Settings
from telegram_explorer.gui.core.modal import FormResult
from telegram_explorer.gui.core.modal import ModalForm


class PhoneCodeForm(ModalForm):
    """Simple one-field form to input a code for the two-step auth flow."""

    def __init__(self, parent: Toplevel) -> None:
        super().__init__(parent)
        self.title("PhoneCode")

        self._phone_code = StringVar(self, name="phone_code")

        self._setup_layout()

    @property
    def phone_code(self) -> int:
        return int(self._phone_code.get())

    def _setup_layout(self) -> None:
        Label(self, text="Code:").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        Entry(self, textvariable=self._phone_code).grid(row=0, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)

        Button(self, text="ok", command=self.ok).grid(row=1, column=0, columnspan=2, sticky="ewns", padx=5, pady=5)
        Button(self, text="cancel", command=self.cancel).grid(row=1, column=2, sticky="ewns", padx=5, pady=5)


class LoginForm(ModalForm):
    """Login window: contains complete knowledge about the login process."""

    def __init__(self, parent: Tk, settings: Settings) -> None:
        super().__init__(parent)
        self.title("LoginForm")

        self._settings = settings

        self._phone_number = StringVar(self, value=settings.phone_number, name="phone_number")
        self._password = StringVar(self, name="password")

        self._setup_layout()

    def _setup_layout(self) -> None:
        # Phone number
        Label(self, text="Phone number:").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        Entry(self, textvariable=self._phone_number).grid(row=0, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)

        # Password
        Label(self, text="Password:").grid(row=1, column=0, sticky="ewns", padx=5, pady=5)
        password = Entry(self, textvariable=self._password, show="*")
        password.grid(row=1, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)

        # Buttons
        Button(self, text="Login", command=self._login).grid(row=2, column=1, sticky="ewns", padx=5, pady=5)
        Button(self, text="Cancel", command=self.cancel).grid(row=2, column=2, sticky="ewns", padx=5, pady=5)

    def _login(self) -> None:
        # TODO: implement login flow with Pyrogram.Client
        confirm = PhoneCodeForm(self)
        if confirm.show_modal() is FormResult.Cancel:
            return self.cancel()

        phone_number = self._phone_number.get()
        if phone_number and phone_number != self._settings.phone_number:
            self._settings.phone_number = phone_number
            self._settings.save()

        self.ok()
