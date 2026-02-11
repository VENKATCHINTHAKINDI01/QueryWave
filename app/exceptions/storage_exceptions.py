from .base_exception import RAGBaseException


class StorageException(RAGBaseException):
    """Errors related to vector DB, file system, or metadata storage."""

    pass
