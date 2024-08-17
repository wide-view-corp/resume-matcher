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
        
        # Initialize conversation history
        self.conversation_history = ""

        logger.info(f"Model loaded and moved to device: {self.device}")

    def _trim_conversation_history(self):
        """Trim conversation history to ensure it does not exceed CONTEXT_LENGTH."""
        # Tokenize the current conversation history
        history_tokens = self.tokenizer(self.conversation_history, return_tensors="pt").input_ids[0]
        
        # If the token length exceeds the context limit, truncate it
        if len(history_tokens) > settings.CONTEXT_LENGTH:
            # Keep only the last CONTEXT_LENGTH tokens
            trimmed_tokens = history_tokens[-settings.CONTEXT_LENGTH:]
            # Decode tokens back to string
            self.conversation_history = self.tokenizer.decode(trimmed_tokens, skip_special_tokens=True)

    async def generate_response(self, prompt: str, max_length: int = settings.MAX_LENGTH, use_rag: bool = False) -> str:
        try:
            if use_rag:
                context = await resume_processor.get_relevant_context(prompt)
                prompt = f"Consider the following resumes with their IDs as context:\n\n{context}\n\n You are a recruitment assistant. " \
                         "Your task is to analyze these resumes and compare them with the given job description. " \
                         "Based on this analysis, suggest the resumes that best match the job description and provide a clear explanation for your choices. " \
                         "If multiple resumes are equally suitable, mention this. " \
                         "If the resumes are unclear or you cannot determine a match, state that you do not know without making up an answer." \
                         f"\n\nQuestion: {prompt}\n\nAnswer:"
            
            # Append the new prompt to the conversation history
            self.conversation_history += f"\n\nUser: {prompt}\n\nAssistant: "
            
            # Trim the conversation history to respect CONTEXT_LENGTH
            self._trim_conversation_history()

            inputs = self.tokenizer(self.conversation_history, return_tensors="pt").to(self.device)
            
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
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Append the response to the conversation history
            self.conversation_history += response

            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
llm = LLM()