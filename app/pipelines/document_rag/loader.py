from typing import List, Dict
import io

from app.utils.logger import get_logger
from app.exceptions import RetrievalException

logger = get_logger(__name__)


def load_documents(uploaded_files: List[Dict]) -> List[Dict]:
    """
    Loads uploaded documents and extracts raw text.
    """

    documents = []

    for file_obj in uploaded_files:
        filename = file_obj["name"]
        file = file_obj["file"]

        logger.info(f"Loading document: {filename}")

        try:
            # 🔥 Always reset pointer first
            file.seek(0)

            if filename.lower().endswith(".txt"):
                text = file.read().decode("utf-8")

            elif filename.lower().endswith(".pdf"):
                import fitz  # PyMuPDF

                file_bytes = file.read()

                if not file_bytes:
                    raise RetrievalException(
                        message=f"Uploaded PDF is empty: {filename}",
                        error_code="EMPTY_PDF_STREAM"
                    )

                with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                    text = "\n".join(page.get_text() for page in doc)

            elif filename.lower().endswith(".docx"):
                from docx import Document
                doc = Document(io.BytesIO(file.read()))
                text = "\n".join(p.text for p in doc.paragraphs)

            else:
                raise RetrievalException(
                    message=f"Unsupported file type: {filename}",
                    error_code="UNSUPPORTED_FILE_TYPE"
                )

            if not text.strip():
                raise RetrievalException(
                    message=f"No text extracted from {filename}",
                    error_code="EMPTY_DOCUMENT"
                )

            documents.append({
                "source": filename,
                "text": text
            })

        except Exception as e:
            logger.error(f"Failed to load document {filename}: {e}")
            raise

    logger.info(f"Loaded {len(documents)} documents")
    return documents
