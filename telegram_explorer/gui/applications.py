"""Contain definitions of applications with GUI."""
from telegram_explorer.gui.core.misc import get_event_loop
from telegram_explorer.gui.core.runner import AsyncRunner
from telegram_explorer.gui.core.runner import Runner
from telegram_explorer.gui.forms import LoginForm
from telegram_explorer.gui.forms import SettingsForm
from telegram_explorer.gui.main_window import MainWindow


def make_application_runner(title: str, *, asynchronous: bool = False) -> Runner:
    """Create application runner."""
    if not asynchronous:
        return Runner(title, theme="clearlooks")

    return AsyncRunner(title, theme="clearlooks", loop=get_event_loop())


def run_settings_editor() -> None:
    """Run settings form as the standalone application."""
    app = make_application_runner("Telegram Explorer Settings")
    settings_window = SettingsForm(app, app.settings)
    app.start(settings_window)


def run_session_creator() -> None:
    """Run login form as the standalone application."""
    app = make_application_runner("Telegram Session Creator", asynchronous=True)
    login_form = LoginForm(app, app.settings, app.loop)
    app.start(login_form)


def run_telegram_explorer() -> None:
    app = make_application_runner("Telegram Explorer", asynchronous=True)
    window = MainWindow(app, app.settings, app.loop)
    app.start(window)
