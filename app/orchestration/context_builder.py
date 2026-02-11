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

    # 🔥 Step 1 — Trim recent history
    trimmed_history = _prepare_chat_history(chat_history)

    # 🔥 Step 2 — Apply relevance filtering
    filterer = RelevanceFilter()

    filtered_history = filterer.filter(
        query=user_query,
        chat_history=trimmed_history
    )

    # 🔥 Step 3 — Build final context object (UNCHANGED STRUCTURE)
    context = {
        "query": user_query,
        "chat_history": filtered_history,
        "retrieved_content": retrieval_data or {},
    }

    logger.info(
        f"Context built with {len(filtered_history)} chat messages "
        f"and {len(context['retrieved_content']) if retrieval_data else 0} retrieval entries"
    )

    return context


def _prepare_chat_history(
    chat_history: List[Dict[str, str]],
    max_turns: int = 5,
) -> List[Dict[str, str]]:
    """
    Prepares recent chat history for context.
    Keeps last N conversational turns.
    """

    if not chat_history:
        return []

    # Take last N turns (user + assistant)
    trimmed_history = chat_history[-(max_turns * 2):]

    logger.info(
        f"Included {len(trimmed_history)} chat messages in context"
    )

    return trimmed_history
