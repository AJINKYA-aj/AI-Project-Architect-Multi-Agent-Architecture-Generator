"""
Requirement Analysis Agent.

Responsibilities:
- Analyze project description
- Optionally enrich with RAG context from uploaded documents
- Generate structured requirements document
"""

from typing import Optional

from langchain_ollama import OllamaLLM

from config.settings import MODEL_CONFIG
from prompts.requirement_prompt import build_requirement_prompt


class RequirementAgent:
    """
    Agent 1: Transforms a raw project idea into a detailed requirements document.
    Uses RAG context when a vector store is available.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or MODEL_CONFIG.default_model
        self.llm = OllamaLLM(
            model=self.model_name,
            base_url=MODEL_CONFIG.ollama_base_url,
            temperature=MODEL_CONFIG.temperature,
            num_predict=MODEL_CONFIG.max_tokens,
        )

    def run(self, project_description: str, rag_context: str = "") -> str:
        """
        Generate a requirements document for the given project.

        Args:
            project_description: The user's raw project idea.
            rag_context: Retrieved context from uploaded documents (optional).

        Returns:
            Structured requirements document as a string.
        """
        prompt = build_requirement_prompt(project_description, rag_context)
        return self.llm.invoke(prompt)
