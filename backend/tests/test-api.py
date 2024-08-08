from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_text():
    response = client.post("/generate", json={"prompt": "Hello, world!"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_empty_prompt():
    response = client.post("/generate", json={"prompt": ""})
    assert response.status_code == 400

def test_generate_text_with_rag():
    response = client.post("/generate", json={"prompt": "Tell me about the resume", "use_rag": True})
    assert response.status_code == 200
    assert "response" in response.json()