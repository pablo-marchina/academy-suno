from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .models import ConceptMention, FinancialConcept, FinancialOntology


@dataclass(frozen=True)
class _MatcherEntry:
    concept: FinancialConcept
    surface: str
    relation: str
    requires_any_context: tuple[str, ...]
    excludes_any_context: tuple[str, ...]
    pattern: re.Pattern[str]


def load_ontology(path: str | Path) -> FinancialOntology:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return FinancialOntology.model_validate(payload)


class OntologyMatcher:
    """Longest-match, context-aware matcher that collapses aliases to concept IDs."""

    def __init__(self, ontology: FinancialOntology) -> None:
        self.ontology = ontology
        self.by_id = {concept.concept_id: concept for concept in ontology.concepts}
        entries: list[_MatcherEntry] = []
        for concept in ontology.concepts:
            surfaces = [(concept.pref_label_pt, "exact", (), ())]
            surfaces.extend(
                (
                    alias.value,
                    alias.relation,
                    alias.requires_any_context,
                    alias.excludes_any_context,
                )
                for alias in concept.aliases
            )
            for surface, relation, requires, excludes in surfaces:
                pattern = re.compile(rf"(?<!\w){re.escape(surface)}(?!\w)", re.IGNORECASE)
                entries.append(
                    _MatcherEntry(
                        concept=concept,
                        surface=surface,
                        relation=relation,
                        requires_any_context=requires,
                        excludes_any_context=excludes,
                        pattern=pattern,
                    )
                )
        self.entries = tuple(sorted(entries, key=lambda item: len(item.surface), reverse=True))

    @staticmethod
    def _context_ok(text: str, start: int, end: int, entry: _MatcherEntry) -> bool:
        left = max(0, start - 120)
        right = min(len(text), end + 120)
        context = text[left:right].casefold()
        if entry.requires_any_context and not any(
            token.casefold() in context for token in entry.requires_any_context
        ):
            return False
        if entry.excludes_any_context and any(
            token.casefold() in context for token in entry.excludes_any_context
        ):
            return False
        return True

    def match(self, text: str) -> tuple[ConceptMention, ...]:
        occupied: list[tuple[int, int]] = []
        mentions: list[ConceptMention] = []
        for entry in self.entries:
            for match in entry.pattern.finditer(text):
                start, end = match.span()
                if any(start < used_end and end > used_start for used_start, used_end in occupied):
                    continue
                if not self._context_ok(text, start, end, entry):
                    continue
                occupied.append((start, end))
                mentions.append(
                    ConceptMention(
                        concept_id=entry.concept.concept_id,
                        surface=match.group(0),
                        start=start,
                        end=end,
                        relation=entry.relation,
                        difficulty=entry.concept.difficulty,
                    )
                )
        return tuple(sorted(mentions, key=lambda item: (item.start, item.end)))
