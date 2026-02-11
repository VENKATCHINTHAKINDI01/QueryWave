from typing import List, Dict

from app.utils.logger import get_logger

logger = get_logger(__name__)


def chunk_documents(
    documents: List[Dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> List[Dict]:
    """
    Splits documents into overlapping text chunks.

    Returns:
        [
          {
            "source": filename,
            "chunk_id": int,
            "text": chunk_text
          }
        ]
    """

    chunks = []

    for doc in documents:
        text = doc["text"]
        source = doc["source"]

        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "source": source,
                "chunk_id": chunk_id,
                "text": chunk_text
            })

            start = end - chunk_overlap
            chunk_id += 1

        logger.info(
            f"Created {chunk_id} chunks from {source}"
        )

    return chunks
