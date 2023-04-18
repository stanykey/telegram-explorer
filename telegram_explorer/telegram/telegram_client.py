"""Simple wrapper around Pyrogam.Client class."""
from datetime import date
from datetime import datetime
from datetime import timezone
from pathlib import Path

from pyrogram import Client
from pyrogram.types import Chat
from pyrogram.types import Message


class TelegramClient:
    """Class to download Telegram chat/channel history."""

    def __init__(self, name: str, api_id: int, api_hash: str, phone_number: str, session_dir: Path) -> None:
        self._client = Client(name, api_id, api_hash, phone_number=phone_number, workdir=str(session_dir))

    async def is_authorized(self) -> bool:
        """Check authorization status."""
        authorized: bool = await self._client.connect()
        await self._client.disconnect()
        return authorized

    async def get_chats(self) -> list[Chat]:
        """Get the list of all chats for a particular account."""
        async with self._client:
            return [dialog.chat async for dialog in self._client.get_dialogs()]

    async def download_history(self, chat: str | Chat, date_from: date, date_to: date) -> list[Message]:
        """Get the conversation history for the particular chat for the specific period."""
        date_from = datetime.combine(date_from, datetime.min.time(), timezone.utc)
        date_to = datetime.combine(date_to, datetime.min.time(), timezone.utc)

        chat_id = chat if isinstance(chat, str) else chat.id
        async with self._client:
            grabber = self._client.get_chat_history(chat_id, offset_date=date_to)
            start_offset = date_from.timestamp()
            return [msg async for msg in grabber if msg.date.timestamp() >= start_offset]
