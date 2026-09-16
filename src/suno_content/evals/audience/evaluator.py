from __future__ import annotations

import re
from collections import Counter, defaultdict

from suno_content.domain import AudienceLevel, OutputFormat

from .models import (
    AntiGamingDiagnostics,
    AudienceComplexityVector,
    ContextEvidence,
    FinancialOntology,
    TerminologyVector,
)
from .ontology import OntologyMatcher
from .readability import evaluate_readability

_EXPLANATION_RE = re.compile(
    r"\b(?:é|significa|quer dizer|ou seja|isto é|mede|representa|indica|corresponde|reflete)\b",
    re.IGNORECASE,
)
_CONTEXT_RE = re.compile(
    r"\b(?:na prática|isso significa|impacta|afeta|mostra|serve para|ajuda a|por isso|porque)\b",
    re.IGNORECASE,
)
_ANALOGY_RE = re.compile(
    r"\b(?:pense como|funciona como|é como|imagine|como se fosse|analogia)\b",
    re.IGNORECASE,
)


def _local_window(text: str, start: int, end: int, radius: int = 180) -> str:
    left_boundary = max(
        text.rfind(".", 0, start),
        text.rfind("!", 0, start),
        text.rfind("?", 0, start),
        text.rfind("\n", 0, start),
    )
    left = max(left_boundary + 1, start - radius, 0)
    right_candidates = [idx for sep in ".!?\n" if (idx := text.find(sep, end)) != -1]
    right_boundary = min(right_candidates) + 1 if right_candidates else len(text)
    right = min(right_boundary, end + radius, len(text))
    return text[left:right]


def _context_evidence(text: str, matcher: OntologyMatcher, mentions) -> tuple[ContextEvidence, ...]:
    first_mentions = {}
    for mention in mentions:
        first_mentions.setdefault(mention.concept_id, mention)

    evidence: list[ContextEvidence] = []
    for concept_id, mention in sorted(first_mentions.items()):
        window = _local_window(text, mention.start, mention.end)
        concept = matcher.by_id[concept_id]
        other_surface_present = any(
            alias.value.casefold() in window.casefold()
            and alias.value.casefold() != mention.surface.casefold()
            for alias in concept.aliases
        ) or (
            concept.pref_label_pt.casefold() in window.casefold()
            and concept.pref_label_pt.casefold() != mention.surface.casefold()
        )
        explanation = bool(_EXPLANATION_RE.search(window) or other_surface_present)
        practical = bool(_CONTEXT_RE.search(window))
        analogy = bool(_ANALOGY_RE.search(window))
        evidence.append(
            ContextEvidence(
                concept_id=concept_id,
                definition_or_explanation=explanation,
                practical_context=practical,
                analogy=analogy,
            )
        )
    return tuple(evidence)


def _is_acronym(surface: str, relation: str) -> bool:
    letters = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ]", "", surface)
    return relation == "exact_acronym" or (2 <= len(letters) <= 8 and letters.isupper())


def evaluate_audience_features(
    text: str,
    *,
    audience: AudienceLevel,
    output_format: OutputFormat,
    ontology: FinancialOntology,
    required_concept_ids: set[str] | frozenset[str] | tuple[str, ...] = (),
) -> AudienceComplexityVector:
    matcher = OntologyMatcher(ontology)
    mentions = matcher.match(text)
    readability = evaluate_readability(text, output_format)
    word_count = max(1, readability.word_count)

    detected = tuple(sorted({mention.concept_id for mention in mentions}))
    raw_density = len(mentions) / word_count * 100.0
    unique_density = len(detected) / word_count * 100.0
    weighted_density = (
        sum(matcher.by_id[concept_id].difficulty for concept_id in detected) / word_count * 100.0
    )

    evidence = _context_evidence(text, matcher, mentions)
    evidence_by_id = {item.concept_id: item for item in evidence}
    explanation_required: list[str] = []
    analogy_required: list[str] = []
    for concept_id in detected:
        policy = matcher.by_id[concept_id].audience_policy[audience]
        if policy in {"explain_on_first_use", "explain_and_analogy"}:
            explanation_required.append(concept_id)
        if policy == "explain_and_analogy":
            analogy_required.append(concept_id)

    unexplained = [
        concept_id
        for concept_id in explanation_required
        if not evidence_by_id[concept_id].contextualized
    ]
    unexplained_rate = (
        len(unexplained) / len(explanation_required) if explanation_required else None
    )
    contextualization_rate = (
        sum(evidence_by_id[cid].contextualized for cid in explanation_required)
        / len(explanation_required)
        if explanation_required
        else None
    )
    analogy_rate = (
        sum(evidence_by_id[cid].analogy for cid in analogy_required) / len(analogy_required)
        if analogy_required
        else None
    )

    required = tuple(sorted(set(required_concept_ids)))
    unknown_required = [concept_id for concept_id in required if concept_id not in matcher.by_id]
    if unknown_required:
        raise ValueError(f"required concepts absent from ontology: {unknown_required}")
    missing_required = tuple(sorted(set(required) - set(detected)))
    recall = (
        (len(required) - len(missing_required)) / len(required)
        if required
        else None
    )

    counts = Counter(mention.concept_id for mention in mentions)
    repetition_ratio = (
        (len(mentions) - len(detected)) / len(mentions) if mentions else 0.0
    )
    surfaces = defaultdict(set)
    for mention in mentions:
        surfaces[mention.concept_id].add(mention.surface.casefold())
    alias_stuffing = any(counts[cid] >= 3 and len(surfaces[cid]) >= 2 for cid in counts)
    jargon_stuffing = len(mentions) >= 4 and repetition_ratio >= 0.5

    acronym_mentions = sum(_is_acronym(m.surface, m.relation) for m in mentions)
    acronym_ratio = acronym_mentions / len(mentions) if mentions else 0.0
    acronym_hack = bool(
        len(mentions) >= 3
        and acronym_ratio >= 0.75
        and ((unexplained_rate or 0.0) >= 0.5 or repetition_ratio >= 0.33)
    )

    glossary_dumping = False
    for line in text.splitlines() or [text]:
        line_mentions = matcher.match(line)
        if len({m.concept_id for m in line_mentions}) >= 3 and re.search(r"[,;|]", line):
            if not (
                _EXPLANATION_RE.search(line)
                or _CONTEXT_RE.search(line)
                or _ANALOGY_RE.search(line)
            ):
                glossary_dumping = True
                break

    sentence_chopping = bool(
        readability.sentence_count >= 4
        and (
            readability.very_short_sentence_ratio >= 0.5
            or readability.fragment_ratio >= 0.3
        )
    )
    required_omission = bool(required and missing_required)

    flags: list[str] = []
    if jargon_stuffing:
        flags.append("JARGON_STUFFING")
    if alias_stuffing:
        flags.append("ALIAS_STUFFING")
    if glossary_dumping:
        flags.append("GLOSSARY_DUMPING")
    if sentence_chopping:
        flags.append("SENTENCE_CHOPPING")
    if acronym_hack:
        flags.append("ACRONYM_HACK")
    if required_omission:
        flags.append("REQUIRED_CONCEPT_OMISSION")

    return AudienceComplexityVector(
        ontology_version=ontology.ontology_version,
        audience=audience,
        format=output_format,
        readability=readability,
        terminology=TerminologyVector(
            raw_term_density_per_100_words=round(raw_density, 6),
            unique_concept_density_per_100_words=round(unique_density, 6),
            difficulty_weighted_density_per_100_words=round(weighted_density, 6),
            unexplained_jargon_rate=(
                round(unexplained_rate, 6) if unexplained_rate is not None else None
            ),
            contextualization_rate=(
                round(contextualization_rate, 6)
                if contextualization_rate is not None
                else None
            ),
            analogy_rate=round(analogy_rate, 6) if analogy_rate is not None else None,
            required_concept_recall=round(recall, 6) if recall is not None else None,
            detected_concepts=detected,
            required_concepts=required,
            missing_required_concepts=missing_required,
            context_evidence=evidence,
        ),
        anti_gaming=AntiGamingDiagnostics(
            repetition_ratio=round(repetition_ratio, 6),
            acronym_mention_ratio=round(acronym_ratio, 6),
            jargon_stuffing=jargon_stuffing,
            alias_stuffing=alias_stuffing,
            glossary_dumping=glossary_dumping,
            sentence_chopping=sentence_chopping,
            acronym_hack=acronym_hack,
            required_concept_omission=required_omission,
            flags=tuple(flags),
        ),
    )
