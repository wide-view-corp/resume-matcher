import pytest
from app.services.resume_processor import ResumeProcessor

@pytest.fixture
def resume_processor():
    return ResumeProcessor()

def test_process_pdf(resume_processor):
    # This is a mock test. In a real scenario, you'd use a sample PDF file.
    mock_pdf_content = b"%PDF-1.3\n%\xe2\xe3\xcf\xd3\n..."
    result = resume_processor.process_pdf(mock_pdf_content)
    assert result == True

def test_get_relevant_context(resume_processor):
    # First, add some mock data to the index
    resume_processor.resume_texts = ["Sample resume text"]
    resume_processor.index.add(resume_processor.tokenizer("Sample resume text", return_tensors="pt", max_length=512, truncation=True, padding="max_length").input_ids.float().numpy())

    context = resume_processor.get_relevant_context("Sample query")
    assert "Sample resume text" in context