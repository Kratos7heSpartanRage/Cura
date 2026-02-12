import sys
from pathlib import Path
import tempfile
import subprocess
import shutil

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

import streamlit as st

from agents.directory_agent import DirectoryAgent
from agents.summarizer_agent import SummarizerAgent
from agents.intent_agent import IntentAgent
from agents.planner_agent import PlannerAgent
from agents.synthesizer_agent import SynthesizerAgent
from agents.critic_agent import CriticAgent

from core.repo_facts import RepoFactsExtractor
from core.summary_compressor import compress_summaries

# ---- Page config ----
st.set_page_config(
    page_title="Cura — README Generator",
    layout="centered"
)

st.title("🧠 Cura")
st.caption("AI-powered README generation")

repo_input = st.text_input(
    "Repository (Local path or GitHub URL)",
    placeholder="e.g. ./my_project or https://github.com/user/repo"
)

def prepare_repo(repo_input: str) -> str:
    if repo_input.startswith("http://") or repo_input.startswith("https://"):
        temp_dir = tempfile.mkdtemp(prefix="cura_")
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_input, temp_dir],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return temp_dir
    return repo_input

generate = st.button("Generate README")

if generate:
    if not repo_input.strip():
        st.error("Please provide a valid local path or GitHub repository URL.")
        st.stop()

    repo_path = prepare_repo(repo_input)

    with st.status("Running Cura pipeline...", expanded=True) as status:

        # ---- Step 1: Directory Scan ----
        st.write("📁 Scanning directory...")
        dir_agent = DirectoryAgent()
        directory_result = dir_agent.analyze(repo_path)
        st.success("Directory scanned")

        st.expander("Directory Structure").json(directory_result)

        # ---- Step 2: Repo Facts ----
        st.write("📊 Extracting repository facts...")
        facts_extractor = RepoFactsExtractor(repo_path)
        repo_facts = facts_extractor.extract()
        st.success("Repository facts extracted")

        st.expander("Repository Facts").json(repo_facts)

        # ---- Step 3: File Summaries (VERBOSE) ----
        st.write("🧠 Summarizing files...")
        summarizer = SummarizerAgent()
        raw_summaries = []

        for file_info in directory_result.get("files", []):
            summary = summarizer.summarize_file(file_info)
            if summary:
                raw_summaries.append(summary)

        st.success(f"Generated {len(raw_summaries)} file summaries")

        # ---- Step 4: Compress Summaries (CRITICAL) ----
        compressed_summaries = compress_summaries(raw_summaries)
        st.success("Summaries compressed for downstream agents")

        st.expander("Compressed File Roles").json(compressed_summaries)

        # ---- Step 5: Intent Analysis ----
        st.write("🎯 Inferring project intent...")
        intent_agent = IntentAgent()
        intent = intent_agent.infer_intent(compressed_summaries)
        st.success("Intent inferred")

        st.expander("Project Intent").markdown(intent)

        # ---- Step 6: README Planning ----
        st.write("🗂 Planning README...")
        planner = PlannerAgent()
        plan = planner.plan_readme(intent)
        st.success("README plan created")

        st.expander("README Plan").markdown(plan)

        # ---- Step 7: Repo Statistics ----
        st.write("📈 Computing repository statistics...")
        repo_stats = {
            "total_files": len(directory_result.get("files", [])),
            "python_files": len(repo_facts.get("python_files", [])),
            "entry_points": len(repo_facts.get("entry_points", [])),
            "directories": len(repo_facts.get("directory_structure", [])),
        }
        st.success("Repository statistics computed")

        st.expander("Repository Statistics").json(repo_stats)

        # ---- Step 8: README Generation ----
        st.write("✍ Generating README...")
        synthesizer = SynthesizerAgent()
        readme_draft = synthesizer.generate_readme(
            plan=plan,
            summaries=compressed_summaries,
            intent=intent,
            repo_facts=repo_facts,
            repo_stats=repo_stats,
        )
        st.success("README generated")

        # ---- Step 9: Critic Review ----
        st.write("🛠 Reviewing README...")
        critic = CriticAgent()
        final_readme = critic.review_readme(
            readme_draft,
            repo_facts,
            repo_stats
        )
        st.success("README polished")

        status.update(label="Pipeline complete", state="complete")

    st.divider()
    st.subheader("📄 Final README")

    tab1, tab2 = st.tabs(["Preview", "Raw Markdown"])

    with tab1:
        st.markdown(final_readme)

    with tab2:
        st.code(final_readme, language="markdown")

    st.download_button(
        "⬇ Download README.md",
        final_readme,
        file_name="README.md",
        mime="text/markdown",
    )

    # ---- Cleanup ----
    if repo_input.startswith("http"):
        shutil.rmtree(repo_path, ignore_errors=True)
