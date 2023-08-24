import re
from typing import Optional

from scripts.am.config import Route as ConfigRoute
from .route import Route
from scripts.am.label.parser import MatcherTypeEnum, Matcher, parse_matchers


def convert_to_validator_route(
    config_routes: list[Optional["ConfigRoute"]], parent_route=None
) -> list[Optional["Route"]]:
    results = []
    for config_route in config_routes:
        if config_route:
            legacy_equal_matchers = []
            legacy_regexp_matchers = []
            for key, value in config_route.match.items():
                legacy_equal_matchers.append(
                    Matcher(MatcherTypeEnum.MatchEqual, key, value)
                )
            for key, value in config_route.match_re.items():
                legacy_regexp_matchers.append(
                    Matcher(MatcherTypeEnum.MatchRegex, key, value, re.compile(value))
                )
            matchers = []
            for item in config_route.matchers:
                matchers.append(*parse_matchers(item))
            new_route = Route(
                config_route.receiver,
                legacy_equal_matchers + legacy_regexp_matchers + matchers,
                continue_=config_route.continue_,
                routes=[],
                parent_route=parent_route,
            )
            new_route.routes = convert_to_validator_route(
                config_route.routes, new_route
            )
            results.append(new_route)

    return results
