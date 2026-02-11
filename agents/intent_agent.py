from core.llm import LLM

class IntentAgent:
    def __init__(self):
        self.llm = LLM()

    def infer_intent(self, summaries):
        combined = "\n\n".join(
            s.get("summary", "") for s in summaries if isinstance(s, dict)
        )

        system_prompt = """
        You are Cura's Intent Analysis Agent.
        Your job is to analyze file-level summaries and infer:

        - Overall project purpose
        - Target audience
        - Type of application (CLI, API, library, web app, etc.)
        - Core features
        - High-level architecture style

        Respond in structured markdown.
        """

        user_prompt = f"""
        File Summaries:
        {combined}
        """

        result = self.llm.generate(system_prompt, user_prompt)

        return result
