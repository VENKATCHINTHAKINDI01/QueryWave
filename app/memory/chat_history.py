from typing import List, Dict
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChatHistoryManager:
    """
    Manages chat history lifecycle.
    This is the single source of truth for conversation memory.
    """

    def __init__(self, session_state: Dict):
        self.session_state = session_state

        if "chat_history" not in self.session_state:
            self.session_state["chat_history"] = []
            logger.info("Chat history initialized")

    def add_user_message(self, content: str) -> None:
        self.session_state["chat_history"].append(
            {
                "role": "user",
                "content": content
            }
        )
        logger.debug("User message added to chat history")

    def add_assistant_message(self, content: str) -> None:
        self.session_state["chat_history"].append(
            {
                "role": "assistant",
                "content": content
            }
        )
        logger.debug("Assistant message added to chat history")

    def get_history(self) -> List[Dict[str, str]]:
        return self.session_state.get("chat_history", [])

    def clear(self) -> None:
        self.session_state["chat_history"] = []
        logger.info("Chat history cleared")
