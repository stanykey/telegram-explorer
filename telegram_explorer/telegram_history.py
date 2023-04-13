from datetime import datetime
from pathlib import Path

from click import argument
from click import command
from click import DateTime
from click import option
from pyrogram import Client


def get_session_dir() -> Path:
    root = Path.home() / ".telegram-explorer"
    root.mkdir(parents=True, exist_ok=True)
    return root


@command()
@argument("api-id", type=int)
@argument("api-hash", type=str)
@option("--chat", type=str, help="Chat name or id")
@option("-s", "--start", type=DateTime(formats=["%d.%m.%Y"]), default="", help="Start date")
@option("-e", "--end", type=DateTime(formats=["%d.%m.%Y"]), default="", help="End date")
def cli(api_id: int, api_hash: str, chat: str, start: datetime, end: datetime) -> None:
    session_dir = get_session_dir()
    client = Client("telegram-history", api_id, api_hash, workdir=str(session_dir), hide_password=True)
    with client:
        grabber = client.get_chat_history(chat_id=chat, limit=0, offset_date=end)
        history = [msg for msg in grabber if msg.date.timestamp() >= start.timestamp()]
        for message in history:
            print(message.date, message.author_signature, message.text)


if __name__ == "__main__":
    cli()
