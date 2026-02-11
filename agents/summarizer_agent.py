# agents/summarizer_agent.py

from core.llm import LLM
from typing import Optional, Dict

class SummarizerAgent:
    def __init__(self):
        self.llm = LLM()

    def summarize_file(self, file_info) -> Optional[Dict[str, str]]:
        try:
            with open(file_info["path"], "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return None

        if len(content.strip()) == 0:
            return None

        # Prevent token explosion
        content = content[:8000]

        system_prompt = """
        You are Cura, an expert code analyst.
        Your task is to analyze a source file and extract:
        - Its role in the project
        - Main functionality
        - Key components (functions/classes)
        - Whether it is likely an entry point
        Respond in structured markdown.
        """

        user_prompt = f"""
        File Name: {file_info['file_name']}
        File Path: {file_info['path']}
        File Content:
        {content}
        """

        summary = self.llm.generate(system_prompt, user_prompt)

        return {
            "file": file_info["file_name"],
            "path": file_info["path"],
            "summary": summary
        }
