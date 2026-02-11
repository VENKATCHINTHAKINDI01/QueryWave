import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from app.utils.logger import get_logger
from app.utils.config_loader import ConfigLoader
from app.exceptions import RAGBaseException

from app.UI.sidebar import render_sidebar
from app.UI.chat_ui import render_chat_ui
from app.UI.file_upload import render_file_upload

def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "active_mode" not in st.session_state:
        st.session_state.active_mode = None


def main():
    # Load configs
    config_loader = ConfigLoader()
    app_config = config_loader.load("app_config.yaml")

    # Setup logger
    logger = get_logger(
        name=app_config.get("app", {}).get("name", "QueryWave")
    )

    logger.info("Starting Streamlit application")

    # Streamlit page config
    st.set_page_config(
        page_title=app_config["app"]["name"],
        layout="wide",
    )

    st.title(f"💬 {app_config['app']['name']}")

    initialize_session_state()
    
    render_sidebar()
    render_chat_ui()
    if st.session_state.active_mode == "document":
        render_file_upload()

    # Placeholder UI (will be replaced in Phase 1)
    st.info(".")

    # Debug section
    if app_config["app"].get("debug"):
        st.subheader("Debug Info")
        st.json({
            "active_mode": st.session_state.active_mode,
            "chat_history_length": len(st.session_state.chat_history)
        })


if __name__ == "__main__":
    try:
        main()
    except RAGBaseException as e:
        st.error(str(e))
    except Exception as e:
        st.error("Unexpected application error occurred.")
        raise e
