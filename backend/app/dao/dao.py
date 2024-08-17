from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.resume import Resume
from app.models.chunks import Chunks
from app.models.index import IndexData
from app.dao.database import AsyncSessionLocal
import numpy as np

async def store_resume_in_database(content: bytes, text: str):
    """Stores resume in the database."""
    async with AsyncSessionLocal() as session:
        resume = Resume(content=content, text=text)
        session.add(resume)
        await session.commit()
        await session.refresh(resume)
        return resume.id

async def store_chunk_in_database(chunk: str, embedding_id: int, embedding: np.ndarray, resume_id: int):
    """Stores resume's chunk and its embedding_id in the database."""
    async with AsyncSessionLocal() as session:
        chunk = Chunks(content=chunk, embedding_id=embedding_id, embedding=embedding.tobytes(), resume_id=resume_id)
        session.add(chunk)
        await session.commit()

async def get_relevant_context(indices: list[int]) -> list[str]:
    """Retrieves resumes of relevant chunks based on indices."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Resume.id, Resume.text)
            .join(Chunks, Resume.id == Chunks.resume_id)
            .where(Chunks.embedding_id.in_(indices))
            .distinct(Resume.id)  # Ensure unique resume entries
        )
        resumes = result.all()
        
    # Combine the results into the desired format: id followed by text, separated by "\n"
    relevant_texts = "\n\n".join(f"{resume.id}\n{resume.text}" for resume in resumes)

    return relevant_texts

async def save_index_to_database(index_data: bytes):
    """Saves the FAISS index data to the database."""
    async with AsyncSessionLocal() as session:
        # Assuming you have a model to store the index, e.g., IndexData
        index_entry = IndexData(data=index_data)
        session.add(index_entry)
        await session.commit()

async def load_index_from_database() -> bytes:
    """Loads the FAISS index data from the database."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(IndexData.data).order_by(IndexData.id.desc()).limit(1))
        index_data = result.scalar_one_or_none()
    return index_data