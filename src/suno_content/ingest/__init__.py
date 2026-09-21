from .adapters import (
    AutoPdfAdapter,
    PdfExtraction,
    PdfParserAdapter,
    PdfParserError,
    PdfParserUnavailable,
    PdftotextAdapter,
    PypdfAdapter,
    detect_table_role_ambiguity,
)
from .service import (
    IngestResult,
    IntegratedEvidence,
    ThreeByThreeCell,
    ingest_pdf_bytes,
    ingest_pdf_path,
    ingest_text,
    load_integrated_evidence,
)

__all__ = [
    "AutoPdfAdapter",
    "IngestResult",
    "IntegratedEvidence",
    "PdfExtraction",
    "PdfParserAdapter",
    "PdfParserError",
    "PdfParserUnavailable",
    "PdftotextAdapter",
    "PypdfAdapter",
    "ThreeByThreeCell",
    "detect_table_role_ambiguity",
    "ingest_pdf_bytes",
    "ingest_pdf_path",
    "ingest_text",
    "load_integrated_evidence",
]
