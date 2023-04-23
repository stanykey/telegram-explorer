from asyncio import AbstractEventLoop
from datetime import date
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Tk
from tkinter import Toplevel
from tkinter.ttk import Button
from tkinter.ttk import Combobox
from tkinter.ttk import Label
from tkinter.ttk import Treeview

from tkcalendar import DateEntry

from telegram_explorer import Settings
from telegram_explorer.gui.core.misc import centralize_window
from telegram_explorer.gui.core.variable import DateVar
from telegram_explorer.gui.forms import FormResult
from telegram_explorer.gui.forms import LoginForm
from telegram_explorer.gui.forms import SettingsForm
from telegram_explorer.telegram import Chat
from telegram_explorer.telegram import ChatType
from telegram_explorer.telegram import Message
from telegram_explorer.telegram import TelegramClient


class MainWindow(Toplevel):
    def __init__(self, parent: Tk | Toplevel, settings: Settings, loop: AbstractEventLoop) -> None:
        super().__init__(parent)
        self.resizable(False, False)

        self._settings = settings
        self._loop = loop

        self._chats: dict[str, Chat] = dict()

        self._chat_name = StringVar(self, name="chat-name")
        self._date_from = DateVar(self, name="date-from")
        self._date_to = DateVar(self, name="date-to")

        self.overrideredirect(True)
        self.withdraw()
        self._create_controls()
        centralize_window(self, parent)
        self.overrideredirect(False)
        self.deiconify()

        self._loop.create_task(self._get_chats_list())

    def _create_controls(self) -> None:
        # Chat selection
        Label(self, text="Chat:").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        self._chatsbox = Combobox(self, state="readonly", textvariable=self._chat_name)
        self._chatsbox.grid(row=0, column=1, columnspan=3, sticky="ewns", padx=5, pady=5)

        # Dates selections
        Label(self, text="Start Date:").grid(row=1, column=0, sticky="ewns", padx=5, pady=5)
        self._date_entry_from = DateEntry(self, textvariable=self._date_from, date_pattern="dd.mm.yyyy")
        self._date_entry_from.set_date(date.today())
        self._date_entry_from.grid(row=1, column=1, sticky="ewns", padx=5, pady=5)

        Label(self, text="End Date:").grid(row=1, column=2, sticky="ens", padx=5, pady=5)
        self._date_entry_to = DateEntry(self, textvariable=self._date_to, date_pattern="dd.mm.yyyy")
        self._date_entry_to.set_date(date.today())
        self._date_entry_to.grid(row=1, column=3, sticky="ewns", padx=5, pady=5)

        # Buttons
        settings_button = Button(self, text="Settings", command=self._show_settings)
        settings_button.grid(row=2, column=0, sticky="ewns", padx=5, pady=5)

        download_button = Button(self, text="Download History", command=self._request_download_history)
        download_button.grid(row=2, column=3, columnspan=1, sticky="ewns", padx=5, pady=5)

        # Messages grid view
        columns = ("date", "author", "text")
        self._messages = Treeview(self, columns=columns, show="headings")
        for col in columns:
            self._messages.heading(col, text=col)
            self._messages.column(col, width=100, stretch=False)
        self._messages.column("text", width=100, stretch=True)

        self._messages.grid(row=3, column=0, columnspan=4, sticky="ewns", padx=5, pady=5)

    def _show_settings(self) -> None:
        form = SettingsForm(self, self._settings, title="Settings")
        form.show_modal()

    def _request_download_history(self) -> None:
        if not self._chat_name.get():
            messagebox.showerror(title="Error", message="Select chat first")
            return

        start = self._date_from.get()
        end = self._date_to.get()
        if not (start and end):
            messagebox.showerror(title="Error", message="Choose dates")
            return

        if start > end:
            messagebox.showerror(title="Error", message="Start date must be less or equal to End date")
            return

        self._loop.create_task(self._download_history())

    def _get_telegram_client(self) -> TelegramClient:
        return TelegramClient(
            name="telegram-explorer",
            api_id=self._settings.api_id,
            api_hash=self._settings.api_hash,
            phone_number=self._settings.phone_number,
            session_dir=self._settings.get_session_dir(),
        )

    async def _get_chats_list(self) -> None:
        if not await self._login():
            return

        client = self._get_telegram_client()
        chats = await client.get_chats()
        await self._fill_chats_box(chats)

    async def _download_history(self) -> None:
        if not await self._login():
            return

        chat = self._chats.get(self._chat_name.get())
        date_from = self._date_from.get()
        date_to = self._date_to.get()

        client = self._get_telegram_client()
        history = await client.download_history(chat, date_from, date_to)
        await self._fill_messages_grid(history)

    async def _check_session(self) -> bool:
        """Check for authorization status."""
        client = self._get_telegram_client()
        return await client.is_authorized()

    async def _login(self, *, force: bool = False) -> bool:
        """Initiate logic procedure which can take a lot of time."""
        if not force and await self._check_session():
            return True

        login_form = LoginForm(self, self._settings)
        status = login_form.show_modal()
        return status is not FormResult.Ok

    async def _fill_chats_box(self, chats: list[Chat]) -> None:
        allowed_chat_types = (ChatType.PRIVATE, ChatType.GROUP, ChatType.CHANNEL, ChatType.SUPERGROUP)
        self._chats = {
            self._get_chat_title(chat): chat for idx, chat in enumerate(chats) if chat.type in allowed_chat_types
        }

        self._chatsbox["values"] = list(self._chats.keys())
        self._chatsbox["state"] = "readonly"

    @staticmethod
    def _get_chat_title(chat: Chat) -> str:
        if chat.type is ChatType.PRIVATE:
            return " ".join(text for text in (chat.first_name, chat.last_name) if text)

        return str(chat.title) if chat.title else ""

    async def _fill_messages_grid(self, history: list[Message]) -> None:
        self._clear_history()
        for msg in history:
            visible_values = msg.date.date(), msg.author_signature, msg.text
            self._messages.insert("", "end", values=visible_values)

    def _clear_history(self) -> None:
        rows = self._messages.get_children()
        self._messages.delete(*rows)
