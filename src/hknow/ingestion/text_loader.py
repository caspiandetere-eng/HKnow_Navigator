"""
Text and Markdown document loader.
"""

from pathlib import Path

from hknow.config.logging import get_logger
from hknow.ingestion.base import BaseDocumentLoader
from hknow.ingestion.schemas import (
    HealthcareAuthority,
    HealthcareDocumentMetadata,
    RawHealthcareDocument,
)

logger = get_logger(__name__)


class TextHealthcareLoader(BaseDocumentLoader):
    """
    Loads Markdown (.md) or Text (.txt) files.
    """

    def __init__(
        self,
        default_source: HealthcareAuthority = "OtherAuthoritative",
        default_category: str = "general",
    ) -> None:
        self.default_source = default_source
        self.default_category = default_category

    def load(self, file_path: Path) -> list[RawHealthcareDocument]:
        """
        Loads a raw text or markdown file as a single RawHealthcareDocument.
        """
        if not file_path.exists():
            logger.error("File not found: %s", file_path)
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info("Loading text document from %s", file_path)
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            raise ValueError(f"File {file_path} is empty.")

        metadata = HealthcareDocumentMetadata(
            source=self.default_source,
            title=file_path.stem.replace("_", " ").replace("-", " ").title(),
            document_type="article",
            category=self.default_category,
        )

        doc = RawHealthcareDocument(
            document_id=file_path.stem,
            content=content,
            metadata=metadata,
        )

        return [doc]
