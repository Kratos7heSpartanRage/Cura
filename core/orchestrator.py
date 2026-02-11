from agents.directory_agent import DirectoryAgent
from agents.summarizer_agent import SummarizerAgent
from agents.intent_agent import IntentAgent
from agents.planner_agent import PlannerAgent
from agents.synthesizer_agent import SynthesizerAgent
from agents.critic_agent import CriticAgent

from core.repo_facts import RepoFactsExtractor

from typing import Any


class CuraOrchestrator:
    def __init__(self):
        self.directory_agent = DirectoryAgent()
        self.summarizer_agent = SummarizerAgent()
        self.intent_agent = IntentAgent()
        self.planner_agent = PlannerAgent()
        self.synthesizer_agent = SynthesizerAgent()
        self.critic_agent = CriticAgent()

    def run(self, project_path: str) -> str:
        print("🔍 Scanning directory...")
        structure = self.directory_agent.analyze(project_path)

        # ---------------------------
        # 🧠 Extract Ground Truth Facts
        # ---------------------------
        print("📊 Extracting repository facts...")
        facts_extractor = RepoFactsExtractor(project_path)
        repo_facts = facts_extractor.extract()

        summaries: list[dict[str, Any]] = []

        # ---------------------------
        # 📄 File Summarization
        # ---------------------------
        for file_info in structure["files"]:
            print(f"🧠 Analyzing {file_info['file_name']}...")
            summary = self.summarizer_agent.summarize_file(file_info)

            if summary:
                summaries.append(summary)

        # ---------------------------
        # 🎯 Intent Inference
        # ---------------------------
        print("🔎 Inferring project intent...")
        intent = self.intent_agent.infer_intent(summaries)

        # ---------------------------
        # 🗂 README Planning
        # ---------------------------
        print("🗂 Planning README structure...")
        plan = self.planner_agent.plan_readme(intent)

        # ---------------------------
        # ✍ README Generation (Grounded)
        # ---------------------------
        print("✍ Generating README...")
        readme = self.synthesizer_agent.generate_readme(
            plan,
            summaries,
            intent,
            repo_facts,   # <-- Injected grounded facts
        )

        # ---------------------------
        # 🛠 Critic / Reviewer
        # ---------------------------
        print("🛠 Reviewing README...")
        final_readme = self.critic_agent.review_readme(readme, repo_facts)

        # ---------------------------
        # 💾 Save Output
        # ---------------------------
        with open("README_GENERATED.md", "w", encoding="utf-8") as f:
            f.write(final_readme or "")

        print("\n✅ README_GENERATED.md created successfully!")

        return final_readme
