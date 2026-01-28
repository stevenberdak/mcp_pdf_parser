from ..config import SETTINGS
from ..core.storage import get_vectorstore
from .schema import ModelContext, RetrievedChunk

def assemble_context(query: str, top_k: int | None = None) -> ModelContext:
    vs = get_vectorstore()
    k = top_k or SETTINGS.top_k

    results = vs.similarity_search_with_score(query, k=k)

    retrieved = []
    for doc, score in results:
        md = doc.metadata or {}
        retrieved.append(
            RetrievedChunk(
                chunk_id=str(md.get("id", "")),
                text=doc.page_content,
                source=str(md.get("source", "")),
                page=int(md.get("page", -1)),
                score=float(score),
            )
        )

    return ModelContext(query=query, retrieved=retrieved, metadata={"k": k})
