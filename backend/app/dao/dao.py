
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.resume import Resume
from app.dao.database import AsyncSessionLocal

async def load_embeddings_from_database():
    """Loads embeddings from the database.

    Returns:
        A list of embeddings loaded from the database.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Resume.embedding))
        embeddings = result.scalars().all()
    return embeddings

async def store_embeddings_in_database(chunks: list[str], embeddings: np.ndarray):
    """Stores resume chunks and their embeddings in the database.

    Args:
        chunks: A list of text chunks extracted from a resume.
        embeddings: A NumPy array of embeddings corresponding to the chunks.
    """
    async with AsyncSessionLocal() as session:
        for chunk, embedding in zip(chunks, embeddings):
            resume = Resume(content=chunk, embedding=embedding.tobytes())
            session.add(resume)
        await session.commit()

async def get_relevant_context(indices: list[int]) -> list[str]:
    """Retrieves relevant text chunks from the database based on indices.

    Args:
        indices: A list of indices representing relevant resume chunks.

    Returns:
        A list of relevant text chunks.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Resume.content).where(Resume.id.in_(indices + 1)))
        relevant_texts = result.scalars().all()
    return relevant_texts