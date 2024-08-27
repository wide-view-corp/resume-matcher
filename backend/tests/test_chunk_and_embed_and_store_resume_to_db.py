import pytest
from app.services.resume_processor import ResumeProcessor
from app.dao.dao import delete_all

@pytest.mark.asyncio
async def test_chunk_and_embed_and_store_resume_to_db():
    # Clear the database before running the test
    await delete_all()

    # Initialize ResumeProcessor instance
    resume_processor = ResumeProcessor()
    # Ensure that the index is correctly initialized by awaiting the index setup
    resume_processor.index = await resume_processor.index
    
    # Ensure the test file exists
    test_file_path = "./tests/cv_test_1.pdf"
    
    try:
        with open(test_file_path, "rb") as file:
            mock_pdf_content = file.read()
            mock_pdf_name = file.name
    except FileNotFoundError:
        pytest.fail(f"Test file {test_file_path} not found.")
    
    # Call the method under test
    result = await resume_processor.chunk_and_embed_and_store_resume_to_db(mock_pdf_content, mock_pdf_name)
    
    # Verify the result
    assert result is True, "The function should return True on success."
