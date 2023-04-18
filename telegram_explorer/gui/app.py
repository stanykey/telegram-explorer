from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from asyncio import sleep
from datetime import date
from tkinter.ttk import Button
from tkinter.ttk import Combobox
from tkinter.ttk import Label
from tkinter.ttk import Treeview

from tkcalendar import DateEntry
from ttkthemes import ThemedTk

from telegram_explorer import Settings
from telegram_explorer.gui.forms import FormResult
from telegram_explorer.gui.forms import LoginForm
from telegram_explorer.gui.forms import SettingsForm
from telegram_explorer.telegram import Chat
from telegram_explorer.telegram import Message
from telegram_explorer.telegram import TelegramClient


class Application(ThemedTk):
    def __init__(self, loop: AbstractEventLoop, interval: float = 1 / 120) -> None:
        super().__init__(theme="clearlooks", themebg=True)

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title("Telegram Explorer")
        self.resizable(False, False)

        self._settings = Settings.load_default()
        self._setup_layout()

        self._loop = loop
        self._running = True
        self._gui = loop.create_task(self._run_gui(interval), name="gui-loop")

        self._loop.create_task(self._get_chats_list())

    def close(self) -> None:
        self._running = False
        self._loop.create_task(self._shutdown(), name="shutdown")

    def start(self) -> None:
        """Run application main loop."""
        self._loop.run_forever()

    async def _run_gui(self, interval: float) -> None:
        while self._running:
            self.update()
            await sleep(interval)

    async def _shutdown(self) -> None:
        self._loop.stop()
        self.destroy()

    def _setup_layout(self) -> None:
        # Chat
        Label(self, text="Chat:").grid(row=0, column=0, sticky="ewns", padx=5, pady=5)
        Combobox(self).grid(row=0, column=1, columnspan=3, sticky="ewns", padx=5, pady=5)

        # Dates
        Label(self, text="Start Date:").grid(row=1, column=0, sticky="ewns", padx=5, pady=5)
        DateEntry(self).grid(row=1, column=1, sticky="ewns", padx=5, pady=5)

        Label(self, text="End Date:").grid(row=1, column=2, sticky="ens", padx=5, pady=5)
        DateEntry(self).grid(row=1, column=3, sticky="ewns", padx=5, pady=5)

        # Settings Button
        settings_button = Button(self, text="Settings", command=self._show_settings)
        settings_button.grid(row=2, column=0, sticky="ewns", padx=5, pady=5)

        # Download Button
        download_button = Button(self, text="Download History", command=self._request_download_history)
        download_button.grid(row=2, column=3, columnspan=1, sticky="ewns", padx=5, pady=5)

        # Messages
        columns = ("id", "date", "author", "text")
        messages = Treeview(self, columns=columns, show="headings")
        for col in columns:
            messages.heading(col, text=col)
            messages.column(col, width=100, stretch=False)
        messages.column("text", width=100, stretch=True)

        for i in range(12):
            messages.insert("", "end", values=(i, i) + ("aaaa", "bbbb"))

        messages.grid(row=3, column=0, columnspan=4, sticky="ewns", padx=5, pady=5)

    def _show_settings(self) -> None:
        form = SettingsForm(self, self._settings)
        form.show_modal()

    def _request_download_history(self) -> None:
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

        chat = "me"  # TODO: get the Chat object by the `Chat` combobox value
        date_from = date.min  # TODO: get date from `Start Date` date entry value
        date_to = date.today()  # TODO: get date from `End Date` date entry value

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
        # TODO: (re)fill chat combobox here
        print(chats)

    async def _fill_messages_grid(self, history: list[Message]) -> None:
        # TODO: (re)fill messages grid here
        print(history)


def run() -> None:
    loop = get_event_loop()
    app = Application(loop)
    app.start()


if __name__ == "__main__":
    run()
