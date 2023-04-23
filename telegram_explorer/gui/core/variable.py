"""Contain implementations of the `Variable` protocol allowing bind values for the Tkinter controls."""
from datetime import date
from tkinter import BaseWidget
from tkinter import Tk
from tkinter import Variable


class DateVar(Variable):
    """Value holder for strings variables."""

    def __init__(self, master: Tk | BaseWidget, value: str | date | None = None, *, name: str | None = None) -> None:
        super().__init__(master, value, name)

    def set(self, value: str | date) -> None:
        super().set(value)

    def get(self) -> date:
        """Return value of variable as date."""
        value = super().get()  # type: ignore
        if isinstance(value, date):
            return value

        try:
            return date.fromisoformat(value)
        except ValueError:
            day, month, year = tuple(map(int, value.split(".")))
            return date(year, month, day)
