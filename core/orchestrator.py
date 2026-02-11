from agents.directory_agent import DirectoryAgent
from agents.summarizer_agent import SummarizerAgent
from agents.intent_agent import IntentAgent
from agents.planner_agent import PlannerAgent
from agents.synthesizer_agent import SynthesizerAgent
from agents.critic_agent import CriticAgent
from typing import Any


class CuraOrchestrator:
    def __init__(self):
        self.directory_agent = DirectoryAgent()
        self.summarizer_agent = SummarizerAgent()
        self.intent_agent = IntentAgent()
        self.planner_agent = PlannerAgent()
        self.synthesizer_agent = SynthesizerAgent()
        self.critic_agent = CriticAgent()

    def run(self, project_path):
        print("🔍 Scanning directory...")
        structure = self.directory_agent.analyze(project_path)

        summaries: list[dict[str, Any]] = []

        for file_info in structure["files"]:
            print(f"🧠 Analyzing {file_info['file_name']}...")
            summary = self.summarizer_agent.summarize_file(file_info)
            if summary:
                summaries.append(summary)

        print("🔎 Inferring project intent...")
        intent = self.intent_agent.infer_intent(summaries)

        print("🗂 Planning README structure...")
        plan = self.planner_agent.plan_readme(intent)

        print("✍ Generating README...")
        readme = self.synthesizer_agent.generate_readme(plan, summaries, intent)

        print("🛠 Reviewing README...")
        final_readme = self.critic_agent.review_readme(readme)

        with open("README_GENERATED.md", "w", encoding="utf-8") as f:
            f.write(final_readme)

        print("\n✅ README_GENERATED.md created successfully!")

        return final_readme
