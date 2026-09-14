"""
AI Project Architect — Streamlit UI.
Professional multi-agent software architecture generator.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit import session_state as ss

from config.settings import MODEL_CONFIG, APP_CONFIG
from rag import (
    load_documents_from_upload,
    split_documents,
    build_vectorstore,
    retrieve_context,
)

# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_CONFIG.title,
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%); }

    [data-testid="stSidebar"] {
        background: #12151f;
        border-right: 1px solid #2d3142;
    }

    .hero-header {
        background: linear-gradient(135deg, #1e2540 0%, #151829 100%);
        border: 1px solid #2d3a5e;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%; right: -10%;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a78bfa 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-top: 0.5rem;
    }

    .badge {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        color: #a78bfa;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        margin-bottom: 1rem;
    }

    .section-card {
        background: #1a1f2e;
        border: 1px solid #2d3142;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
    }

    .section-card-title {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6366f1;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .agent-card {
        background: #1a1f2e;
        border: 1px solid #2d3142;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.4rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .agent-card.active {
        border-color: #6366f1;
        background: rgba(99,102,241,0.05);
        animation: pulse-border 1.5s infinite;
    }

    @keyframes pulse-border {
        0%,100% { border-color: #6366f1; }
        50%      { border-color: #a78bfa; }
    }

    .agent-card.done {
        border-color: #10b981;
        background: rgba(16,185,129,0.05);
    }

    .agent-icon { font-size: 1.5rem; min-width: 2rem; text-align: center; }

    .agent-info h4 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 600;
        color: #e2e8f0;
    }

    .agent-info p {
        margin: 0;
        font-size: 0.75rem;
        color: #64748b;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: #12151f;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #2d3142;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #64748b;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.5rem 1.25rem;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: #6366f1 !important;
        color: white !important;
    }

    .stTextArea textarea {
        background: #1a1f2e !important;
        border: 1px solid #2d3142 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.75rem 2rem;
        width: 100%;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 25px rgba(99,102,241,0.4);
    }

    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }

    .sidebar-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #4b5563;
        margin: 1.5rem 0 0.5rem 0;
    }

    .info-box {
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.2);
        border-radius: 8px;
        padding: 0.65rem 1rem;
        font-size: 0.78rem;
        color: #7dd3fc;
        margin: 0.4rem 0;
    }

    .rag-active {
        background: rgba(16,185,129,0.08);
        border: 1px solid rgba(16,185,129,0.25);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.78rem;
        color: #6ee7b7;
        margin: 0.4rem 0;
    }

    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        flex: 1;
        background: #1a1f2e;
        border: 1px solid #2d3142;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #6366f1;
    }

    .metric-label {
        font-size: 0.72rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.2rem;
    }

    .download-row {
        display: flex;
        gap: 0.75rem;
        margin-top: 1rem;
    }

    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
    }

    .empty-state .icon { font-size: 4rem; margin-bottom: 1rem; }

    .empty-state .title {
        font-size: 1.15rem;
        color: #4b5563;
        margin-bottom: 0.5rem;
    }

    .empty-state .subtitle { font-size: 0.85rem; color: #374151; }

    .pipeline-header {
        background: #12151f;
        border: 1px solid #2d3142;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0 1rem 0;
    }

    .pipeline-header h3 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
        color: #94a3b8;
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; }

    /* expander */
    .streamlit-expanderHeader {
        background: #1a1f2e !important;
        border: 1px solid #2d3142 !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-size: 0.88rem !important;
    }

    .streamlit-expanderContent {
        background: #12151f !important;
        border: 1px solid #2d3142 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Session state init
# ─────────────────────────────────────────────────────────────
def _init():
    defaults = {
        "requirements": "",
        "system_design": "",
        "final_report": "",
        "vectorstore": None,
        "uploaded_filename": None,
        "pipeline_ran": False,
        "pipeline_running": False,
        "last_project": "",
        "last_model": "",
    }
    for k, v in defaults.items():
        if k not in ss:
            ss[k] = v

_init()


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:1.25rem 0 0.5rem;'>
            <div style='font-size:2.8rem;'>🏗️</div>
            <div style='font-size:1.05rem; font-weight:700; color:#e2e8f0; margin-top:0.4rem;'>
                AI Project Architect
            </div>
            <div style='font-size:0.72rem; color:#4b5563; margin-top:0.2rem;'>
                Multi-Agent System
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Model ──
    st.markdown("<div class='sidebar-label'>🤖 Language Model</div>", unsafe_allow_html=True)
    selected_model = st.selectbox(
        "model",
        options=MODEL_CONFIG.available_models,
        index=MODEL_CONFIG.available_models.index(MODEL_CONFIG.default_model),
        label_visibility="collapsed",
    )
    st.markdown(
        "<div class='info-box'>Requires Ollama running locally.<br/>Pull model first: <code>ollama pull phi3</code></div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── RAG Upload ──
    st.markdown("<div class='sidebar-label'>📄 Context Documents (RAG)</div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.75rem;color:#4b5563;margin-bottom:0.5rem;'>Upload PDFs or text files to enrich agent analysis</div>",
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload PDF or TXT",
        type=["pdf", "txt", "md"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        if ss.uploaded_filename != uploaded_file.name:
            with st.spinner("Indexing document..."):
                try:
                    raw = uploaded_file.read()
                    docs = load_documents_from_upload(raw, uploaded_file.name)
                    chunks = split_documents(docs)
                    ss.vectorstore = build_vectorstore(chunks)
                    ss.uploaded_filename = uploaded_file.name
                    st.success(f"✅ {len(chunks)} chunks indexed")
                except Exception as e:
                    st.error(f"Error: {e}")

    if ss.vectorstore is not None:
        st.markdown(
            f"<div class='rag-active'>📚 RAG Active<br/><span style='color:#4ade80;font-weight:600;'>{ss.uploaded_filename}</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='font-size:0.75rem;color:#374151;margin-top:0.4rem;'>No document uploaded — agents will use project description only</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Pipeline info ──
    st.markdown("<div class='sidebar-label'>⚙️ Pipeline</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.78rem; color:#4b5563; line-height:2.2;'>
        <span style='color:#6366f1;'>●</span> Agent 1 — Requirements<br/>
        <span style='color:#8b5cf6;'>●</span> Agent 2 — System Design<br/>
        <span style='color:#10b981;'>●</span> Agent 3 — Final Report<br/>
        <br/>
        <span style='color:#374151;'>Embeddings:</span> MiniLM-L6-v2<br/>
        <span style='color:#374151;'>Vector DB:</span> FAISS (local)
    </div>
    """, unsafe_allow_html=True)

    if ss.pipeline_ran:
        st.markdown("---")
        st.markdown("<div class='sidebar-label'>📌 Last Run</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:0.75rem;color:#4b5563;'>"
            f"Model: <span style='color:#a78bfa;'>{ss.last_model}</span><br/>"
            f"Project: <span style='color:#94a3b8;'>{ss.last_project[:40]}{'...' if len(ss.last_project)>40 else ''}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-header'>
    <div class='badge'>Multi-Agent AI System</div>
    <h1 class='hero-title'>AI Project Architect</h1>
    <p class='hero-subtitle'>
        Describe any software project. Three specialized AI agents collaborate to generate
        a complete requirements document, system design, and architecture report — fully offline.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Input area
# ─────────────────────────────────────────────────────────────
col_input, col_examples = st.columns([3, 1], gap="medium")

with col_input:
    st.markdown(
        "<div style='font-size:0.8rem;color:#64748b;margin-bottom:0.4rem;font-weight:500;'>📝 Project Description</div>",
        unsafe_allow_html=True,
    )
    project_description = st.text_area(
        "project_desc",
        placeholder=(
            "e.g. Build a Labour Contractor Management System for managing workers, "
            "attendance, daily wages, and contractor relationships across multiple construction sites."
        ),
        height=130,
        label_visibility="collapsed",
    )

with col_examples:
    st.markdown("""
    <div style='padding:0.5rem 0;'>
        <div style='font-size:0.75rem;color:#64748b;font-weight:600;margin-bottom:0.6rem;'>
            💡 Example Ideas
        </div>
        <div style='font-size:0.76rem;color:#4b5563;line-height:2.1;'>
            🏗️ Labour Management<br/>
            🛒 E-Commerce Platform<br/>
            🏥 Hospital Management<br/>
            🌾 Farmer Auction Portal<br/>
            📚 LMS / EdTech App<br/>
            🏦 Banking Portal<br/>
            🚗 Fleet Management<br/>
            📦 Inventory System
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Generate button ──
btn_col, _ = st.columns([1, 2])
with btn_col:
    generate_clicked = st.button(
        "🚀  Generate Architecture",
        disabled=ss.pipeline_running,
    )


# ─────────────────────────────────────────────────────────────
# Pipeline execution
# ─────────────────────────────────────────────────────────────
if generate_clicked:
    if not project_description.strip():
        st.warning("⚠️ Please describe your project before generating.")
    else:
        ss.pipeline_running = True
        ss.pipeline_ran = False
        ss.requirements = ss.system_design = ss.final_report = ""

        st.markdown("""
        <div class='pipeline-header'>
            <h3>⚙️ Running Multi-Agent Pipeline</h3>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        def agent_card(col, icon, name, status, state=""):
            col.markdown(
                f"<div class='agent-card {state}'>"
                f"<div class='agent-icon'>{icon}</div>"
                f"<div class='agent-info'><h4>{name}</h4><p>{status}</p></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        s1 = c1.empty()
        s2 = c2.empty()
        s3 = c3.empty()

        with s1.container():
            st.markdown("""<div class='agent-card active'><div class='agent-icon'>🔵</div>
            <div class='agent-info'><h4>Requirement Agent</h4><p>Analyzing requirements...</p></div></div>""",
            unsafe_allow_html=True)
        with s2.container():
            st.markdown("""<div class='agent-card'><div class='agent-icon'>🟣</div>
            <div class='agent-info'><h4>Design Agent</h4><p>Waiting...</p></div></div>""",
            unsafe_allow_html=True)
        with s3.container():
            st.markdown("""<div class='agent-card'><div class='agent-icon'>🟢</div>
            <div class='agent-info'><h4>Report Agent</h4><p>Waiting...</p></div></div>""",
            unsafe_allow_html=True)

        progress_bar = st.progress(0, text="Starting pipeline...")

        try:
            from agents import RequirementAgent, SystemDesignAgent, ReportAgent

            # RAG context
            rag_context = ""
            if ss.vectorstore is not None:
                rag_context = retrieve_context(ss.vectorstore, project_description)

            # ── Agent 1 ──
            progress_bar.progress(10, text="Agent 1: Analyzing requirements...")
            with st.spinner(""):
                req_agent = RequirementAgent(model_name=selected_model)
                ss.requirements = req_agent.run(project_description, rag_context)
            progress_bar.progress(35, text="Agent 1 complete ✓")

            s1.markdown("""<div class='agent-card done'><div class='agent-icon'>✅</div>
            <div class='agent-info'><h4>Requirement Agent</h4><p>Requirements generated</p></div></div>""",
            unsafe_allow_html=True)
            s2.markdown("""<div class='agent-card active'><div class='agent-icon'>🟣</div>
            <div class='agent-info'><h4>Design Agent</h4><p>Designing architecture...</p></div></div>""",
            unsafe_allow_html=True)

            # ── Agent 2 ──
            progress_bar.progress(40, text="Agent 2: Designing system architecture...")
            with st.spinner(""):
                design_agent = SystemDesignAgent(model_name=selected_model)
                ss.system_design = design_agent.run(ss.requirements)
            progress_bar.progress(70, text="Agent 2 complete ✓")

            s2.markdown("""<div class='agent-card done'><div class='agent-icon'>✅</div>
            <div class='agent-info'><h4>Design Agent</h4><p>Architecture designed</p></div></div>""",
            unsafe_allow_html=True)
            s3.markdown("""<div class='agent-card active'><div class='agent-icon'>🟢</div>
            <div class='agent-info'><h4>Report Agent</h4><p>Compiling report...</p></div></div>""",
            unsafe_allow_html=True)

            # ── Agent 3 ──
            progress_bar.progress(75, text="Agent 3: Compiling final report...")
            with st.spinner(""):
                report_agent = ReportAgent(model_name=selected_model)
                ss.final_report = report_agent.run(ss.requirements, ss.system_design)
            progress_bar.progress(100, text="Pipeline complete ✅")

            s3.markdown("""<div class='agent-card done'><div class='agent-icon'>✅</div>
            <div class='agent-info'><h4>Report Agent</h4><p>Report ready</p></div></div>""",
            unsafe_allow_html=True)

            ss.pipeline_ran = True
            ss.last_project = project_description
            ss.last_model = selected_model
            st.success("✅ Architecture generation complete! Scroll down to view results.")

        except Exception as e:
            st.error(f"❌ Pipeline error: {e}")
            st.info(
                "Troubleshooting:\n"
                "1. Make sure Ollama is running: `ollama serve`\n"
                f"2. Make sure the model is pulled: `ollama pull {selected_model}`\n"
                "3. Check that port 11434 is accessible"
            )
        finally:
            ss.pipeline_running = False


# ─────────────────────────────────────────────────────────────
# Output section
# ─────────────────────────────────────────────────────────────
if ss.pipeline_ran:
    st.markdown("---")

    # ── Stats row ──
    req_words   = len(ss.requirements.split())
    design_words = len(ss.system_design.split())
    report_words = len(ss.final_report.split())
    total_words  = req_words + design_words + report_words

    st.markdown(f"""
    <div class='metric-row'>
        <div class='metric-card'>
            <div class='metric-value'>{req_words:,}</div>
            <div class='metric-label'>Requirement Words</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>{design_words:,}</div>
            <div class='metric-label'>Design Words</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>{report_words:,}</div>
            <div class='metric-label'>Report Words</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>{total_words:,}</div>
            <div class='metric-label'>Total Generated</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2, tab3 = st.tabs([
        "📝  Requirements",
        "🏛️  System Design",
        "📄  Final Report",
    ])

    # ════════════════════════════════
    # TAB 1 — Requirements
    # ════════════════════════════════
    with tab1:
        st.markdown("### 📝 Requirements Analysis")
        st.markdown(
            "<p style='color:#64748b;font-size:0.88rem;'>Generated by <b style='color:#6366f1;'>Requirement Agent</b> — covers project overview, features, user stories, and full scope definition.</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Render full content
        st.markdown(ss.requirements)

        st.markdown("---")

        # Raw view toggle
        with st.expander("🔍 View Raw Text"):
            st.code(ss.requirements, language="markdown")

        # Download
        st.download_button(
            label="⬇️ Download Requirements (Markdown)",
            data=ss.requirements,
            file_name="requirements_analysis.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # ════════════════════════════════
    # TAB 2 — System Design
    # ════════════════════════════════
    with tab2:
        st.markdown("### 🏛️ System Architecture Design")
        st.markdown(
            "<p style='color:#64748b;font-size:0.88rem;'>Generated by <b style='color:#8b5cf6;'>System Design Agent</b> — covers database schema, API endpoints, tech stack, auth, and deployment.</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Split into sub-sections with cards for easier reading
        design_text = ss.system_design

        # Tech Stack section highlight
        sections_map = {
            "RECOMMENDED TECHNOLOGY STACK": ("💻", "Technology Stack"),
            "DATABASE SCHEMA":              ("🗄️",  "Database Schema"),
            "API ENDPOINTS":                ("🔌", "API Endpoints"),
            "SYSTEM ARCHITECTURE":          ("🏗️", "System Architecture"),
            "AUTHENTICATION":               ("🔐", "Auth & Security"),
            "DEPLOYMENT":                   ("🚀", "Deployment Architecture"),
        }

        # Try to detect and highlight known sections with a card header
        rendered_sections = set()
        lines = design_text.split("\n")
        current_chunk = []
        current_label = None

        def flush_chunk(label, chunk_lines):
            content = "\n".join(chunk_lines).strip()
            if not content:
                return
            icon = "📌"
            display = label or "Details"
            for key, (ic, disp) in sections_map.items():
                if key in (label or "").upper():
                    icon, display = ic, disp
                    break
            st.markdown(
                f"<div class='section-card-title'>{icon} &nbsp; {display}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(content)
            st.markdown("")

        for line in lines:
            stripped = line.strip()
            is_heading = stripped.startswith("###") and len(stripped) > 4
            if is_heading:
                flush_chunk(current_label, current_chunk)
                current_label = stripped.lstrip("#").strip()
                current_chunk = []
            else:
                current_chunk.append(line)

        flush_chunk(current_label, current_chunk)

        st.markdown("---")
        with st.expander("🔍 View Raw Text"):
            st.code(ss.system_design, language="markdown")

        st.download_button(
            label="⬇️ Download System Design (Markdown)",
            data=ss.system_design,
            file_name="system_design.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # ════════════════════════════════
    # TAB 3 — Final Report
    # ════════════════════════════════
    with tab3:
        st.markdown("### 📄 Final Software Planning Report")
        st.markdown(
            "<p style='color:#64748b;font-size:0.88rem;'>Generated by <b style='color:#10b981;'>Report Agent</b> — executive-ready consolidated document with risk assessment and implementation roadmap.</p>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        st.markdown(ss.final_report)

        st.markdown("---")

        with st.expander("🔍 View Raw Text"):
            st.code(ss.final_report, language="markdown")

        col_dl1, col_dl2 = st.columns(2)

        with col_dl1:
            st.download_button(
                label="⬇️ Download Final Report",
                data=ss.final_report,
                file_name="architecture_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with col_dl2:
            full_bundle = (
                f"# Requirements Analysis\n\n{ss.requirements}\n\n"
                f"---\n\n# System Design\n\n{ss.system_design}\n\n"
                f"---\n\n# Final Architecture Report\n\n{ss.final_report}"
            )
            st.download_button(
                label="⬇️ Download Full Bundle",
                data=full_bundle,
                file_name="full_architecture_bundle.md",
                mime="text/markdown",
                use_container_width=True,
            )

        # Bonus: print-friendly text preview
        with st.expander("🖨️ Print-Friendly Preview (Full Document)"):
            st.markdown(f"""
---
## REQUIREMENTS ANALYSIS

{ss.requirements}

---
## SYSTEM DESIGN

{ss.system_design}

---
## FINAL REPORT

{ss.final_report}
""")

# ─────────────────────────────────────────────────────────────
# Empty state
# ─────────────────────────────────────────────────────────────
elif not ss.pipeline_running:
    st.markdown("""
    <div class='empty-state'>
        <div class='icon'>🏗️</div>
        <div class='title'>Ready to architect your project</div>
        <div class='subtitle'>
            Describe your software idea above and click
            <span style='color:#6366f1;font-weight:600;'>Generate Architecture</span><br/>
            Three AI agents will collaborate to produce your complete software planning document.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How it works section
    st.markdown("---")
    st.markdown("#### How It Works")
    hw1, hw2, hw3 = st.columns(3)

    with hw1:
        st.markdown("""
        <div class='section-card'>
            <div class='section-card-title'>🔵 &nbsp; Step 1 — Requirement Agent</div>
            <div style='font-size:0.85rem;color:#64748b;line-height:1.7;'>
                Analyzes your project description (and any uploaded PDFs via RAG) to produce
                a detailed requirements document: overview, features, user stories, and scope.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hw2:
        st.markdown("""
        <div class='section-card'>
            <div class='section-card-title'>🟣 &nbsp; Step 2 — Design Agent</div>
            <div style='font-size:0.85rem;color:#64748b;line-height:1.7;'>
                Takes the requirements and designs: database schema, 20+ API endpoints,
                full tech stack, authentication strategy, and deployment architecture.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hw3:
        st.markdown("""
        <div class='section-card'>
            <div class='section-card-title'>🟢 &nbsp; Step 3 — Report Agent</div>
            <div style='font-size:0.85rem;color:#64748b;line-height:1.7;'>
                Consolidates all outputs into a polished executive report with risk assessment,
                implementation roadmap, and download-ready markdown documents.
            </div>
        </div>
        """, unsafe_allow_html=True)
