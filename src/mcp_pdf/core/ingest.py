from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
import json

from langchain_core.documents import Document

from ..config import SETTINGS
from .pdf import iter_pages
from .chunking import split_page
from .ids import file_fingerprint, chunk_id
from .storage import get_vectorstore


def _load_manifest() -> Dict[str, Any]:
    path = Path(SETTINGS.manifest_path)
    if not path.exists():
        return {"files": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        # If manifest is corrupt, start fresh rather than failing ingestion
        return {"files": {}}


def _save_manifest(manifest: Dict[str, Any]) -> None:
    path = Path(SETTINGS.manifest_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def iter_pdfs(root: Path) -> List[Path]:
    root = root.resolve()
    if root.is_file() and root.suffix.lower() == ".pdf":
        return [root]
    return sorted([p for p in root.rglob("*.pdf") if p.is_file()])


def _delete_by_source(vs, source: str) -> None:
    """
    Delete all vectors/chunks previously stored for a given source file.
    Works with Chroma's underlying collection.
    """
    # LangChain's Chroma wrapper exposes the underlying chromadb collection via _collection
    if hasattr(vs, "_collection") and vs._collection is not None:
        vs._collection.delete(where={"source": source})
        return
    # Fallback if wrapper supports delete(where=...)
    if hasattr(vs, "delete"):
        try:
            vs.delete(where={"source": source})
            return
        except TypeError:
            pass
    raise RuntimeError("Vector store does not support delete-by-metadata in this environment.")


def ingest_pdf(pdf_path: Path, *, force: bool = False) -> Dict[str, Any]:
    pdf_path = pdf_path.resolve()
    key = str(pdf_path)

    vs = get_vectorstore()
    manifest = _load_manifest()
    files = manifest.setdefault("files", {})

    fp = file_fingerprint(pdf_path)

    # Skip unchanged
    if not force and key in files and files[key].get("fp") == fp:
        return {"path": key, "status": "skipped", "reason": "unchanged", "fp": fp}

    # Delete stale chunks for this file before re-adding
    try:
        _delete_by_source(vs, key)
    except Exception:
        # If delete fails (older wrappers), we still proceed.
        # Query-time can filter by latest fingerprint if you add that constraint.
        pass

    batch_docs: List[Document] = []
    batch_ids: List[str] = []
    total_chunks = 0

    for page_doc in iter_pages(pdf_path):
        page_doc.metadata = page_doc.metadata or {}
        # Normalize source
        page_doc.metadata["source"] = key

        # PyPDFLoader typically uses 0-based page index
        page0 = page_doc.metadata.get("page", 0)
        page = (page0 + 1) if isinstance(page0, int) else -1

        chunks = split_page(
            page_doc,
            chunk_size=SETTINGS.chunk_size_chars,
            overlap=SETTINGS.chunk_overlap_chars,
        )

        for d in chunks:
            cidx = int(d.metadata.get("chunk", 0))
            cid = chunk_id(fp, page, cidx, d.page_content)

            d.metadata.update({
                "id": cid,      # for citations
                "fp": fp,       # for incremental/debug
                "page": page,
                "chunk": cidx,
                "source": key,
            })

            batch_docs.append(d)
            batch_ids.append(cid)
            total_chunks += 1

            if len(batch_docs) >= SETTINGS.ingest_batch_size:
                vs.add_documents(batch_docs, ids=batch_ids)
                batch_docs.clear()
                batch_ids.clear()

    if batch_docs:
        vs.add_documents(batch_docs, ids=batch_ids)

    vs.persist()

    files[key] = {"fp": fp, "chunks": total_chunks}
    _save_manifest(manifest)

    return {"path": key, "status": "ingested", "fp": fp, "chunks": total_chunks}


def ingest_directory(root: Path, *, force: bool = False) -> Dict[str, Any]:
    root = root.resolve()
    pdfs = iter_pdfs(root)

    results: List[Dict[str, Any]] = []
    counts = {"ingested": 0, "skipped": 0, "failed": 0}

    for pdf in pdfs:
        try:
            r = ingest_pdf(pdf, force=force)
            results.append(r)
            counts[r["status"]] += 1
        except Exception as e:
            results.append({"path": str(pdf), "status": "failed", "error": str(e)})
            counts["failed"] += 1

    return {"root": str(root), "counts": counts, "results": results}
