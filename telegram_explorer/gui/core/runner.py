"""Contain (async)runner for Tk-based applications."""
from asyncio import AbstractEventLoop
from asyncio import sleep
from tkinter import TclError
from tkinter import Toplevel

from ttkthemes.themed_tk import ThemedTk

from telegram_explorer import Settings
from telegram_explorer.gui.core.misc import centralize_window
from telegram_explorer.gui.core.misc import get_event_loop


class Runner(ThemedTk):
    """Allow to run Tkinter applications with asyncio."""

    def __init__(self, name: str, *, theme: str) -> None:
        super().__init__(theme=theme, themebg=True, toplevel=True)
        self.title(name)
        self.protocol("WM_DELETE_WINDOW", self.stop)

        self.overrideredirect(True)
        centralize_window(self)
        self.update()
        self.withdraw()

        self._settings = Settings.load_default()

    @property
    def settings(self) -> Settings:
        """Provide application settings."""
        return self._settings

    @property
    def loop(self) -> AbstractEventLoop:
        return get_event_loop()

    def start(self, window: Toplevel) -> None:
        """Run application main loop."""
        centralize_window(window)
        self.wait_window(window)
        self.stop()

    def stop(self) -> None:
        """Stop the application execution."""
        self.destroy()


class AsyncRunner(Runner):
    """Allow to run Tkinter applications with asyncio."""

    def __init__(self, name: str, *, theme: str, loop: AbstractEventLoop, interval: float = 1 / 120) -> None:
        super().__init__(name, theme=theme)

        self._update_interval = interval
        self._loop = loop
        self._running = False

    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop

    def start(self, window: Toplevel) -> None:
        """Run application main loop."""
        self._running = True
        self._loop.create_task(self._run_gui(window), name="gui-loop")
        self._loop.run_forever()

    def stop(self) -> None:
        """Request to stop execution scheduling task in the loop."""
        self._running = False
        self._loop.create_task(self._shutdown(), name="shutdown")

    async def _run_gui(self, window: Toplevel) -> None:
        centralize_window(window)
        while self._running:
            try:
                window.winfo_id()  # Will throw TclError if the window is destroyed
            except TclError:
                self.stop()

            self.update()
            await sleep(self._update_interval)

    async def _shutdown(self) -> None:
        self._loop.stop()
        self.destroy()
