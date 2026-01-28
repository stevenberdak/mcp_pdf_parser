from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    # Chroma persistence
    persist_dir: str = "./chroma_store"
    collection: str = "pdf_chunks"
    manifest_path: str = "./chroma_store/manifest.json"

    # Chunking
    chunk_size_chars: int = 2000
    chunk_overlap_chars: int = 150

    # Ingestion
    ingest_batch_size: int = 64

    # Retrieval
    top_k: int = 10

    # Local embeddings
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

SETTINGS = Settings()
