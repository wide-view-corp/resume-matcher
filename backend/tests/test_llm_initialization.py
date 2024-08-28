import pytest 
from app.services.llm import LLM

@pytest.mark.asyncio
async def test_llm_initialization():
    llm = LLM()
    assert llm is not None
