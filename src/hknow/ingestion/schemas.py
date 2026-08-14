"""
Data models and schemas for healthcare document ingestion.
"""

from datetime import UTC, date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl

HealthcareAuthority = Literal[
    "WHO",
    "CDC",
    "NIH",
    "FDA",
    "NHS",
    "PubMed",
    "ClinicalGuideline",
    "OtherAuthoritative",
]

DocumentType = Literal["guideline", "article", "report", "factsheet", "faq"]


class HealthcareDocumentMetadata(BaseModel):
    """
    Standard metadata schema associated with an ingested healthcare document.
    """

    source: HealthcareAuthority = Field(
        description="Authoritative source governing the document"
    )
    title: str = Field(min_length=1, description="Title of the document")
    url: HttpUrl | None = Field(
        default=None, description="Canonical source URL of the document"
    )
    publication_date: date | None = Field(
        default=None, description="Original publication or revision date"
    )
    document_type: DocumentType = Field(
        default="article", description="Classification of the document structure"
    )
    category: str = Field(
        default="general",
        description="Clinical or healthcare category (e.g., cardiology, immunology)",
    )
    extra: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional unstructured metadata key-values",
    )


class RawHealthcareDocument(BaseModel):
    """
    Represents an unprocessed raw healthcare document ingested into the system.
    """

    document_id: str = Field(
        min_length=1, description="Unique identifier for the document"
    )
    content: str = Field(
        min_length=1, description="Raw text or structured markdown content"
    )
    metadata: HealthcareDocumentMetadata = Field(
        description="Standardized metadata attributes"
    )
    ingested_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when document was acquired",
    )
