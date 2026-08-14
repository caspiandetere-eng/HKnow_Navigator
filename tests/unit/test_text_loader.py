from pathlib import Path

import pytest

from hknow.ingestion.text_loader import TextHealthcareLoader


def test_text_loader_valid(tmp_path: Path):
    """Verify loading text files with default metadata generation."""
    file_path = tmp_path / "diabetes_prevention.md"
    file_path.write_text(
        "# Diabetes Prevention\nA healthy diet and physical activity help prevent type 2 diabetes.",
        encoding="utf-8",
    )

    loader = TextHealthcareLoader(
        default_source="CDC", default_category="endocrinology"
    )
    docs = loader.load(file_path)

    assert len(docs) == 1
    assert docs[0].document_id == "diabetes_prevention"
    assert docs[0].metadata.source == "CDC"
    assert docs[0].metadata.category == "endocrinology"
    assert "Diabetes Prevention" in docs[0].content


def test_text_loader_empty_file(tmp_path: Path):
    """Verify error raised when reading an empty file."""
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    loader = TextHealthcareLoader()
    with pytest.raises(ValueError, match="is empty"):
        loader.load(file_path)
