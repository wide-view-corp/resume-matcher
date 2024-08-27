from app.models.resume import Resume
from app.models.chunks import Chunks
from app.models.index import IndexData
from app.dao.database import AsyncSessionLocal
from sqlalchemy.future import select
from app.dao.database import Base
from sqlalchemy import text
import numpy as np

async def store_resume_in_database(file_name: str, content: bytes, text: str):
    """Stores resume in the database."""
    async with AsyncSessionLocal() as session:
        resume = Resume(name = file_name, content=content, text=text)
        session.add(resume)
        await session.commit()
        await session.refresh(resume)
        return resume.id

async def store_chunk_in_database(chunk: str, embedding_id: int, resume_id: int):
    """Stores resume's chunk and its embedding_id in the database."""
    async with AsyncSessionLocal() as session:
        chunk = Chunks(content=chunk, embedding_id=embedding_id, resume_id=resume_id)
        session.add(chunk)
        await session.commit()

async def get_relevant_context(indices: list[int]):
    """Retrieves resumes of relevant chunks based on indices."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Resume.name, Resume.text)
            .join(Chunks, Resume.id == Chunks.resume_id)
            .where(Chunks.embedding_id.in_(indices))
            .distinct(Resume.id)  # Ensure unique resume entries
        )
        resumes = result.all()
        
    return resumes

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

async def delete_all():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Disable foreign key checks to prevent issues while truncating
            await session.execute(text("PRAGMA foreign_keys=OFF;"))

            # Iterate over all tables and delete the data
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())

            # Re-enable foreign key checks
            await session.execute(text("PRAGMA foreign_keys=ON;"))

            # Commit the transaction
            await session.commit()