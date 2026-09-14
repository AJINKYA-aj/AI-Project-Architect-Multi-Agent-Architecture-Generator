"""
Document loader for RAG pipeline.
Handles PDF and plain-text ingestion from file paths or uploaded bytes.
"""

import os
import tempfile
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_pdf_from_bytes(file_bytes: bytes, filename: str = "upload.pdf") -> List[Document]:
    """Load a PDF from raw bytes (e.g. Streamlit UploadedFile)."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = filename
        return docs
    finally:
        os.unlink(tmp_path)


def load_text_from_bytes(file_bytes: bytes, filename: str = "upload.txt") -> List[Document]:
    """Load a plain text file from raw bytes."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        loader = TextLoader(tmp_path, encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = filename
        return docs
    finally:
        os.unlink(tmp_path)


def load_documents_from_upload(file_bytes: bytes, filename: str) -> List[Document]:
    """Route uploaded file to appropriate loader based on extension."""
    ext = os.path.splitext(filename)[-1].lower()
    if ext == ".pdf":
        return load_pdf_from_bytes(file_bytes, filename)
    elif ext in (".txt", ".md"):
        return load_text_from_bytes(file_bytes, filename)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported: .pdf, .txt, .md")
