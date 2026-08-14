"""
Abstract base class for document loaders.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from hknow.ingestion.schemas import RawHealthcareDocument


class BaseDocumentLoader(ABC):
    """
    Abstract contract for ingesting raw files into standardized RawHealthcareDocuments.
    """

    @abstractmethod
    def load(self, file_path: Path) -> list[RawHealthcareDocument]:
        """
        Loads and parses a document from disk into a list of RawHealthcareDocument objects.

        Parameters
        ----------
        file_path : Path
            Path to the source file to ingest.

        Returns
        -------
        list[RawHealthcareDocument]
            List of parsed raw document models.
        """
        raise NotImplementedError
