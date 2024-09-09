import logging
from tritonclient.http import InferenceServerClient, InferInput, InferRequestedOutput
import numpy as np
from app.core.config import settings
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)

class LLM:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLM, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        logger.info(f"Initializing LLM client for model: {settings.MODEL_NAME}")
        self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
        self.triton_client = InferenceServerClient(url="localhost:8000")
        self.conversation_history = ""

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

    async def generate_response(self, prompt: str, max_length: int = settings.MAX_LENGTH, use_rag: bool = False, context: str = None) -> str:
        try:
            if use_rag and context:
                prompt = f"Consider the following resumes with their names as context:\n\n{context}\n\n You are a recruitment assistant. " \
                         "Your task is to analyze these resumes and compare them with the given job description. " \
                         "Based on this analysis, suggest the resumes that best match the job description and provide a clear explanation for your choices. " \
                         "If multiple resumes are equally suitable, mention this. " \
                         "If the resumes are unclear or you cannot determine a match, state that you do not know without making up an answer." \
                         f"\n\nQuestion: {prompt}\n\nAnswer:"
            
            self.conversation_history += f"\n\nUser: {prompt}\n\nAssistant: "
            self._trim_conversation_history()

            input_ids = self.tokenizer.encode(self.conversation_history, return_tensors="np")
            
            input_tensor = InferInput("INPUT_0", input_ids.shape, "INT64")
            input_tensor.set_data_from_numpy(input_ids)

            output = InferRequestedOutput("OUTPUT_0")
            
            response = self.triton_client.infer("llama", [input_tensor], outputs=[output], client_timeout=settings.TRITON_TIMEOUT)
            
            output_ids = response.as_numpy("OUTPUT_0")
            response_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            self.conversation_history += response_text
            return response_text

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def get_conversation_history(self):
        # Split the conversation history into a list of messages
        messages = self.conversation_history.strip().split('\n\n')
        
        # Convert the messages into a list of dictionaries
        history = []
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                history.append({
                    "user": messages[i].replace("User: ", ""),
                    "assistant": messages[i + 1].replace("Assistant: ", "")
                })
        
        return history
    
# Initialize the LLM instance at module level
llm_instance = LLM()

def get_llm_instance():
    return llm_instance