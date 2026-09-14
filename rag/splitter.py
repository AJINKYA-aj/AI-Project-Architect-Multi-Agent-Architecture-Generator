"""
Text splitting utilities for the RAG pipeline.
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import EMBEDDING_CONFIG


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split raw documents into smaller chunks suitable for embedding.
    Uses RecursiveCharacterTextSplitter for semantic-aware splitting.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=EMBEDDING_CONFIG.chunk_size,
        chunk_overlap=EMBEDDING_CONFIG.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    return chunks
