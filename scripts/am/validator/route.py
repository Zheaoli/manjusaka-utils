import enum
import re
from dataclasses import dataclass
from typing import Optional


class MatcherTypeEnum(enum.IntEnum):
    MatchEqual = 0
    MatchNotEqual = 1
    MatchRegex = 2
    MatchNotRegex = 3


@dataclass
class Matcher:
    type: MatcherTypeEnum
    name: str
    value: str
    regex: Optional[re.Pattern] = None

    def match(self, value: str) -> bool:
        match self.type:
            case MatcherTypeEnum.MatchEqual:
                return self.value == value
            case MatcherTypeEnum.MatchNotEqual:
                return self.value != value
            case MatcherTypeEnum.MatchRegex:
                return bool(self.regex.match(value))
            case MatcherTypeEnum.MatchNotRegex:
                return not bool(self.regex.match(value))
        raise ValueError(f"Unknown matcher type: {self.type}")


@dataclass
class Label:
    name: str
    value: str


@dataclass
class Route:
    receiver: str
    matchers: list[Matcher]
    continue_: bool
    routes: list["Route"]
    parent_route: Optional["Route"] = None

    def match(self, labels: list[Label]) -> list[Optional["Route"]]:
        if not self._match(labels):
            return []
        results = []
        for route in self.routes:
            flag = route.match(labels)
            results.append(route)
            if flag and not route.continue_:
                break
        if not results:
            results.append(self.parent_route)
        return results

    def _match(self, labels: list[Label]) -> True:
        for matcher in self.matchers:
            for label in labels:
                if label.name == matcher.name and matcher.match(label.value):
                    break
            else:
                return False
        return True
