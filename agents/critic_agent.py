from core.llm import LLM
from typing import Any


class CriticAgent:
    def __init__(self):
        self.llm = LLM(model="llama-3.1-8b-instant")

    def review_readme(self, readme: str, repo_facts: dict[str, Any]) -> str:
        system_prompt = """
You are a strict documentation reviewer.

Your job:
- Improve clarity
- Fix logical gaps
- Improve structure

CRITICAL RULES:
- Do NOT invent features.
- Do NOT invent dependencies.
- Do NOT invent commands.
- Do NOT add sections not supported by repository facts.
- Output ONLY the final refined README.
- Do NOT include explanations of what you changed.
- Do NOT include review commentary.
- Only refine what exists.
- If something does not exist in repo facts, do not add it.
"""

        user_prompt = f"""
=========================
CURRENT README
=========================
{readme}

=========================
REPOSITORY FACTS
=========================
Has requirements.txt: {repo_facts.get("has_requirements")}
Has LICENSE file: {repo_facts.get("has_license")}
Entry points: {repo_facts.get("entry_points")}
Python files: {repo_facts.get("python_files")}

Your task:
- Improve clarity and structure
- Remove incorrect claims
- Do NOT add new fictional features
"""

        return self.llm.generate(system_prompt, user_prompt)
