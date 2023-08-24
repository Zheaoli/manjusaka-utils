from dataclasses import dataclass
from typing import Optional

from scripts.am.label.parser import Label, Matcher


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

    def __str__(self):
        return f"receiver: {self.receiver}"
