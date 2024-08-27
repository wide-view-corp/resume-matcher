import pytest
from app.services.resume_processor import extract_text_from_resume
from app.dao.dao import store_resume_in_database

@pytest.mark.asyncio
async def test_store_resume_in_database():
    # Ensure the test file exists
    test_file_path = "./tests/cv_test_1.pdf"
    
    try:
        with open(test_file_path, "rb") as file:
            mock_pdf_content = file.read()
            mock_pdf_name = file.name
    except FileNotFoundError:
        pytest.fail(f"Test file {test_file_path} not found.")
    
    # Extract text using the extract_text_from_resume function
    extracted_text = extract_text_from_resume(mock_pdf_content)
    
    # Store resume - properly await the coroutine
    resume_id = await store_resume_in_database(mock_pdf_name, mock_pdf_content, extracted_text)

    print(resume_id)
    # You can add assertions here to check if resume_id is valid, or query the database to ensure the resume was stored



