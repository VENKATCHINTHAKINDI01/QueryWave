import streamlit as st
from app.utils.logger import get_logger

logger = get_logger(__name__)


def render_file_upload():
    """
    Renders file upload component for document-based Q&A.
    """

    st.subheader("📄 Upload Documents")

    uploaded_files = st.file_uploader(
        label="Upload documents (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f["name"] for f in st.session_state.uploaded_files]:
                st.session_state.uploaded_files.append(
                    {
                        "name": file.name,
                        "file": file
                    }
                )
                logger.info(f"Uploaded file: {file.name}")
                
    if st.session_state.uploaded_files:
        st.markdown("#### ✅ Uploaded Files")
        for f in st.session_state.uploaded_files:
            st.write(f"- {f['name']}")
            
    # Invalidate retriever if new files uploaded
    if "document_retriever" in st.session_state:
        del st.session_state["document_retriever"]
