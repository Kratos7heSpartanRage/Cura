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

┌─────────────────────────────────────────────────────────────┐
│ Cura Pipeline │
├───────────────┬─────────────────────────────────────────────┤
│ Directory │ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ Scan │ │ Repo │ │ Repo │ │ File │ │
│ │ │ Facts │ │ Stats │ │Summaries│ │
├───────────────┤ └─────────┘ └─────────┘ └─────────┘ │
│ Analysis │ ↓ ↓ ↓ │
│ │ ┌─────────────────────────────────┐ │
│ Layer │ │ Intent Agent │ │
│ │ │ (Project Purpose & Type) │ │
│ │ └─────────────────────────────────┘ │
├───────────────┤ ↓ │
│ Planning │ ┌─────────────────────────────────┐ │
│ │ │ Planner Agent │ │
│ Layer │ │ (README Structure Design) │ │
│ │ └─────────────────────────────────┘ │
├───────────────┤ ↓ │
│ Generation │ ┌─────────────────────────────────┐ │
│ │ │ Synthesizer Agent │ │
│ Layer │ │ (README Content Creation) │ │
│ │ └─────────────────────────────────┘ │
├───────────────┤ ↓ │
│ Review │ ┌─────────────────────────────────┐ │
│ │ │ Critic Agent │ │
│ Layer │ │ (Validation & Refinement) │ │
│ │ └─────────────────────────────────┘ │
└───────────────┴─────────────────────────────────────────────┘
