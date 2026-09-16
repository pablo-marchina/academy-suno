from __future__ import annotations

from typing import Literal
from pydantic import Field, model_validator

from suno_content.domain import AudienceLevel, DomainModel, OutputFormat

READABILITY_VERSION = "ptbr-readability-v001"
ONTOLOGY_SCHEMA_VERSION = "finance-ontology-schema-v001"
FEATURE_VERSION = "audience-features-v001"
THRESHOLD_MODE = "DIAGNOSTIC_ONLY_UNTIL_GOLD"

AliasRelation = Literal[
    "exact",
    "exact_acronym",
    "translation",
    "near_equivalent",
    "deprecated",
]
TermPolicy = Literal[
    "allow",
    "explain_on_first_use",
    "explain_and_analogy",
    "preserve_term",
    "avoid_unless_required",
]


class OntologySourceRef(DomainModel):
    authority: str
    url: str
    source_type: str = "institutional"


class ConceptAlias(DomainModel):
    value: str
    relation: AliasRelation = "exact"
    requires_any_context: tuple[str, ...] = ()
    excludes_any_context: tuple[str, ...] = ()


class FinancialConcept(DomainModel):
    concept_id: str
    pref_label_pt: str
    aliases: tuple[ConceptAlias, ...] = ()
    definition_canonical: str
    definition_beginner: str | None = None
    category: str
    difficulty: int = Field(ge=1, le=3)
    audience_policy: dict[AudienceLevel, TermPolicy]
    source_refs: tuple[OntologySourceRef, ...] = ()

    @model_validator(mode="after")
    def require_all_audiences(self) -> "FinancialConcept":
        missing = set(AudienceLevel) - set(self.audience_policy)
        if missing:
            raise ValueError(f"audience_policy missing: {sorted(item.value for item in missing)}")
        return self


class FinancialOntology(DomainModel):
    schema_version: str
    ontology_version: str
    language: Literal["pt-BR"]
    concepts: tuple[FinancialConcept, ...]

    @model_validator(mode="after")
    def validate_identity(self) -> "FinancialOntology":
        if self.schema_version != ONTOLOGY_SCHEMA_VERSION:
            raise ValueError(f"unsupported schema_version: {self.schema_version}")
        ids = [concept.concept_id for concept in self.concepts]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate concept_id")
        return self


class ConceptMention(DomainModel):
    concept_id: str
    surface: str
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    relation: AliasRelation
    difficulty: int = Field(ge=1, le=3)


class ReadabilityResult(DomainModel):
    version: str = READABILITY_VERSION
    format: OutputFormat
    flesch_raw: float | None
    words_per_sentence: float | None
    syllables_per_word: float | None
    sentence_count: int = Field(ge=0)
    word_count: int = Field(ge=0)
    supported_syllable_tokens: int = Field(ge=0)
    syllable_coverage: float = Field(ge=0.0, le=1.0)
    unsupported_tokens: tuple[str, ...] = ()
    very_short_sentence_ratio: float = Field(ge=0.0, le=1.0)
    very_long_sentence_ratio: float = Field(ge=0.0, le=1.0)
    fragment_ratio: float = Field(ge=0.0, le=1.0)
    valid: bool


class ContextEvidence(DomainModel):
    concept_id: str
    definition_or_explanation: bool = False
    practical_context: bool = False
    analogy: bool = False

    @property
    def contextualized(self) -> bool:
        return self.definition_or_explanation or self.practical_context or self.analogy


class TerminologyVector(DomainModel):
    raw_term_density_per_100_words: float
    unique_concept_density_per_100_words: float
    difficulty_weighted_density_per_100_words: float
    unexplained_jargon_rate: float | None
    contextualization_rate: float | None
    analogy_rate: float | None
    required_concept_recall: float | None
    detected_concepts: tuple[str, ...]
    required_concepts: tuple[str, ...]
    missing_required_concepts: tuple[str, ...]
    context_evidence: tuple[ContextEvidence, ...]


class AntiGamingDiagnostics(DomainModel):
    repetition_ratio: float = Field(ge=0.0, le=1.0)
    acronym_mention_ratio: float = Field(ge=0.0, le=1.0)
    jargon_stuffing: bool = False
    alias_stuffing: bool = False
    glossary_dumping: bool = False
    sentence_chopping: bool = False
    acronym_hack: bool = False
    required_concept_omission: bool = False
    flags: tuple[str, ...] = ()


class AudienceComplexityVector(DomainModel):
    schema_version: str = "audience-complexity-vector-v001"
    feature_version: str = FEATURE_VERSION
    ontology_version: str
    threshold_mode: str = THRESHOLD_MODE
    audience: AudienceLevel
    format: OutputFormat
    readability: ReadabilityResult
    terminology: TerminologyVector
    anti_gaming: AntiGamingDiagnostics
