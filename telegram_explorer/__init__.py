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
    api_id: int
    api_hash: str
    path: Path = settings_file()

    def __post_init__(self) -> None:
        """We just want to do some minimal validation."""
        if not self._validate_api():
            raise ValueError("Settings initialized with wrong values")

    def get_session_dir(self) -> Path:
        """Return the settings parent directory, and ensure it exists."""
        working_dir = self.path.parent
        if not working_dir.exists():
            working_dir.mkdir(parents=True, exist_ok=True)
        return working_dir

    @classmethod
    def load(cls, path: Path) -> Self:
        if not path.is_file():
            raise ValueError(f"path ({path}) is not a file.")

        with open(path, encoding="utf-8") as file:
            raw_settings: dict[str, Any] = load(file)

        return cls(path=path, api_id=int(raw_settings.get("api_id", 0)), api_hash=raw_settings.get("api_hash", ""))

    def save(self) -> None:
        path = self.path if not self.path.exists() else self.path.with_suffix(".new")

        data = dict(api_id=self.api_id, api_hash=self.api_hash)
        with open(path, "w", encoding="utf-8") as file:
            dump(data, file, indent=4)

        if path is not self.path:
            path.replace(self.path)

    def _validate_api(self) -> bool:
        return bool(self.api_id) and bool(self.api_hash)
