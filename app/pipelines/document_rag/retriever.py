from typing import List, Dict
from rank_bm25 import BM25Okapi

from app.utils.logger import get_logger
from app.storage.vector_store import VectorStore

logger = get_logger(__name__)


class DocumentRetriever:

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.vector_store = VectorStore(
            embedding_dim=embedding_model.get_sentence_embedding_dimension()
        )
        self.bm25 = None
        self.corpus = []

    def index_chunks(self, chunks: List[Dict]):

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts).tolist()

        metadatas = [
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"]
            }
            for chunk in chunks
        ]

        # Vector index
        self.vector_store.add(embeddings, metadatas)

        # BM25 index
        tokenized_corpus = [text.split() for text in texts]
        self.bm25 = BM25Okapi(tokenized_corpus)
        self.corpus = metadatas

        logger.info("Hybrid index created (Vector + BM25)")

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:

        # Vector retrieval
        query_embedding = self.embedding_model.encode(query).tolist()
        vector_results = self.vector_store.search(query_embedding, top_k=top_k)

        # BM25 retrieval
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_top_indices = sorted(
            range(len(bm25_scores)),
            key=lambda i: bm25_scores[i],
            reverse=True
        )[:top_k]

        bm25_results = [self.corpus[i] for i in bm25_top_indices]

        # Merge results (simple union)
        combined = { (r["source"], r["chunk_id"]): r for r in vector_results }

        for r in bm25_results:
            combined[(r["source"], r["chunk_id"])] = r

        final_results = list(combined.values())[:top_k]

        logger.info(f"Hybrid retrieval returned {len(final_results)} chunks")

        return final_results
