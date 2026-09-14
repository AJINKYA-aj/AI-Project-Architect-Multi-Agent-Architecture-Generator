# 🏗️ AI Project Architect

A production-quality **Multi-Agent AI System** that acts as a virtual software consulting company.
Describe any project idea and three specialized AI agents collaboratively generate a complete
software architecture and planning document — fully offline, zero paid APIs.

---

## What It Does

| Input | Output |
|---|---|
| "Build a Labour Management System" | Full requirements document |
| "Build an E-Commerce Website" | Database schema + API design |
| "Build a Hospital Portal" | Technology stack recommendation |
| Any project idea | Final consolidated architecture report |

---

## Architecture

```
User Input
    │
    ▼
┌─────────────────────────────────┐
│        RAG Pipeline             │
│  PDF → Chunks → Embeddings      │
│  → FAISS → Retrieved Context    │
└──────────────┬──────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│    Agent 1: Requirement Agent    │
│  • Project Overview              │
│  • Key Features                  │
│  • Functional Requirements       │
│  • Non-Functional Requirements   │
│  • User Stories                  │
│  • Project Scope                 │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│   Agent 2: System Design Agent   │
│  • Technology Stack              │
│  • Database Schema               │
│  • API Endpoints (20+)           │
│  • System Architecture           │
│  • Auth Strategy                 │
│  • Deployment Plan               │
└──────────────┬───────────────────┘
               │
               ▼
┌──────────────────────────────────┐
│     Agent 3: Report Agent        │
│  • Executive Summary             │
│  • Consolidated Planning Report  │
│  • Risk Assessment               │
│  • Implementation Roadmap        │
└──────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agents | LangChain + Ollama |
| LLM | Phi-3 / Llama 3.2 / Qwen 2.5 (local) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector DB | FAISS (local) |
| UI | Streamlit |
| Document Loaders | LangChain Community (PyPDF) |

---

## Folder Structure

```
AI_Project_Architect/
├── agents/
│   ├── requirement_agent.py      # Agent 1
│   ├── system_design_agent.py    # Agent 2
│   └── report_agent.py           # Agent 3
├── rag/
│   ├── loader.py                 # PDF/TXT ingestion
│   ├── splitter.py               # Text chunking
│   ├── embeddings.py             # HuggingFace embeddings
│   └── vectorstore.py            # FAISS store + retriever
├── prompts/
│   ├── requirement_prompt.py
│   ├── system_design_prompt.py
│   └── report_prompt.py
├── ui/
│   └── streamlit_app.py          # Full Streamlit UI
├── config/
│   └── settings.py               # All config in one place
├── main.py                       # Orchestrator / CLI entry
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed

### Step 1: Clone / Download the project

```bash
cd AI_Project_Architect
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install and start Ollama

```bash
# Install from https://ollama.ai
ollama serve
```

### Step 5: Pull a model

```bash
# Choose one:
ollama pull phi3
ollama pull llama3.2
ollama pull qwen2.5
```

### Step 6: Run the Streamlit app

```bash
streamlit run ui/streamlit_app.py
```

Open your browser at: **http://localhost:8501**

---

## Using the App

1. **Select a model** from the sidebar (Phi-3, Llama 3.2, or Qwen 2.5)
2. *(Optional)* Upload a PDF or TXT with business requirements — RAG will enrich the agents
3. **Describe your project** in the main text area
4. Click **Generate Architecture**
5. Watch three agents run in sequence
6. Explore results across three tabs:
   - 📝 **Requirements** — full requirements document
   - 🏛️ **System Design** — database, APIs, architecture
   - 📄 **Final Report** — executive-ready consolidated report
7. **Download** individual documents or the full combined report

---

## CLI Usage

```bash
# Run from project root
python main.py "Build a Farmer Auction Platform"
```

---

## Configuration

Edit `config/settings.py` to change:

```python
MODEL_CONFIG.default_model = "phi3"        # Default model
MODEL_CONFIG.temperature = 0.3             # LLM temperature
EMBEDDING_CONFIG.chunk_size = 1000         # RAG chunk size
EMBEDDING_CONFIG.retriever_k = 4           # Top-K retrieved chunks
```

---

## Model Guide

| Model | Size | Speed | Quality |
|---|---|---|---|
| phi3 | ~2GB | ⚡⚡⚡ Fast | Good |
| llama3.2 | ~2GB | ⚡⚡⚡ Fast | Good |
| qwen2.5 | ~5GB | ⚡⚡ Medium | Better |

For best results on complex projects, use `qwen2.5`.

---

## Portfolio Notes

This project demonstrates:
- **Multi-agent orchestration** without a cloud LLM
- **RAG pipeline** from scratch with FAISS + HuggingFace
- **Production code structure** — typed, modular, config-driven
- **Streamlit UI** — professional dark theme, real-time agent status
- **Fully offline** — suitable for air-gapped enterprise environments

Built with LangChain, Ollama, FAISS, HuggingFace Transformers, and Streamlit.
