from datetime import date

import pytest
from pydantic import ValidationError

from hknow.ingestion.schemas import (
    HealthcareDocumentMetadata,
    RawHealthcareDocument,
)


def test_valid_metadata_creation():
    """Verify metadata model parses and validates valid source metadata."""
    metadata = HealthcareDocumentMetadata(
        source="WHO",
        title="Cardiovascular Disease Factsheet",
        url="https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases",
        publication_date=date(2024, 1, 15),
        document_type="factsheet",
        category="cardiology",
    )

    assert metadata.source == "WHO"
    assert metadata.title == "Cardiovascular Disease Factsheet"
    assert str(metadata.url).startswith("https://www.who.int")
    assert metadata.document_type == "factsheet"


def test_invalid_authority_validation():
    """Verify invalid authority raises a ValidationError."""
    with pytest.raises(ValidationError):
        HealthcareDocumentMetadata(
            source="RandomBlog",  # type: ignore[arg-type]
            title="Unverified post",
        )


def test_raw_document_creation():
    """Verify raw document creation with required fields."""
    metadata = HealthcareDocumentMetadata(
        source="CDC",
        title="Seasonal Flu Basics",
    )
    doc = RawHealthcareDocument(
        document_id="cdc-flu-001",
        content="Influenza is a contagious respiratory illness caused by influenza viruses.",
        metadata=metadata,
    )

    assert doc.document_id == "cdc-flu-001"
    assert "Influenza" in doc.content
    assert doc.metadata.source == "CDC"
    assert doc.ingested_at is not None
