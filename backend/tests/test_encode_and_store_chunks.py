import pytest
from app.services.resume_processor import ResumeProcessor
from app.dao.dao import delete_all

@pytest.mark.asyncio
async def test_encode_and_store_chunks():
    # Clear the database before running the test
    await delete_all()
    
    # Initialize ResumeProcessor instance
    resume_processor = ResumeProcessor()

    # Ensure that the index is correctly initialized by awaiting the index setup
    resume_processor.index = await resume_processor.index

    # Create random chunks and a random resume_id
    chunks = ["This is a chunk of text.", "Here is another chunk.", "Final chunk of resume."]
    resume_id = 123

    # Ensure the index is initialized and empty
    initial_index_count = resume_processor.index.ntotal

    # Call the method under test
    await resume_processor.encode_and_store_chunks(chunks, resume_id)

    # Assertions
    # Ensure that the index has been updated with the new embeddings
    assert resume_processor.index.ntotal == initial_index_count + len(chunks)

#Make sure to run test_drop_all_tables after running this code