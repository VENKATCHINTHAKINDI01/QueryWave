from typing import Dict, List, Any

from app.utils.logger import get_logger

from app.memory.relevance_filter import RelevanceFilter


logger = get_logger(__name__)


def build_context(
    user_query: str,
    chat_history: List[Dict[str, str]],
    retrieval_data: Dict[str, Any] | None = None,
) -> Dict[str, Any]:

    logger.info("Building context for LLM")

    filterer = RelevanceFilter()

    filtered_history = filterer.filter(
        query=user_query,
        chat_history=chat_history
    )

    context = {
        "query": user_query,
        "chat_history": filtered_history,
        "retrieved_content": retrieval_data or {},
    }

    return context

def _prepare_chat_history(
    chat_history: List[Dict[str, str]],
    max_turns: int = 5,
) -> List[Dict[str, str]]:
    """
    Prepares recent chat history for context.
    Later this will include relevance filtering.
    """

    if not chat_history:
        return []

    # Take last N turns (user + assistant)
    trimmed_history = chat_history[-(max_turns * 2):]

    logger.info(
        f"Included {len(trimmed_history)} chat messages in context"
    )

    return trimmed_history
