
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.resume import Resume
from app.models.chunks import Chunks
from app.dao.database import AsyncSessionLocal
import numpy as np

async def load_embeddings_from_database():
    """Loads embeddings from the database.

    Returns:
        A list of embeddings loaded from the database.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Chunks.embedding))
        embeddings = result.scalars().all()
    return embeddings

async def store_resume_in_database(content = bytes, text = str):
    """Stores resume in the database.
    """
    async with AsyncSessionLocal() as session:
        resume = Resume(content = content, text = text)
        session.add(resume)
        await session.commit()
        await session.refresh(resume)
        return resume.id


async def store_chunk_in_database(chunk: str, embedding_id: int, embedding: np.ndarray,resume_id: int):
    """Stores resume's chunk and its embedding_id in the database.
    """
    async with AsyncSessionLocal() as session:
        chunk = Chunks(content=chunk, embedding_id=embedding_id, embedding=embedding.tobytes(), resume_id= resume_id)
        session.add(chunk)
        await session.commit()

async def get_relevant_context(indices: list[int]) -> list[str]:
    """Retrieves resumes of relevant chunks based on indices.

    Args:
        indices: A list of indices representing relevant resume chunks.

    Returns:
        A list of relevant resumes.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
                select(Resume.text)
                .join(Chunks, Resume.id == Chunks.resume_id)
                .where(Chunks.embedding_id.in_(indices))
            )
        relevant_texts = result.scalars().all()
    return relevant_texts