""""""
import asyncio
from datetime import datetime
from os import environ
from typing import Any
from typing import Self

from pyrogram import Client
from pyrogram.types import Message


class TelegramClient:
    """Class to download Telegram chat/channel history."""

    def __init__(self, api_id: int, api_hash: str, phone_number: str) -> None:
        self._api_id = api_id
        self._api_hash = api_hash
        self._phone_number = phone_number
        self._session_name = self._phone_number + ".session"
        self._app = Client(self._session_name, self._api_id, self._api_hash, phone_number=self._phone_number)

    async def __aenter__(self) -> Self:
        """Start the Telegram client."""
        await self._app.start()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Stop the Telegram client."""
        await self._app.stop()

    async def download_history(self, entity: str, start_date: datetime, end_date: datetime) -> list[Message]:
        """Download the history of a chat/channel for a given period of time."""
        grabber = self._app.get_chat_history(chat_id=entity, limit=0, offset_date=end_date)
        return [msg async for msg in grabber if msg.date.timestamp() >= start_date.timestamp()]


async def test_main() -> None:
    api_id = int(environ["API_ID"])
    api_hash = environ["API_HASH"]
    phone_number = environ["PHONE_NUMBER"]
    async with TelegramClient(api_id, api_hash, phone_number) as client:
        start_date = datetime(year=2022, month=1, day=4)
        end_date = datetime(year=2023, month=2, day=5)
        for message in await client.download_history("me", start_date, end_date):
            print(message.text)


if __name__ == "__main__":
    asyncio.run(test_main())
