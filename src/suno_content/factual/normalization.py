from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

_NUMBER_RE = re.compile(r"(?<![\w])[-+]?(?:\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?)(?![\w])")
_PERCENT_RE = re.compile(r"([-+]?\d+(?:[.,]\d+)?)\s*%")
_PERIOD_RE = re.compile(r"\b(?:[1-4]T\d{2,4}|[12]S\d{2,4}|20\d{2}|19\d{2})\b", re.IGNORECASE)
_DATE_RE = re.compile(r"\b(?:\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})\b")
_SCALE_WORDS = {
    "mil": Decimal("1000"),
    "milhao": Decimal("1000000"),
    "milhoes": Decimal("1000000"),
    "bilhao": Decimal("1000000000"),
    "bilhoes": Decimal("1000000000"),
    "trilhao": Decimal("1000000000000"),
    "trilhoes": Decimal("1000000000000"),
}
_DIRECTION_GROUPS = {
    "UP": {"subiu", "aumentou", "cresceu", "avancou", "expandiu", "alta"},
    "DOWN": {"caiu", "reduziu", "diminuiu", "recuou", "contraiu", "queda"},
    "STABLE": {"manteve", "estavel", "estabilidade"},
}
_MODALITY = {"estima", "estimativa", "espera", "esperado", "pode", "podera", "previsto", "preve", "possivel", "possibilidade", "sujeito", "condicionado", "condicionada"}


@dataclass(frozen=True)
class NumericValue:
    value: Decimal
    surface: str
    percent: bool = False


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.lower()).strip()


def parse_decimal(surface: str) -> Decimal:
    value = surface.strip().replace(" ", "")
    if "," in value and "." in value:
        value = value.replace(".", "").replace(",", ".")
    elif "," in value:
        value = value.replace(",", ".")
    return Decimal(value)


def extract_numbers(text: str) -> tuple[NumericValue, ...]:
    percent_spans = {m.span(1) for m in _PERCENT_RE.finditer(text)}
    values: list[NumericValue] = []
    for match in _NUMBER_RE.finditer(text):
        surface = match.group(0)
        left = text[max(0, match.start() - 1):match.start()]
        right = text[match.end():match.end() + 1]
        if left.upper() == "T" or right.upper() == "T":
            continue
        try:
            value = parse_decimal(surface)
        except Exception:
            continue
        pct = any(a <= match.start() and match.end() <= b for a, b in percent_spans)
        values.append(NumericValue(value=value, surface=surface, percent=pct))
    return tuple(values)


def extract_percentages(text: str) -> tuple[Decimal, ...]:
    return tuple(parse_decimal(m.group(1)) for m in _PERCENT_RE.finditer(text))


def extract_periods(text: str) -> tuple[str, ...]:
    return tuple(m.group(0).upper() for m in _PERIOD_RE.finditer(text))


def extract_dates(text: str) -> tuple[str, ...]:
    return tuple(m.group(0) for m in _DATE_RE.finditer(text))


def extract_scale_words(text: str) -> tuple[str, ...]:
    normalized = fold(text)
    found: list[str] = []
    for word in _SCALE_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", normalized):
            found.append(word)
    return tuple(found)


def extract_direction(text: str) -> str | None:
    normalized = fold(text)
    for direction, words in _DIRECTION_GROUPS.items():
        if any(re.search(rf"\b{re.escape(word)}\b", normalized) for word in words):
            return direction
    return None


def has_negation(text: str) -> bool:
    normalized = fold(text)
    return bool(re.search(r"\bnao\b", normalized))


def has_modality(text: str) -> bool:
    normalized = fold(text)
    return any(re.search(rf"\b{re.escape(word)}\b", normalized) for word in _MODALITY)


def has_explicit_range(text: str) -> bool:
    normalized = fold(text)
    return bool(re.search(r"\bentre\s+[-+]?\d+(?:[.,]\d+)?\s*%?\s+e\s+[-+]?\d+(?:[.,]\d+)?\s*%?", normalized))


def round_half_up(value: Decimal, decimals: int) -> Decimal:
    quantum = Decimal("1").scaleb(-decimals)
    return value.quantize(quantum, rounding=ROUND_HALF_UP)
