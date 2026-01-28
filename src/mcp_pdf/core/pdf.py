from pathlib import Path
from typing import Iterator

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def iter_pages(pdf_path: Path) -> Iterator[Document]:
    """
    Lazily yield page Documents from a PDF.
    PyPDFLoader typically includes 0-based page index in metadata["page"].
    """
    loader = PyPDFLoader(str(pdf_path))
    yield from loader.lazy_load()
