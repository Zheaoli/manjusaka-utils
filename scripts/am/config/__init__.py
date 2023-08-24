from typing import Any, Optional

from pydantic import BaseModel, Field


class Route(BaseModel):
    receiver: str = Field(alias="receiver", default="")
    group_by_str: list[str] = []
    match: dict[str, str] = {}
    match_re: dict[str, str] = {}
    matchers: list[str] = []
    mute_time_intervals: list[str] = []
    active_time_intervals: list[str] = []
    continue_: bool = Field(alias="continue", default=False)
    routes: list[Optional["Route"]] = []
    group_wait: Optional[Any] = None
    group_interval: Optional[Any] = None
    repeat_interval: Optional[Any] = None
