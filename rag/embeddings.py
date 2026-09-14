"""
HuggingFace embedding model initialisation.
Uses sentence-transformers/all-MiniLM-L6-v2 — fully local, no API key required.
"""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import EMBEDDING_CONFIG


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Return a cached HuggingFaceEmbeddings instance.
    Cached so the model is only loaded once per process.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_CONFIG.model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
