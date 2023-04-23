"""Contain definitions of applications with GUI."""
from telegram_explorer.gui.core.misc import get_event_loop
from telegram_explorer.gui.core.runner import AsyncRunner
from telegram_explorer.gui.core.runner import Runner
from telegram_explorer.gui.forms import SettingsForm
from telegram_explorer.gui.main_window import MainWindow


def run_settings_editor() -> None:
    """Run settings form as the standalone application."""
    app = Runner("Telegram Explorer Settings", theme="clearlooks")
    settings_window = SettingsForm(app, app.settings)
    app.start(settings_window)


def run_session_creator() -> None:
    """Run login form as the standalone application."""
    pass


def run_telegram_explorer() -> None:
    app = AsyncRunner("Telegram Explorer", theme="clearlooks", loop=get_event_loop())
    window = MainWindow(app, app.settings, app.loop)
    app.start(window)
