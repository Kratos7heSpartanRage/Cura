from core.llm import LLM
from typing import Any


class SynthesizerAgent:
    def __init__(self):
        # Balanced + fast model
        self.llm = LLM(model="llama-3.1-8b-instant")

    def generate_readme(
        self,
        plan: str,
        summaries: list[dict[str, Any]],
        intent: str,
        repo_facts: dict[str, Any],
        repo_stats: dict[str, Any],
    ) -> str:

        # Combine file summaries safely
        combined_summaries = "\n\n".join(
            [s.get("summary", "") for s in summaries]
        )

        system_prompt = """
You are Cura, the Code Curator.

You generate professional README.md files for software projects.

CRITICAL RULES:
- Do NOT hallucinate dependencies.
- Do NOT invent files.
- Do NOT assume a license unless explicitly told.
- Do NOT fabricate CLI outputs.
- Base everything strictly on the provided repository facts and summaries.
- If something does not exist, do not mention it.
- If no requirements.txt exists: Mention that no external dependencies are required. Do NOT say installation steps are unavailable.
- The following sections are INTERNAL CONTEXT and MUST NOT appear in the final README:
  - README PLAN
  - PROJECT INTENT
  - FILE SUMMARIES
  - REPOSITORY FACTS
- Output ONLY the final README.md content.

ABSOLUTE RULES:
- Do NOT describe CLI flags unless explicitly present in code.
- Do NOT describe directories unless they exist in repository facts.
- Do NOT describe reports unless file summaries confirm report generation.

Your output must be:
- Clean Markdown
- Well structured
- Professional
- Accurate
"""

        user_prompt = f"""
===============================
README PLAN
===============================
{plan}

===============================
PROJECT INTENT
===============================
{intent}

===============================
FILE SUMMARIES
===============================
{combined_summaries}

===============================
REPOSITORY FACTS (GROUND TRUTH)
===============================
Has requirements.txt: {repo_facts.get("has_requirements")}
Has LICENSE file: {repo_facts.get("has_license")}
Existing README present: {repo_facts.get("has_readme")}
Entry points: {repo_facts.get("entry_points")}
Python files: {repo_facts.get("python_files")}
Directory structure: {repo_facts.get("directory_structure")}

===============================
REPOSITORY STATISTICS
===============================
Total Python files: {repo_stats.get("total_python_files")}
Total directories: {repo_stats.get("total_directories")}
Entry points: {repo_stats.get("entry_points")}

Infer a strong, descriptive project title based on:
- Project intent
- Entry points
- Core functionality

Do not use generic titles like "Project Title".

If the repository appears to be a demo, example, or test project,
clearly state that in the Overview.

IMPORTANT:
- Only describe installation steps if requirements.txt exists.
- Only describe a license if one exists.
- Do not invent example CLI outputs.
- Keep the README accurate and grounded in reality.
"""

        return self.llm.generate(system_prompt, user_prompt)
