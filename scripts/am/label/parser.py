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

    def __str__(self):
        return f"{self.name} {self.type.name} {self.value}"


@dataclass
class Label:
    name: str
    value: str


matcher_regex = re.compile(r"^\s*([a-zA-Z_:][a-zA-Z0-9_:]*)\s*(=~|=|!=|!~)\s*(.*?)\s*$")
type_map = {
    "=": MatcherTypeEnum.MatchEqual,
    "!=": MatcherTypeEnum.MatchNotEqual,
    "=~": MatcherTypeEnum.MatchRegex,
    "!~": MatcherTypeEnum.MatchNotRegex,
}


# NewMatcher function (used for creating Matcher objects)
def new_matcher(match_type: MatcherTypeEnum, label: str, value: str) -> Matcher:
    regex_pattern = None
    if match_type in [MatcherTypeEnum.MatchRegex, MatcherTypeEnum.MatchNotRegex]:
        regex_pattern = re.compile(value)
    return Matcher(match_type, label, value, regex_pattern)


# parse_matcher function
def parse_matcher(s: str) -> Optional["Matcher"]:
    match = matcher_regex.match(s)
    if not match:
        return None, f"bad matcher format: {s}"

    raw_value = match.group(3)
    value = []
    escaped = False
    expect_trailing_quote = False

    if raw_value.startswith('"'):
        raw_value = raw_value[1:]
        expect_trailing_quote = True

    if not raw_value.isascii():
        raise ValueError(f"matcher value not ASCII: {raw_value}")

    # Unescape the raw value
    for i, char in enumerate(raw_value):
        if escaped:
            escaped = False
            if char == "n":
                value.append("\n")
            elif char in ['"', "\\"]:
                value.append(char)
            else:
                value.extend(["\\", char])
            continue

        if char == "\\":
            if i < len(raw_value) - 1:
                escaped = True
                continue
            value.append("\\")
        elif char == '"':
            if not expect_trailing_quote or i < len(raw_value) - 1:
                raise ValueError(
                    f"matcher value contains unescaped double quote: {raw_value}"
                )
            expect_trailing_quote = False
        else:
            value.append(char)

    if expect_trailing_quote:
        raise ValueError(f"matcher value contains unescaped double quote: {raw_value}")

    return new_matcher(type_map[match.group(2)], match.group(1), "".join(value))


# parse_matchers function
def parse_matchers(s: str) -> list[Matcher]:
    matchers = []
    s = s.lstrip("{").rstrip("}")

    inside_quotes = False
    escaped = False
    token = []
    tokens = []

    for char in s:
        if char == "," and not inside_quotes:
            tokens.append("".join(token))
            token.clear()
            continue
        elif char == '"':
            if not escaped:
                inside_quotes = not inside_quotes
            else:
                escaped = False
        elif char == "\\":
            escaped = not escaped
        else:
            escaped = False
        token.append(char)

    if token:
        tokens.append("".join(token))

    for token in tokens:
        matchers.append(parse_matcher(token))

    return matchers
