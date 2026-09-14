"""
Report Consolidation Agent.

Responsibilities:
- Consume outputs from Requirement Agent and System Design Agent
- Produce a single polished software planning report
- Format for stakeholder and engineering audience
"""

from typing import Optional

from langchain_ollama import OllamaLLM

from config.settings import MODEL_CONFIG
from prompts.report_prompt import build_report_prompt


class ReportAgent:
    """
    Agent 3: Consolidates requirements and system design into a final report.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or MODEL_CONFIG.default_model
        self.llm = OllamaLLM(
            model=self.model_name,
            base_url=MODEL_CONFIG.ollama_base_url,
            temperature=MODEL_CONFIG.temperature,
            num_predict=MODEL_CONFIG.max_tokens,
        )

    def run(self, requirements_output: str, system_design_output: str) -> str:
        """
        Generate the final consolidated report.

        Args:
            requirements_output: Output from RequirementAgent.run()
            system_design_output: Output from SystemDesignAgent.run()

        Returns:
            Final polished report as a markdown string.
        """
        prompt = build_report_prompt(requirements_output, system_design_output)
        return self.llm.invoke(prompt)
