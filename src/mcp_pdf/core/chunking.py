import re
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(s: str) -> str:
    # Conservative cleanup: preserve content while normalizing whitespace.
    s = s.replace("\x00", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def split_page(doc: Document, *, chunk_size: int, overlap: int) -> List[Document]:
    """
    Split a page Document into smaller chunk Documents while preserving metadata.
    Uses character-based chunking (fast, robust).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". "],
    )

    text = clean_text(doc.page_content or "")
    if not text:
        return []

    chunks = splitter.split_text(text)
    out: List[Document] = []
    base_md = dict(doc.metadata or {})
    for i, ch in enumerate(chunks):
        ch = clean_text(ch)
        if not ch:
            continue
        md = {**base_md, "chunk": i}
        out.append(Document(page_content=ch, metadata=md))
    return out
