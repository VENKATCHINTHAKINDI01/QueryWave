from .base_exception import RAGBaseException


class ExternalAPIException(RAGBaseException):
    """Errors from third-party APIs (arXiv, search engines, etc.)."""

    pass
