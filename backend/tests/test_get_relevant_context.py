import pytest
from app.services.resume_processor import ResumeProcessor
from app.dao.dao import delete_all

@pytest.mark.asyncio
async def test_get_relevant_context():
    # Clear the database before running the test
    await delete_all()
    
    # Initialize ResumeProcessor instance
    resume_processor = ResumeProcessor()
    resume_processor.index = await resume_processor.index
    
    # Add 5 resumes
    for i in range(1, 6):
        test_file_path = f"./tests/cv_test_{i}.pdf"
    
        try:
            with open(test_file_path, "rb") as file:
                mock_pdf_content = file.read()
                mock_pdf_name = file.name
        except FileNotFoundError:
            pytest.fail(f"Test file {test_file_path} not found.")
        
        # Call the method under test
        await resume_processor.chunk_and_embed_and_store_resume_to_db(mock_pdf_content, mock_pdf_name)
        
    query = "I am looking for a software engineer with experience in machine learning."

    context = await resume_processor.get_relevant_context(query, k= 1)

    print(context)




    
