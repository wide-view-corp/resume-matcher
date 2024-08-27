import pytest
from app.services.resume_processor import ResumeProcessor
from app.services.index_manager import save_index
from app.dao.dao import delete_all
import numpy as np


@pytest.mark.asyncio
async def test_save_index():
    await delete_all()
    resume_processor = ResumeProcessor()

    resume_processor.index = await resume_processor.index

    chunk = "This is a chunk of text."
    embedding = resume_processor.model.encode(chunk)
    resume_processor.index.add(np.array([embedding], dtype=np.float32))

    # Save the updated index to the database
    await save_index(resume_processor.index)

    print(embedding, len(embedding))
