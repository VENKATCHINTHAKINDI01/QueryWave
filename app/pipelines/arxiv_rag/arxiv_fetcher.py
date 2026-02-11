import arxiv
import requests
import io
import fitz

from app.utils.logger import get_logger
from app.exceptions import RetrievalException

logger = get_logger(__name__)


def fetch_arxiv_pdf(arxiv_id: str) -> str:
    """
    Fetch arXiv paper by ID and return extracted text.
    """

    logger.info(f"Fetching arXiv paper: {arxiv_id}")

    search = arxiv.Search(id_list=[arxiv_id])
    results = list(search.results())

    if not results:
        raise RetrievalException(
            message=f"No paper found with ID {arxiv_id}",
            error_code="ARXIV_NOT_FOUND"
        )

    paper = results[0]
    pdf_url = paper.pdf_url

    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise RetrievalException(
            message="Failed to download arXiv PDF",
            error_code="ARXIV_DOWNLOAD_FAILED"
        )

    pdf_bytes = io.BytesIO(response.content)

    with fitz.open(stream=pdf_bytes.read(), filetype="pdf") as doc:
        text = "\n".join(page.get_text() for page in doc)

    if not text.strip():
        raise RetrievalException(
            message="Extracted paper text is empty",
            error_code="ARXIV_EMPTY_TEXT"
        )

    return text
