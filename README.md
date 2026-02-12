# 🧠 Cura — AI-Powered README Generator

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)

**Cura (Code Curator) is an intelligent multi-agent system that automatically generates comprehensive, accurate README.md files for any software repository.**

[Features](#-features) • [Architecture](#-architecture) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Visual Pipeline](#-visual-pipeline) • [Configuration](#-configuration) • [Contributing](#-contributing) • [License](#-license)

</div>

---

## 📋 Overview

Cura analyzes your codebase using a sophisticated **multi-agent pipeline**, extracting ground truth directly from your repository to generate documentation that is:

- ✅ **Accurate** — Never hallucinates features, files, or dependencies
- ✅ **Complete** — Covers installation, usage, architecture, and more  
- ✅ **Professional** — Clean markdown formatting with proper structure
- ✅ **Transparent** — Shows its work at every step for complete visibility

Unlike traditional documentation generators that simply parse docstrings, Cura **understands the intent and architecture** of your project through multiple specialized AI agents working in concert.

---

## ✨ Features

### 🎯 **Intelligent Code Analysis**
- **Deep File Understanding** — Each Python file is analyzed for its role, functionality, and relationships
- **Entry Point Detection** — Automatically identifies main scripts and CLI entry points
- **Dependency Mapping** — Detects requirements and external libraries
- **Framework Recognition** — Identifies Flask, Django, FastAPI, and other frameworks

### 📊 **Multi-Agent Architecture**
| Agent | Responsibility |
|-------|---------------|
| **DirectoryAgent** | Scans repository structure |
| **SummarizerAgent** | Analyzes individual files |
| **IntentAgent** | Infers project purpose |
| **PlannerAgent** | Designs README structure |
| **SynthesizerAgent** | Generates initial README |
| **CriticAgent** | Reviews and refines |
| **RepoStatsAgent** | Computes metrics |

### 🚀 **Production-Ready Output**
- **No Hallucinations** — Strict grounding in actual repository facts
- **Section Optimization** — Only includes supported sections
- **License Awareness** — Respects actual project licensing
- **Installation Accuracy** — Only shows steps that actually work

### 🔍 **Complete Visibility**
Every step of the pipeline is **fully transparent**:
- 📁 Directory structure scan results
- 📊 Extracted repository facts
- 🧠 File-by-file analysis summaries
- 🎯 Inferred project intent
- 🗂 Generated README plan
- 📈 Repository statistics
- 🛠 Critic review changes

---

## 🏗 Architecture

Cura/
├── agents/                  # The AI Workforce
│   ├── critic_agent.py      # Final reviewer (quality gate)
│   ├── directory_agent.py   # Analyzes file structure
│   ├── intent_agent.py      # Infers project purpose
│   ├── planner_agent.py     # Outlines README sections
│   ├── summarizer_agent.py  # Summarizes individual files
│   └── synthesizer_agent.py # Generates the Markdown draft
├── core/                    # The Foundational Logic
│   ├── llm.py               # Groq/Llama API client
│   ├── orchestrator.py      # Manages agent hand-offs
│   ├── repo_facts.py        # Static analysis & ground truth
│   └── summary_compressor.py# Prepares data for synthesis
├── tools/                   # Utility Scripts
│   └── file_scanner.py      # Directory traversal logic
├── demo_app/                # Your test project folder
├── .env                     # API keys (DO NOT GIT COMMIT)
├── .gitignore               # Ignores venv, .env, __pycache__
├── main.py                  # Streamlit UI & Entry Point
└── requirements.txt         # Project dependencies


---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- [Groq API key](https://console.groq.com/) (free tier available)

### Option 1: Install from PyPI
```bash
pip install cura-readme-generator
```
### Option 2: Install from source

# Clone the repository
```bash
git clone https://github.com/yourusername/cura.git
cd cura
```
# Create virtual environment
```bash
python -m venv cura-env
source cura-env/bin/activate  # On Windows: cura-env\Scripts\activate
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Set up environment variables
```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

## 🚀 Usage
Generate a README for any local project:

```bash
# Basic usage
python main.py --path /path/to/your/project

# Output is saved as README_GENERATED.md in current directory
```

## 🌐 Web Interface (Streamlit)
```bash
streamlit run app.py
```
Then:
1. Enter a local path or GitHub URL
2. Click "Generate README"
3. Watch the pipeline execute in real-time
4. Preview, edit, and download your README

## How It Works:
