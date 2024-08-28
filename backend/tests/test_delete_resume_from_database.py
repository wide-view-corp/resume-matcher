import pytest
from app.dao.dao import delete_resume_from_database
from app.services.resume_processor import ResumeProcessor

@pytest.mark.asyncio
async def test_delete_resume_from_database():
    
    resume_processor = ResumeProcessor()
    # Ensure that the index is correctly initialized by awaiting the index setup
    resume_processor.index = await resume_processor.index

    index_list = await delete_resume_from_database("./tests/cv_test_3.pdf")
    await resume_processor.delete_elements_from_index(index_list)

    assert len(index_list) > 0
    print(index_list)

                                           