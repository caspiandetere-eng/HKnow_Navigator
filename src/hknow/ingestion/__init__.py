"""Document ingestion and acquisition module exports."""

from hknow.ingestion.base import BaseDocumentLoader
from hknow.ingestion.json_loader import JSONHealthcareLoader
from hknow.ingestion.schemas import (
    HealthcareAuthority,
    HealthcareDocumentMetadata,
    RawHealthcareDocument,
)
from hknow.ingestion.text_loader import TextHealthcareLoader

__all__ = [
    "BaseDocumentLoader",
    "HealthcareAuthority",
    "HealthcareDocumentMetadata",
    "JSONHealthcareLoader",
    "RawHealthcareDocument",
    "TextHealthcareLoader",
]
