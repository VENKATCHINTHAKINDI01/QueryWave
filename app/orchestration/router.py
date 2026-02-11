from typing import Dict

from app.exceptions import RoutingException
from app.utils.logger import get_logger

logger = get_logger(__name__)


def route_query(user_query: str, state: Dict) -> Dict:
    """
    Routes user query to the correct pipeline based on active mode.

    Returns:
        {
            "mode": str,
            "query": str,
            "metadata": dict
        }
    """

    active_mode = state.get("active_mode")

    if not active_mode:
        raise RoutingException(
            message="No mode selected by user",
            error_code="MODE_NOT_SELECTED"
        )

    logger.info(f"Routing query under mode: {active_mode}")

    # Document Q&A requires uploaded files
    if active_mode == "document":
        uploaded_files = state.get("uploaded_files", [])
        if not uploaded_files:
            raise RoutingException(
                message="No documents uploaded for Document Q&A",
                error_code="NO_DOCUMENTS_UPLOADED"
            )

        return {
            "mode": "document",
            "query": user_query,
            "metadata": {
                "file_count": len(uploaded_files)
            },
            "state" : state
        }

    # Web search
    if active_mode == "web":
        return {
            "mode": "web",
            "query": user_query,
            "metadata": {},
            "state" : state
            
        }

    # Research papers (arXiv)
    if active_mode == "arxiv":
        return {
            "mode": "arxiv",
            "query": user_query,
            "metadata": {},
            "state" : state
        }

    # Fallback (should never happen)
    raise RoutingException(
        message=f"Unsupported mode: {active_mode}",
        error_code="INVALID_MODE"
    )
