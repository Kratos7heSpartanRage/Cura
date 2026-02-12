from core.llm import LLM

class PlannerAgent:
    def __init__(self):
        self.llm = LLM()

    def plan_readme(self, intent_analysis):
        system_prompt = """
        You are Cura's README Planning Agent.

        Based on the project analysis, decide:

        - Which README sections are needed
        - Their order
        - What content each section should contain

        Sections may include:
        - Title
        - Overview
        - Features
        - Tech Stack
        - Installation
        - Usage
        - Project Structure
        - Configuration
        - Contributing
        - Limitations
        - Future Improvements

        Only include sections that can be directly supported by repository files.
        Avoid generic boilerplate sections.

        Return a structured section plan.
        """

        user_prompt = f"""
        Project Analysis:
        {intent_analysis}
        """

        return self.llm.generate(system_prompt, user_prompt)
