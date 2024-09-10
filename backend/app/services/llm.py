from ctransformers import AutoModelForCausalLM
import logging
from app.core.config import settings

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
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.MODEL_NAME,
            model_type="llama",
            max_new_tokens=settings.MAX_LENGTH,
            context_length=settings.CONTEXT_LENGTH,
            gpu_layers=0
        )
        self.conversation_history = ""

    def _trim_conversation_history(self):
        tokens = self.model.tokenize(self.conversation_history)
        if len(tokens) > settings.CONTEXT_LENGTH:
            trimmed_tokens = tokens[-settings.CONTEXT_LENGTH:]
            self.conversation_history = self.model.detokenize(trimmed_tokens)

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

            response = self.model(self.conversation_history, max_new_tokens=max_length)
            
            self.conversation_history += response
            return response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    def get_conversation_history(self):
        messages = self.conversation_history.strip().split('\n\n')
        history = []
        for i in range(0, len(messages), 2):
            if i + 1 < len(messages):
                history.append({
                    "user": messages[i].replace("User: ", ""),
                    "assistant": messages[i + 1].replace("Assistant: ", "")
                })
        return history

llm_instance = LLM()

def get_llm_instance():
    return llm_instance