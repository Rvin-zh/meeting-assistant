import json
from pathlib import Path

from backend.models.schemas import TranscriptChunk
from backend.services.embeddings import EmbeddingService, cosine_similarity


class StoredChunk:
    def __init__(
        self,
        chunk_id: str,
        speaker: str,
        text: str,
        embedding: list[float],
    ) -> None:
        self.chunk_id = chunk_id
        self.speaker = speaker
        self.text = text
        self.embedding = embedding


class VectorStore:
    def __init__(
        self, vectors_dir: Path, embedder: EmbeddingService | None = None
    ) -> None:
        self.vectors_dir = vectors_dir
        self.embedder = embedder or EmbeddingService()

    def _path(self, meeting_id: str) -> Path:
        return self.vectors_dir / f"{meeting_id}.json"

    async def index_meeting(
        self,
        meeting_id: str,
        chunks: list[TranscriptChunk],
    ) -> None:
        embeddings = await self.embedder.embed([c.text for c in chunks])
        payload = {
            "meeting_id": meeting_id,
            "chunks": [
                {
                    "chunk_id": chunk.chunk_id,
                    "speaker": chunk.speaker,
                    "text": chunk.text,
                    "embedding": embedding,
                }
                for chunk, embedding in zip(chunks, embeddings)
            ],
        }
        self._path(meeting_id).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self, meeting_id: str) -> list[StoredChunk]:
        path = self._path(meeting_id)
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return [
            StoredChunk(
                chunk_id=item["chunk_id"],
                speaker=item["speaker"],
                text=item["text"],
                embedding=item["embedding"],
            )
            for item in data.get("chunks", [])
        ]

    async def search(
        self,
        meeting_id: str,
        query: str,
        top_k: int = 5,
    ) -> list[StoredChunk]:
        chunks = self.load(meeting_id)
        if not chunks:
            return []
        query_embedding = await self.embedder.embed_query(query)
        ranked = sorted(
            chunks,
            key=lambda c: cosine_similarity(query_embedding, c.embedding),
            reverse=True,
        )
        return ranked[:top_k]
