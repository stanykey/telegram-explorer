"""
Encapsulate the login process into the Telegram account.

It can be used in the standalone form to log in because it depends on the `telegram` module only, which stores the
session data in the file.
"""
from asyncio import AbstractEventLoop
from enum import auto
from enum import IntEnum
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Tk
from tkinter import Toplevel
from tkinter.ttk import Button
from tkinter.ttk import Entry
from tkinter.ttk import Label

from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import User

from telegram_explorer import Settings
from telegram_explorer.gui.core.modal import FormResult
from telegram_explorer.gui.core.modal import ModalForm
from telegram_explorer.gui.core.window import show_wait_window


class PhoneCodeForm(ModalForm):
    """Simple one-field form to input a code for the two-step auth flow."""

    def __init__(self, parent: Toplevel) -> None:
        super().__init__(parent)
        self.title("PhoneCode")

        self._phone_code = StringVar(self, name="phone_code")

        self._create_controls()

    @property
    def phone_code(self) -> str:
        return self._phone_code.get()

    def _create_controls(self) -> None:
        Label(self, text="Code:").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        Entry(self, textvariable=self._phone_code).grid(row=0, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)

        Button(self, text="ok", command=self.ok).grid(row=1, column=0, columnspan=2, sticky="ewns", padx=5, pady=5)
        Button(self, text="cancel", command=self.cancel).grid(row=1, column=2, sticky="ewns", padx=5, pady=5)


class LoginResult(IntEnum):
    Success = auto()
    Cancelled = auto()
    PhoneNumberInvalid = auto()
    CodeWrong = auto()
    UserUnregistered = auto()
    PasswordIncorrect = auto()


class LoginForm(ModalForm):
    """Login window: contains complete knowledge about the login process."""

    def __init__(self, parent: Tk | Toplevel, settings: Settings, loop: AbstractEventLoop, *, title: str = "") -> None:
        super().__init__(parent, title)

        self._settings = settings
        self._loop = loop

        self._phone_number = StringVar(self, value=settings.phone_number, name="phone_number")
        self._password = StringVar(self, name="password")

        self._create_controls()

    def _create_controls(self) -> None:
        # Phone number
        Label(self, text="Phone number:").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        Entry(self, textvariable=self._phone_number).grid(row=0, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)

        # Password
        Label(self, text="Password:").grid(row=1, column=0, sticky="ewns", padx=5, pady=5)
        password = Entry(self, textvariable=self._password, show="*")
        password.grid(row=1, column=1, columnspan=2, sticky="ewns", padx=5, pady=5)

        # Buttons
        Button(self, text="Login", command=self._request_login).grid(row=2, column=1, sticky="ewns", padx=5, pady=5)
        Button(self, text="Cancel", command=self.cancel).grid(row=2, column=2, sticky="ewns", padx=5, pady=5)

    def _request_login(self) -> None:
        if not self._phone_number.get():
            messagebox.showerror(title="Error", message="Phone number is empty")
            return

        if not self._password.get():
            messagebox.showerror(title="Error", message="Password is empty")
            return

        self._loop.create_task(self._login())

    async def _login(self) -> None:
        status = await self._do_login_process()
        if status is LoginResult.Success:
            phone_number = self._phone_number.get()
            if phone_number != self._settings.phone_number:
                self._settings.phone_number = phone_number
                self._settings.save()
            return self.ok()

        if status is not LoginResult.Cancelled:
            self._show_login_error(status)

    async def _do_login_process(self) -> LoginResult:
        """Adopted version of the code/logic extracted pyrogram.Client class."""
        waiter = show_wait_window(self, message="Connecting to Telegram server...")

        client = Client(
            name=self._settings.session_name,
            api_id=self._settings.api_id,
            api_hash=self._settings.api_hash,
            phone_number=self._settings.phone_number,
            workdir=str(self._settings.get_session_dir()),
        )

        try:
            if await client.connect():
                return LoginResult.Success

            phone_number = self._phone_number.get()
            try:
                sent_code = await client.send_code(phone_number)
                waiter.destroy()

                confirm = PhoneCodeForm(self)
                if confirm.show_modal() is FormResult.Cancel:
                    return LoginResult.Cancelled
            except BadRequest:
                return LoginResult.PhoneNumberInvalid

            try:
                signed_in = await client.sign_in(phone_number, sent_code.phone_code_hash, confirm.phone_code)
                return LoginResult.Success if isinstance(signed_in, User) else LoginResult.UserUnregistered
            except BadRequest:
                return LoginResult.CodeWrong
            except SessionPasswordNeeded:
                try:
                    await client.check_password(self._password.get())
                    return LoginResult.Success
                except BadRequest:
                    return LoginResult.PasswordIncorrect
        finally:
            await client.disconnect()
            waiter.destroy()

    @staticmethod
    def _show_login_error(error: LoginResult) -> None:
        if error is LoginResult.Success:
            return

        messagebox.showerror("Login Error", str(error))
