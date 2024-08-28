from app.services.resume_processor import extract_text_from_resume

def test_extract_text_from_resume():
    # Read the content of the cv_test.pdf file
    with open("./tests/cv_test_1.pdf", "rb") as file:
        mock_pdf_content = file.read()
    
    # Extract text using the extract_text_from_resume function
    extracted_text = extract_text_from_resume(mock_pdf_content)
    
    # Print the extracted text so you can see it
    print(extracted_text)

    # Add a meaningful assertion
    assert extracted_text is not None

