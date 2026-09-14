"""
FAISS vector store management for the RAG pipeline.
Supports building an in-memory store from uploaded documents and
persisting/loading the index from disk.
"""

import os
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from config.settings import APP_CONFIG, EMBEDDING_CONFIG
from rag.embeddings import get_embeddings


def build_vectorstore(chunks: List[Document]) -> FAISS:
    """Create a FAISS vector store from document chunks."""
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def save_vectorstore(vectorstore: FAISS) -> None:
    """Persist the FAISS index to disk."""
    os.makedirs(APP_CONFIG.faiss_index_path, exist_ok=True)
    vectorstore.save_local(APP_CONFIG.faiss_index_path)


def load_vectorstore() -> Optional[FAISS]:
    """Load the FAISS index from disk. Returns None if not found."""
    index_file = os.path.join(APP_CONFIG.faiss_index_path, "index.faiss")
    if not os.path.exists(index_file):
        return None
    embeddings = get_embeddings()
    return FAISS.load_local(
        APP_CONFIG.faiss_index_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )


def get_retriever(vectorstore: FAISS):
    """Return a LangChain retriever from the vector store."""
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": EMBEDDING_CONFIG.retriever_k},
    )


def retrieve_context(vectorstore: FAISS, query: str) -> str:
    """
    Retrieve relevant document chunks and join them into a single context string.
    """
    retriever = get_retriever(vectorstore)
    docs = retriever.invoke(query)
    if not docs:
        return ""
    return "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )
