"""
JSON document loader for structured healthcare records.
"""

import json
from pathlib import Path

from hknow.config.logging import get_logger
from hknow.ingestion.base import BaseDocumentLoader
from hknow.ingestion.schemas import HealthcareDocumentMetadata, RawHealthcareDocument

logger = get_logger(__name__)


class JSONHealthcareLoader(BaseDocumentLoader):
    """
    Loads and parses JSON files into RawHealthcareDocument instances.
    Supports either a single document object or a list of document objects.
    """

    def load(self, file_path: Path) -> list[RawHealthcareDocument]:
        """
        Parse JSON file and validate against RawHealthcareDocument schema.
        """
        if not file_path.exists():
            logger.error("File not found: %s", file_path)
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info("Loading JSON healthcare document from %s", file_path)
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        records: list[dict] = data if isinstance(data, list) else [data]
        documents: list[RawHealthcareDocument] = []

        for idx, item in enumerate(records):
            try:
                # If metadata is nested or flattened, reconstruct appropriately
                meta_data = item.get("metadata", {})
                if not meta_data:
                    meta_data = {
                        "source": item.get("source", "OtherAuthoritative"),
                        "title": item.get("title", file_path.stem),
                        "url": item.get("url"),
                        "publication_date": item.get("publication_date"),
                        "document_type": item.get("document_type", "article"),
                        "category": item.get("category", "general"),
                    }

                metadata = HealthcareDocumentMetadata(**meta_data)
                doc = RawHealthcareDocument(
                    document_id=item.get("document_id", f"{file_path.stem}_{idx}"),
                    content=item.get("content", ""),
                    metadata=metadata,
                )
                documents.append(doc)
            except Exception as e:
                logger.warning(
                    "Failed to parse item index %d in %s: %s", idx, file_path, e
                )
                raise

        logger.info(
            "Successfully loaded %d documents from %s", len(documents), file_path
        )
        return documents
