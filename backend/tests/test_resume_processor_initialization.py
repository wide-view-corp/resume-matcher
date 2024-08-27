import pytest
from app.services.resume_processor import ResumeProcessor

@pytest.mark.asyncio
async def test_resume_processor_initialization():
    processor = ResumeProcessor()
    assert processor.index is not None
    assert processor.model is not None

    
    