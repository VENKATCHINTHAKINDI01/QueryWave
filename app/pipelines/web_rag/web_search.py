from ddgs import DDGS
from app.utils.logger import get_logger

logger = get_logger(__name__)


def search_web(query: str, max_results: int = 5):

    logger.info(f"Searching DuckDuckGo for: {query}")

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title"),
                "body": r.get("body"),
                "href": r.get("href")
            })

    return results
