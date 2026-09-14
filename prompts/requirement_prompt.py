"""
Prompt template for the Requirement Analysis Agent.
"""

REQUIREMENT_PROMPT_TEMPLATE = """
You are a Senior Business Analyst and Requirements Engineer at a top-tier software consultancy.

A client has described their project idea. Your job is to produce a thorough, structured
requirements document that a development team can act on immediately.

{rag_context}

## Client Project Description
{project_description}

---

Generate the following sections. Be specific, detailed, and professional.

### 1. PROJECT OVERVIEW
Write 3-4 paragraphs describing what this system is, who it serves, and why it matters.

### 2. KEY FEATURES
List 8-12 core features. For each feature, provide a one-sentence description.

### 3. FUNCTIONAL REQUIREMENTS
List 12-18 specific functional requirements using "The system shall..." format.

### 4. NON-FUNCTIONAL REQUIREMENTS
Cover: Performance, Scalability, Security, Availability, Usability, Maintainability.
Provide measurable criteria where possible.

### 5. USER STORIES
Write 8-10 user stories in format: "As a [role], I want to [action] so that [benefit]."
Include acceptance criteria for each story.

### 6. PROJECT SCOPE
#### In Scope
List 6-8 items explicitly included.
#### Out of Scope
List 4-6 items explicitly excluded.
#### Assumptions
List 4-5 project assumptions.
#### Constraints
List 3-4 technical or business constraints.

Output only the structured document. Do not add preamble or closing remarks.
"""


def build_requirement_prompt(project_description: str, rag_context: str = "") -> str:
    context_block = ""
    if rag_context.strip():
        context_block = f"""
## Relevant Context from Uploaded Documents
The following context was retrieved from documents the client provided.
Use it to enrich your analysis where relevant.

{rag_context}
---
"""
    return REQUIREMENT_PROMPT_TEMPLATE.format(
        project_description=project_description,
        rag_context=context_block,
    )
