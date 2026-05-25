import json

import pytest

from backend.services.vector_store import StoredChunk, VectorStore
from backend.tests.conftest import FakeEmbeddingService


class TestVectorStorePersistence:
    @pytest.mark.asyncio
    async def test_index_and_load(self, vector_store: VectorStore, sample_chunks):
        await vector_store.index_meeting("m1", sample_chunks)
        loaded = vector_store.load("m1")
        assert len(loaded) == 3
        assert loaded[0].chunk_id == "c0"
        assert isinstance(loaded[0].embedding, list)

    def test_load_missing_meeting_returns_empty(self, vector_store: VectorStore):
        assert vector_store.load("nonexistent") == []

    @pytest.mark.asyncio
    async def test_index_writes_json_file(
        self, vector_store: VectorStore, sample_chunks
    ):
        await vector_store.index_meeting("m2", sample_chunks)
        path = vector_store._path("m2")
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["meeting_id"] == "m2"
        assert len(data["chunks"]) == 3


class TestVectorStoreSearch:
    @pytest.mark.asyncio
    async def test_search_returns_top_k(self, vector_store: VectorStore, sample_chunks):
        await vector_store.index_meeting("m3", sample_chunks)
        results = await vector_store.search("m3", "deadline release پنجشنبه", top_k=2)
        assert len(results) <= 2
        assert all(isinstance(r, StoredChunk) for r in results)

    @pytest.mark.asyncio
    async def test_search_empty_store_returns_empty(self, vector_store: VectorStore):
        results = await vector_store.search("missing", "query")
        assert results == []

    @pytest.mark.asyncio
    async def test_search_exact_match_ranks_first(self, vector_store: VectorStore):
        from backend.models.schemas import TranscriptChunk

        chunks = [
            TranscriptChunk(chunk_id="c0", speaker="a", text="alpha", turn_indices=[0]),
            TranscriptChunk(chunk_id="c1", speaker="b", text="beta", turn_indices=[1]),
        ]
        await vector_store.index_meeting("m4", chunks)
        results = await vector_store.search("m4", "alpha", top_k=1)
        assert results[0].chunk_id == "c0"
