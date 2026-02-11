from core.llm import LLM

class CriticAgent:
    def __init__(self):
        self.llm = LLM()

    def review_readme(self, readme_content):
        system_prompt = """
        You are Cura's Critic Agent.

        Review the README and check for:
        - Missing sections
        - Logical gaps
        - Weak installation instructions
        - Clarity issues
        - Missing usage examples

        If improvements are needed, rewrite the README with fixes.
        Otherwise return the original.
        """

        user_prompt = f"""
        README Content:
        {readme_content}
        """

        return self.llm.generate(system_prompt, user_prompt)
