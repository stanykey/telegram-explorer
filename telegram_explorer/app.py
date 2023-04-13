from asyncio import AbstractEventLoop
from asyncio import get_event_loop
from asyncio import sleep
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import Tk


class Application(Tk):
    def __init__(self, loop: AbstractEventLoop, interval: float = 1 / 120) -> None:
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title("Telegram Explorer")

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

    def download_history(self) -> None:
        """Download Telegram Chat/Channel history."""
        pass

    def _setup_layout(self) -> None:
        # API Keys
        Label(self, text="API ID:").grid(row=0, column=0)
        self.api_id_entry = Entry(self)
        self.api_id_entry.grid(row=0, column=1)
        Label(self, text="API Hash:").grid(row=1, column=0)
        self.api_hash_entry = Entry(self)
        self.api_hash_entry.grid(row=1, column=1)

        # Phone Number
        Label(self, text="Phone Number:").grid(row=2, column=0)
        self.phone_number_entry = Entry(self)
        self.phone_number_entry.grid(row=2, column=1)

        # Entity
        Label(self, text="Chat/Channel ID:").grid(row=3, column=0)
        self.entity_entry = Entry(self)
        self.entity_entry.grid(row=3, column=1)

        # Dates
        Label(self, text="Start Date:").grid(row=4, column=0)
        self.start_date = Entry(self)
        self.start_date.grid(row=4, column=1)
        Label(self, text="End Date:").grid(row=5, column=0)
        self.end_date = Entry(self)
        self.end_date.grid(row=5, column=1)

        # Download Button
        self.download_button = Button(self, text="Download History", command=self.download_history)
        self.download_button.grid(row=6, column=1)

    async def _run_gui(self, interval: float) -> None:
        while self._running:
            self.update()
            await sleep(interval)

    async def _shutdown(self) -> None:
        self._loop.stop()
        self.destroy()


def run() -> None:
    loop = get_event_loop()
    app = Application(loop)
    app.start()


if __name__ == "__main__":
    run()
