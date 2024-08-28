import pytest
from app.services.resume_processor import chunk_text, extract_text_from_resume

def test_chunk_resume():
    # Ensure the test file exists
    test_file_path = "./tests/cv_test_1.pdf"
    
    try:
        with open(test_file_path, "rb") as file:
            mock_pdf_content = file.read()
    except FileNotFoundError:
        pytest.fail(f"Test file {test_file_path} not found.")
    
    # Extract text using the extract_text_from_resume function
    extracted_text = extract_text_from_resume(mock_pdf_content)
    
    # Chunk the extracted text
    chunks = chunk_text(extracted_text)
    
    # Print the chunks for debugging purposes
    print(chunks)

    # Assertions
    assert chunks is not None, "Chunks should not be None."
    assert len(chunks) > 0, "Chunks should not be empty."
    
    # Optionally, check specific properties of chunks
    for chunk in chunks:
        assert len(chunk) > 0, "Each chunk should be non-empty."
