"""
AI Project Architect — Main Orchestrator.

Runs the three-agent pipeline in sequence:
  1. RequirementAgent
  2. SystemDesignAgent
  3. ReportAgent

Can be used as a library by the Streamlit UI or run directly from the CLI.
"""

from dataclasses import dataclass
from typing import Optional

from agents import RequirementAgent, SystemDesignAgent, ReportAgent


@dataclass
class PipelineResult:
    requirements: str
    system_design: str
    final_report: str


def run_pipeline(
    project_description: str,
    model_name: str,
    rag_context: str = "",
) -> PipelineResult:
    """
    Execute the full multi-agent pipeline.

    Args:
        project_description: Raw project idea from the user.
        model_name: Ollama model to use for all agents.
        rag_context: Retrieved context from FAISS (empty string if no docs uploaded).

    Returns:
        PipelineResult with outputs from all three agents.
    """
    print(f"[Pipeline] Starting with model: {model_name}")

    print("[Agent 1] Running Requirement Agent...")
    req_agent = RequirementAgent(model_name=model_name)
    requirements = req_agent.run(project_description, rag_context)

    print("[Agent 2] Running System Design Agent...")
    design_agent = SystemDesignAgent(model_name=model_name)
    system_design = design_agent.run(requirements)

    print("[Agent 3] Running Report Agent...")
    report_agent = ReportAgent(model_name=model_name)
    final_report = report_agent.run(requirements, system_design)

    print("[Pipeline] Complete.")
    return PipelineResult(
        requirements=requirements,
        system_design=system_design,
        final_report=final_report,
    )


if __name__ == "__main__":
    import sys

    description = " ".join(sys.argv[1:]) or "Build a Labour Contractor Management System"
    result = run_pipeline(
        project_description=description,
        model_name="phi3",
    )

    print("\n" + "=" * 80)
    print("REQUIREMENTS")
    print("=" * 80)
    print(result.requirements)

    print("\n" + "=" * 80)
    print("SYSTEM DESIGN")
    print("=" * 80)
    print(result.system_design)

    print("\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print(result.final_report)
