from typing import List, Dict
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RelevanceFilter:
    """
    Filters chat history based on relevance to current query.
    This is a lightweight, rule-based version.
    """

    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns

    def filter(
        self,
        query: str,
        chat_history: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Returns only relevant chat messages.
        """

        if not chat_history:
            return []

        logger.info("Applying relevance filter on chat history")

        query_keywords = set(query.lower().split())

        relevant_messages = []

        for message in reversed(chat_history):
            content_words = set(message["content"].lower().split())

            # Simple keyword overlap check
            if query_keywords & content_words:
                relevant_messages.append(message)

            # Stop when enough turns collected
            if len(relevant_messages) >= self.max_turns * 2:
                break

        relevant_messages.reverse()

        logger.info(
            f"Selected {len(relevant_messages)} relevant chat messages"
        )

        return relevant_messages
