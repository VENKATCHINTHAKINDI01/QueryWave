import streamlit as st

from app.utils.logger import get_logger
from app.orchestration.router import route_query
from app.orchestration.tool_manager import execute_tool
from app.exceptions import RoutingException
from app.memory.chat_history import ChatHistoryManager

logger = get_logger(__name__)


def render_chat_ui():
    """
    Premium Chat UI.
    - Clean main interface
    - History accessible via toggle
    - No feature changes
    """

    memory = ChatHistoryManager(st.session_state)

    # -----------------------------------
    # Premium CSS
    # -----------------------------------

    st.markdown("""
    <style>

    .history-button {
        position: fixed;
        top: 90px;
        right: 40px;
        z-index: 1000;
    }

    .history-panel {
        background: rgba(0,0,0,0.85);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(0,255,255,0.2);
    }

    </style>
    """, unsafe_allow_html=True)

    # -----------------------------------
    # History Toggle Button
    # -----------------------------------

    col1, col2 = st.columns([10, 1])

    with col2:
        if st.button("🕘", help="View Chat History"):
            st.session_state["show_history"] = not st.session_state.get("show_history", False)

    # -----------------------------------
    # History Panel (Hidden by Default)
    # -----------------------------------

    if st.session_state.get("show_history", False):

        with st.container():
            st.markdown('<div class="history-panel">', unsafe_allow_html=True)
            st.markdown("### 🕘 Conversation History")

            history = memory.get_history()

            if not history:
                st.caption("No previous messages.")
            else:
                for msg in history:
                    role = "🧑 You" if msg["role"] == "user" else "🤖 Assistant"
                    st.markdown(f"**{role}:** {msg['content']}")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

    # -----------------------------------
    # Clean Main Chat Area
    # -----------------------------------

    user_input = st.chat_input("Ask your question...")

    if user_input:

        memory.add_user_message(user_input)

        try:
            routing_result = route_query(
                user_query=user_input,
                state=st.session_state
            )

            execution_result = execute_tool(routing_result)

            response_data = execution_result["data"]

            assistant_response = response_data["answer"]
            sources = response_data.get("sources", [])

        except RoutingException as e:
            logger.error(str(e))
            assistant_response = f"⚠️ {str(e)}"
            sources = []

        memory.add_assistant_message(assistant_response)

        with st.chat_message("assistant"):
            st.markdown(assistant_response)

            if sources:
                st.markdown("---")
                st.markdown("### 📚 Sources")
                for source in sources:
                    st.markdown(
                        f"- **{source['source']}** (Chunk {source['chunk_id']})"
                    )
