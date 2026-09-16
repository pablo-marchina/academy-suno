from __future__ import annotations

import re
import unicodedata

from suno_content.domain import OutputFormat

from .models import READABILITY_VERSION, ReadabilityResult

MIN_SYLLABLE_COVERAGE = 0.95

_URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_HTML_RE = re.compile(r"<[^>]+>")
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_TIMESTAMP_RE = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")
_STRUCTURAL_PREFIX_RE = re.compile(
    r"(?im)^\s*(?:slide|card|cena|scene|bloco|frame)\s*#?\d+\s*[:.\-–—]?\s*"
)
_TOKEN_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:-[A-Za-zÀ-ÖØ-öø-ÿ]+)*|\d+(?:[.,]\d+)*(?:%|º|ª)?"
)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")
_VOWEL_GROUP_RE = re.compile(r"[aeiouyáéíóúâêôãõàü]+", re.IGNORECASE)

_ACRONYM_SYLLABLES = {
    "IPCA": 4,
    "CDI": 3,
    "CVM": 3,
    "COPOM": 2,
    "SELIC": 2,
    "EBITDA": 3,
    "LAJIDA": 3,
    "CAPEX": 2,
}


def normalize_linguistic_text(text: str, output_format: OutputFormat) -> str:
    """Remove presentation metadata while preserving linguistic content."""
    normalized = _MD_LINK_RE.sub(r"\1", text)
    normalized = _URL_RE.sub(" ", normalized)
    normalized = _HTML_RE.sub(" ", normalized)
    normalized = _TIMESTAMP_RE.sub(" ", normalized)
    if output_format in {OutputFormat.CAROUSEL, OutputFormat.SHORT_VIDEO}:
        normalized = _STRUCTURAL_PREFIX_RE.sub("", normalized)
    normalized = normalized.replace("•", "\n").replace("▪", "\n")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n[ \t]+", "\n", normalized)
    return normalized.strip()


def lexical_tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text)


def segment_sentences(text: str) -> list[str]:
    pieces = [piece.strip(" \t-*–—") for piece in _SENTENCE_SPLIT_RE.split(text)]
    return [piece for piece in pieces if lexical_tokens(piece)]


def count_syllables_ptbr(token: str) -> int | None:
    """Deterministic heuristic syllable counter with explicit unsupported cases."""
    clean = token.strip("-–—")
    if not clean or any(char.isdigit() for char in clean):
        return None
    upper = clean.upper()
    if upper in _ACRONYM_SYLLABLES:
        return _ACRONYM_SYLLABLES[upper]
    if clean.isupper() and 2 <= len(clean) <= 8:
        return None

    total = 0
    for part in clean.split("-"):
        if not part:
            continue
        groups = _VOWEL_GROUP_RE.findall(part)
        if not groups:
            return None
        total += max(1, len(groups))
    return total or None


def evaluate_readability(
    text: str,
    output_format: OutputFormat,
    *,
    min_syllable_coverage: float = MIN_SYLLABLE_COVERAGE,
) -> ReadabilityResult:
    normalized = normalize_linguistic_text(text, output_format)
    sentences = segment_sentences(normalized)
    tokens = lexical_tokens(normalized)

    sentence_lengths = [len(lexical_tokens(sentence)) for sentence in sentences]
    sentence_count = len(sentences)
    word_count = len(tokens)
    words_per_sentence = word_count / sentence_count if sentence_count else None

    syllable_counts: list[int] = []
    unsupported: list[str] = []
    for token in tokens:
        count = count_syllables_ptbr(token)
        if count is None:
            unsupported.append(token)
        else:
            syllable_counts.append(count)

    supported = len(syllable_counts)
    coverage = supported / word_count if word_count else 0.0
    syllables_per_word = sum(syllable_counts) / supported if supported else None
    valid = bool(
        sentence_count
        and word_count
        and syllables_per_word is not None
        and coverage >= min_syllable_coverage
    )
    flesch_raw = None
    if valid and words_per_sentence is not None:
        flesch_raw = 248.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word

    short_ratio = (
        sum(length <= 3 for length in sentence_lengths) / sentence_count if sentence_count else 0.0
    )
    long_ratio = (
        sum(length >= 30 for length in sentence_lengths) / sentence_count if sentence_count else 0.0
    )
    fragment_count = 0
    for sentence in sentences:
        if len(lexical_tokens(sentence)) <= 4 and not re.search(r"[.!?]\s*$", sentence):
            fragment_count += 1
    fragment_ratio = fragment_count / sentence_count if sentence_count else 0.0

    return ReadabilityResult(
        version=READABILITY_VERSION,
        format=output_format,
        flesch_raw=round(flesch_raw, 6) if flesch_raw is not None else None,
        words_per_sentence=round(words_per_sentence, 6) if words_per_sentence is not None else None,
        syllables_per_word=round(syllables_per_word, 6) if syllables_per_word is not None else None,
        sentence_count=sentence_count,
        word_count=word_count,
        supported_syllable_tokens=supported,
        syllable_coverage=round(coverage, 6),
        unsupported_tokens=tuple(dict.fromkeys(unsupported)),
        very_short_sentence_ratio=round(short_ratio, 6),
        very_long_sentence_ratio=round(long_ratio, 6),
        fragment_ratio=round(fragment_ratio, 6),
        valid=valid,
    )
