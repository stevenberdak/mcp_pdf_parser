from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from ..config import SETTINGS

def get_vectorstore(persist_dir: str | None = None, collection: str | None = None) -> Chroma:
    """
    Local persistent Chroma + local sentence-transformers embeddings.
    """
    embeddings = HuggingFaceEmbeddings(model_name=SETTINGS.embedding_model_name)
    return Chroma(
        collection_name=collection or SETTINGS.collection,
        persist_directory=persist_dir or SETTINGS.persist_dir,
        embedding_function=embeddings,
    )
