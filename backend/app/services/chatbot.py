# app/services/chatbot.py
from app.services.llm import LLMService
from typing import List, Dict

class ChatbotService:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def process_query(self, query: str) -> Dict[str, any]:
        # Use the LLM to generate a response
        llm_response = await self.llm_service.generate_response(query)

        # Use FAISS to find relevant resumes
        relevant_resumes = self.find_relevant_resumes(query)

        return {
            "response": llm_response,
            "suggested_resumes": relevant_resumes
        }

    def find_relevant_resumes(self, query: str) -> List[Dict[str, any]]:
        # Convert query to vector using LLM service
        query_vector = self.llm_service.encode_text(query)

        # Search FAISS index for similar vectors
        D, I = self.llm_service.faiss_index.search(query_vector, k=5)  # Find top 5 matches

        # Retrieve resume data for the matched vectors
        relevant_resumes = []
        for idx in I[0]:
            resume_data = self.llm_service.get_resume_data(idx)  # Implement this method in LLMService
            relevant_resumes.append(resume_data)

        return relevant_resumes

chatbot_service = ChatbotService(LLMService())