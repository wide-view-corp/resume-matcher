import pytest 
from app.services.llm import LLM

@pytest.mark.asyncio
async def test_generate_response():
    
    llm = LLM()
    prompt = "Explain quantum computing in simple terms."
    response = await llm.generate_response(prompt)

    print(response)
