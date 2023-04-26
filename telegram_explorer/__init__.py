"""
The package is a small toolset to explore Telegram-related stuff.

Also, contain the definition of package settings and related stuff.
"""
from dataclasses import dataclass
from json import dump
from json import load
from pathlib import Path
from typing import Any
from typing import Self


def settings_directory() -> Path:
    """Return root settings directory path."""
    return Path.home() / ".telegram-explorer"


def settings_file() -> Path:
    """Return settings file path."""
    return settings_directory() / "settings.json"


@dataclass(slots=True, kw_only=True)
class Settings:
    session_name: str
    api_id: int
    api_hash: str
    phone_number: str = ""
    path: Path = settings_file()

    def get_session_dir(self) -> Path:
        """Return the settings parent directory, and ensure it exists."""
        working_dir = self.path.parent
        if not working_dir.exists():
            working_dir.mkdir(parents=True, exist_ok=True)
        return working_dir

    @classmethod
    def load(cls, path: Path) -> Self:
        """Load settings from the `path`."""
        if not path.is_file():
            raise ValueError(f"path ({path}) is not a file.")

        with open(path, encoding="utf-8") as file:
            raw_settings: dict[str, Any] = load(file)

        return cls(
            session_name=raw_settings.get("session_name", "telegram-explorer"),
            path=path,
            api_id=int(raw_settings.get("api_id", 0)),
            api_hash=raw_settings.get("api_hash", ""),
            phone_number=raw_settings.get("phone_number", ""),
        )

    @classmethod
    def load_default(cls) -> Self:
        """Load settings from the default settings location."""
        return cls.load(settings_file())

    def save(self) -> None:
        """Save setting into the file at the `self.path`."""
        path = self.path if not self.path.exists() else self.path.with_suffix(".new")

        data = dict(session_name=self.session_name, api_id=self.api_id, api_hash=self.api_hash)
        if self.phone_number:
            data["phone_number"] = self.phone_number

        with open(path, "w", encoding="utf-8") as file:
            dump(data, file, indent=4)

        if path is not self.path:
            path.replace(self.path)
