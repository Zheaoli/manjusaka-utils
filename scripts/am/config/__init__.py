from typing import Any, Optional

from pydantic import BaseModel, Field


class Route(BaseModel):
    receiver: Any
    group_by_str: Any
    match: dict[str, str]
    match_re: dict[str, str]
    matchers: list[str]
    mute_time_intervals: list[str]
    active_time_intervals: list[str]
    continue_: bool = Field(alias="continue")
    routes: list[Optional["Route"]]
    group_wait: Any
    group_interval: Any
    repeat_interval: Any
