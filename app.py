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

def apply_advanced_styling():
    st.markdown("""
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=JetBrains+Mono&display=swap');

        /* 1. Animated Gradient Background */
        .stApp {
            background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #1e1b4b);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Inter', sans-serif;
        }

        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 2. Glassmorphism for Containers */
        [data-testid="stExpander"], [data-testid="stMetric"], .stTabs {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }

        /* 3. Futuristic Glowing Title */
        h1 {
            font-family: 'Inter', sans-serif;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem !important;
            letter-spacing: -3px !important;
            margin-bottom: 0px !important;
        }

        /* 4. Styled Button with Neon Hover */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            border: none;
            color: white;
            padding: 12px 24px;      /* Increased padding for breathing room */
            border-radius: 50px;
            font-size: 14px !important; /* Decreased font size */
            font-weight: 600;           /* Semi-bold for elegance over bulk */
            letter-spacing: 0.5px;
            text-transform: uppercase;
            width: auto;                /* Let it be a natural size instead of full width */
            display: block;
            margin: 0 auto;             /* Center the button */
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
        }

        div.stButton > button:hover {
            background: #818cf8;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.6);
            transform: scale(1.01);
        }

        /* 5. Code Block Styling */
        code {
            font-family: 'JetBrains Mono', monospace !important;
            background-color: rgba(0,0,0,0.3) !important;
            color: #818cf8 !important;
        }
        </style>
    """, unsafe_allow_html=True)

apply_advanced_styling()

# ---- Page config ----
st.set_page_config(
    page_title="Cura — README Generator",
    layout="centered"
)

st.title("🧠 Cura")
st.caption("AI-powered README generation")

repo_input = st.text_input(
    "Repository",
    placeholder="Local path or GitHub URL"
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
