"""Set of CLI helpers (mostly related to the click package)."""
from datetime import date
from datetime import datetime

from click import BadParameter
from click import Context
from click import Parameter
from click import ParamType


class Date(ParamType):  # type: ignore
    name = "date"

    def __init__(self) -> None:
        self._format = "%d.%m.%Y"

    def get_metavar(self, param: Parameter) -> str:
        return f"[{self._format}]"

    def convert(self, value: str | date, param: Parameter | None, ctx: Context | None) -> date:
        if isinstance(value, date):
            return value

        if parsed := self._try_to_convert_date(date_string=value):
            return parsed

        raise BadParameter(f"invalid date format: {value}. (choose from {self._format})", ctx=ctx, param=param)

    def _try_to_convert_date(self, date_string: str) -> date | None:
        try:
            return datetime.strptime(date_string, self._format).date()
        except ValueError:
            return None
