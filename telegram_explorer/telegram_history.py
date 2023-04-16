from datetime import date
from datetime import datetime
from datetime import timezone

from click import argument
from click import command
from click import option
from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Chat

from telegram_explorer import Settings
from telegram_explorer import settings_file
from telegram_explorer.misc.asyncio import execute_synchronously
from telegram_explorer.misc.cli import Date


def get_settings(api: tuple[int, str]) -> Settings:
    """Get settings in some 'weird' way."""
    if len(api) == 2:
        return Settings(api_id=api[0], api_hash=api[1])

    return Settings.load(settings_file())


def make_telegram_client(config: Settings, /) -> Client:
    """Simple factory method."""
    return Client(
        name="telegram-history",
        api_id=config.api_id,
        api_hash=config.api_hash,
        workdir=str(config.get_session_dir()),
        hide_password=True,
    )


async def find_chat_by(name: str, config: Settings) -> Chat | None:
    """Try to get **chat id** by username or chat title."""
    client = make_telegram_client(config)
    async with client:
        async for dialog in client.get_dialogs():
            chat = dialog.chat
            match chat.type:
                case ChatType.PRIVATE:
                    if chat.username == name:
                        return chat

                    full_name = " ".join(text for text in (chat.first_name, chat.last_name) if text)
                    if full_name == name:
                        return chat

                case ChatType.GROUP | ChatType.CHANNEL:
                    if name == chat.title:
                        return chat
    return None


async def get_telegram_history(config: Settings, chat_name: str, date_from: date, date_to: date) -> None:
    """Receive and print history for `chat` by particular criteria."""
    chat = await find_chat_by(chat_name, config)
    if chat is None:
        return

    date_from = datetime.combine(date_from, datetime.min.time(), timezone.utc)
    date_to = datetime.combine(date_to, datetime.min.time(), timezone.utc)

    client = make_telegram_client(config)
    async with client:
        grabber = client.get_chat_history(chat.id, offset_date=date_to)
        start_offset = date_from.timestamp()
        history = [msg async for msg in grabber if msg.date.timestamp() >= start_offset]

    for message in history:
        print(message.date, message.author_signature, message.text)


@command()
@argument("api", type=tuple[int, str], default=tuple())
@option("--chat", type=str, required=True, help="Chat or user name")
@option("-s", "--date-from", type=Date(), default=date.min, help="Start date  [default: epoch]")
@option("-e", "--date-to", type=Date(), default=date.today(), help="End date    [default: today]")
def cli(api: tuple[int, str], chat: str, date_from: date, date_to: date) -> None:
    """
    The application obtains and prints the history of a particular `chat`.

    If the **API** arguments are omitted then the application tries to read them from settings from the default location
    (~/.telegram- explorer/settings.json)
    """
    config = get_settings(api)
    task = get_telegram_history(config, chat, date_from, date_to)
    execute_synchronously(task)


if __name__ == "__main__":
    cli()
