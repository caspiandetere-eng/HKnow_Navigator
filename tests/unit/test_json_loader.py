import json
from pathlib import Path

import pytest

from hknow.ingestion.json_loader import JSONHealthcareLoader


def test_json_loader_single_doc(tmp_path: Path):
    """Verify loading a single structured JSON document."""
    file_path = tmp_path / "who_doc.json"
    doc_data = {
        "document_id": "who-sample-01",
        "content": "Cardiovascular diseases are the leading cause of death globally.",
        "metadata": {
            "source": "WHO",
            "title": "CVD Overview",
            "category": "cardiology",
        },
    }
    file_path.write_text(json.dumps(doc_data), encoding="utf-8")

    loader = JSONHealthcareLoader()
    docs = loader.load(file_path)

    assert len(docs) == 1
    assert docs[0].document_id == "who-sample-01"
    assert docs[0].metadata.source == "WHO"
    assert "Cardiovascular" in docs[0].content


def test_json_loader_missing_file(tmp_path: Path):
    """Verify error raised on non-existent file."""
    loader = JSONHealthcareLoader()
    with pytest.raises(FileNotFoundError):
        loader.load(tmp_path / "non_existent.json")
