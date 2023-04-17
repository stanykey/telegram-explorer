from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from asyncio import sleep
from tkinter import messagebox
from tkinter.ttk import Button
from tkinter.ttk import Combobox
from tkinter.ttk import Label
from tkinter.ttk import Treeview

from tkcalendar import DateEntry
from ttkthemes import ThemedTk

from telegram_explorer import Settings
from telegram_explorer.gui.forms import SettingsForm


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
        download_button = Button(self, text="Download History", command=self._download_history)
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

    @staticmethod
    def _download_history() -> None:
        messagebox.showinfo(message="Download History Placeholder")


def run() -> None:
    loop = get_event_loop()
    app = Application(loop)
    app.start()


if __name__ == "__main__":
    run()
