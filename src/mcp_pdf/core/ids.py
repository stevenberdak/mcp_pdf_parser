from pathlib import Path
import hashlib
import os

def file_fingerprint(path: Path) -> str:
    """
    Cheap fingerprint: filename + size + mtime.
    Good for incremental ingests; if you need content-hash, swap implementation.
    """
    st = os.stat(path)
    return f"{path.name}-{st.st_size}-{int(st.st_mtime)}"

def chunk_id(fp: str, page: int, chunk: int, text: str) -> str:
    """
    Stable chunk id: fingerprint + location + short hash of content.
    Stored as Chroma id and also in metadata["id"] for citations.
    """
    h = hashlib.md5(text.encode("utf-8", errors="ignore")).hexdigest()[:10]
    return f"{fp}::p{page:06d}::c{chunk:04d}::{h}"
