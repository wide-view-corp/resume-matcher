import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from app.core.config import settings
from app.services.resume_processor import resume_processor

logger = logging.getLogger(__name__)

class LLM:
    def __init__(self):
        logger.info(f"Initializing LLM with model: {settings.MODEL_NAME}")
        self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(settings.MODEL_NAME)
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        logger.info(f"Model loaded and moved to device: {self.device}")

    async def generate_response(self, prompt: str, max_length: int = settings.MAX_LENGTH, use_rag: bool = False) -> str:
        try:
            if use_rag:
                context = await resume_processor.get_relevant_context(prompt)
                prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"

            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    no_repeat_ngram_size=2,
                    top_k=50,
                    top_p=0.95,
                    temperature=0.7
                )
            
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise


    def get_resume_data(self, index: int) -> Dict[str, any]:
            # This method should retrieve the resume data associated with the given index
            # You'll need to implement this based on how you're storing resume data
            # For example, you might have a database or a dictionary mapping indices to resume data
            # For now, we'll return a dummy response
            return {
                "id": index,
                "name": f"Candidate {index}",
                "summary": f"This is a summary of candidate {index}'s resume.",
                "skills": ["Python", "FastAPI", "FAISS"],
                "experience": ["Software Engineer at Tech Co", "Data Scientist at AI Inc"]
            }
    
llm = LLM()