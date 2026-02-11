from sentence_transformers import SentenceTransformer
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_embedding_model(model_name: str):
    logger.info(f"Loading HuggingFace embedding model: {model_name}")
    return SentenceTransformer(model_name)
