"""
Central configuration for AI Project Architect.
All model names, paths, and tunable parameters live here.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ModelConfig:
    available_models: List[str] = field(default_factory=lambda: [
        "phi3",
        "llama3.2",
        "qwen2.5",
        "tinyllama",
        "gemma:2b",
    ])
    default_model: str = "tinyllama"
    ollama_base_url: str = "http://localhost:11434"
    temperature: float = 0.3
    max_tokens: int = 1024


@dataclass
class EmbeddingConfig:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 150
    retriever_k: int = 4


@dataclass
class AppConfig:
    title: str = "AI Project Architect"
    subtitle: str = "Multi-Agent Software Architecture Generator"
    faiss_index_path: str = "data/faiss_index"


MODEL_CONFIG = ModelConfig()
EMBEDDING_CONFIG = EmbeddingConfig()
APP_CONFIG = AppConfig()
