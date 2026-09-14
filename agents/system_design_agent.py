"""
System Design Agent.

Responsibilities:
- Consume requirements document from Requirement Agent
- Design database schema, API endpoints, tech stack
- Generate full system architecture description
- Suggest auth and deployment strategies
"""

from typing import Optional

from langchain_ollama import OllamaLLM

from config.settings import MODEL_CONFIG
from prompts.system_design_prompt import build_system_design_prompt


class SystemDesignAgent:
    """
    Agent 2: Takes structured requirements and produces a detailed system design.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or MODEL_CONFIG.default_model
        self.llm = OllamaLLM(
            model=self.model_name,
            base_url=MODEL_CONFIG.ollama_base_url,
            temperature=MODEL_CONFIG.temperature,
            num_predict=MODEL_CONFIG.max_tokens,
        )

    def run(self, requirements_output: str) -> str:
        """
        Generate a system design document from requirements.

        Args:
            requirements_output: Output from RequirementAgent.run()

        Returns:
            Structured system design document as a string.
        """
        prompt = build_system_design_prompt(requirements_output)
        return self.llm.invoke(prompt)
