from core.llm import LLM
from typing import Any


class CriticAgent:
    def __init__(self):
        self.llm = LLM(model="llama-3.1-8b-instant")

    def review_readme(self, readme: str, repo_facts: dict[str, Any], repo_stats: dict[str, Any],) -> str:
        system_prompt = """
You are a strict documentation reviewer.

Your task is to refine the given README.

Your job:
- Improve clarity
- Fix logical gaps
- Improve structure

CRITICAL RULES:
- The README must ONLY describe files, functions, and behavior that exist in repository facts.
- If a file or function is not explicitly listed in repository facts, REMOVE references to it.
- Do NOT add "Future Improvements", "Roadmap", or similar sections unless they already exist.
- Do NOT assume configuration files or initialization functions.
- When in doubt, REMOVE content instead of adding it.
- Remove any CLI flags not explicitly present in the code.
- Remove any modules not listed in repository facts.
- Downgrade claims that are not directly supported by file summaries.
- If behavior cannot be proven, generalize it.

ABSOLUTE RULES:
- Output ONLY the final refined README.md content.
- Do NOT include headings like "IMPROVED README".
- The README title MUST describe the documented project.
- Do NOT use the generator's name (e.g., Cura) unless the repository facts explicitly say so. 
- If the repository does not clearly indicate a project name, use a descriptive title based on the content. 
- Do not randomly start saying "Cura is a project that..." if the repository does not clearly indicate that.
- Do NOT include explanations, change logs, or commentary.
- Do NOT include repository facts or analysis sections.
- Do NOT invent features, commands, dependencies, or architecture claims.
- Do NOT add new sections that did not already exist.
- Only improve wording, clarity, and structure of existing sections.
- If a section is incorrect, remove it silently.
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

=========================
REPOSITORY STATISTICS
=========================
Total Python files: {repo_stats.get("total_python_files")}
Entry points: {repo_stats.get("entry_points")}

Your task:
- Refine the README according to the rules above.
- Improve clarity and structure
- Ensure the README title reflects the documented application, not the generator
- Remove any mention of Cura unless it is the documented project
- Remove incorrect or unsupported content silently.
- Do NOT add anything new.
"""

        return self.llm.generate(system_prompt, user_prompt)
