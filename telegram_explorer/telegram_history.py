from datetime import datetime
from pathlib import Path

from click import argument
from click import command
from click import DateTime
from click import option
from pyrogram import Client

from telegram_explorer import Settings
from telegram_explorer import settings_directory
from telegram_explorer import settings_file


def get_settings(api: tuple[int, str], path: Path) -> Settings:
    if len(api) == 2:
        return Settings(api_id=api[0], api_hash=api[1])

    return Settings.load(path)


def get_session_dir() -> Path:
    """Return the settings root directory, but ensure it exists."""
    root = settings_directory()
    root.mkdir(parents=True, exist_ok=True)
    return root


@command()
@argument("api", type=tuple[int, str], default=tuple())
@option("--chat", type=str, help="Chat name or id")
@option("-s", "--start", type=DateTime(formats=["%d.%m.%Y"]), default="", help="Start date")
@option("-e", "--end", type=DateTime(formats=["%d.%m.%Y"]), default="", help="End date")
def cli(api: tuple[int, str], chat: str, start: datetime, end: datetime) -> None:
    config = get_settings(api, settings_file())
    session_dir = get_session_dir()
    client = Client("telegram-history", config.api_id, config.api_hash, workdir=str(session_dir), hide_password=True)
    with client:
        grabber = client.get_chat_history(chat_id=chat, limit=0, offset_date=end)
        history = [msg for msg in grabber if msg.date.timestamp() >= start.timestamp()]
        for message in history:
            print(message.date, message.author_signature, message.text)


if __name__ == "__main__":
    cli()
