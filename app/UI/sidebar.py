import streamlit as st
from app.utils.logger import get_logger

logger = get_logger(__name__)


def render_sidebar():
    """
    Premium Sidebar UI for QueryWave.
    Handles mode selection + dynamic inputs.
    """

    with st.sidebar:

        # -------------------------------
        # Branding
        # -------------------------------

        st.markdown("""
        <style>
        .sidebar-title {
            font-size: 26px;
            font-weight: 700;
            color: white;
            margin-bottom: 5px;
        }
        .sidebar-sub {
            font-size: 14px;
            color: #9ca3af;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-title">🌊 QueryWave</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sub">AI Retrieval Platform</div>',
                    unsafe_allow_html=True)

        st.markdown("### ⚙️ Mode Selection")

        # -------------------------------
        # Mode Mapping
        # -------------------------------

        modes = {
            "📄 Document Q&A": "document",
            "🌐 Web Search": "web",
            "📚 Research Papers (arXiv)": "arxiv",
        }

        selected_label = st.radio(
            label="Choose how you want to work:",
            options=list(modes.keys()),
            index=0
        )

        selected_mode = modes[selected_label]

        # Persist active mode
        if st.session_state.get("active_mode") != selected_mode:
            st.session_state.active_mode = selected_mode
            logger.info(f"Active mode changed to: {selected_mode}")

        st.markdown("---")

        # -------------------------------
        # Document Upload Section
        # -------------------------------

        if selected_mode == "document":

            st.markdown("### 📂 Upload Documents")

            uploaded_files = st.file_uploader(
                "Supported: PDF, DOCX, TXT",
                type=["pdf", "docx", "txt"],
                accept_multiple_files=True
            )

            if uploaded_files:
                st.success(f"{len(uploaded_files)} file(s) uploaded")

                # Store in session state
                st.session_state["uploaded_files"] = [
                    {"name": f.name, "file": f}
                    for f in uploaded_files
                ]

                # Optional: show file list
                with st.expander("📑 View Uploaded Files"):
                    for f in uploaded_files:
                        st.write(f"• {f.name}")

        # -------------------------------
        # arXiv Paper Section
        # -------------------------------

        if selected_mode == "arxiv":

            st.markdown("### 📚 arXiv Paper")

            arxiv_id = st.text_input(
                "Enter arXiv Paper ID",
                placeholder="e.g., 1706.03762"
            )

            if arxiv_id:
                st.session_state["arxiv_id"] = arxiv_id.strip()
                st.info(f"Paper ID set: {arxiv_id}")

        # -------------------------------
        # Web Mode Info
        # -------------------------------

        if selected_mode == "web":
            st.markdown("### 🌐 Web Search Mode")
            st.caption("Ask questions using real-time web context.")

        st.markdown("---")

        # -------------------------------
        # Footer
        # -------------------------------

        st.caption("⚡ Powered by Llama3 + Hybrid Retrieval")
        st.caption("🔒 Open-source RAG System")
