from core.llm import LLM

class SynthesizerAgent:
    def __init__(self):
        self.llm = LLM(model="llama-3.1-8b-instant")  # stronger model for final polish

    def generate_readme(self, plan, summaries, intent):
        combined_summaries = "\n\n".join([s["summary"] for s in summaries])

        system_prompt = """
        You are Cura, the Code Curator.

        Using:
        - The README section plan
        - The project intent analysis
        - File-level summaries

        Generate a professional, well-structured README.md
        in clean Markdown format.

        Make it polished and production-ready.
        """

        user_prompt = f"""
        README Plan:
        {plan}

        Project Intent:
        {intent}

        File Summaries:
        {combined_summaries}
        """

        return self.llm.generate(system_prompt, user_prompt)
