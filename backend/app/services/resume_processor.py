import io
import logging
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.core.config import settings
from app.dao.dao import store_resume_in_database, store_chunk_in_database, get_relevant_context

from app.services.index_manager import load_or_create_index, save_index
import nltk
import asyncio

logger = logging.getLogger(__name__)

class ResumeProcessor:
    def __init__(self):
        self.index = load_or_create_index()
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
  
    async def encode_and_store_chunks(self, chunks: list, resume_id: int):
        for chunk in chunks:
            embedding = self.model.encode(chunk)
            self.index.add(np.array([embedding], dtype=np.float32))
            embedding_id = self.index.ntotal - 1
            await store_chunk_in_database(chunk, embedding_id, resume_id)
    
        # Save the updated index to the database
        await save_index(self.index)

    async def chunk_and_embed_and_store_resume_to_db(self, file_content: bytes, file_name: str):
        try:
            text = extract_text_from_resume(file_content)
            chunks = chunk_text(text)
            
            # Store resume
            resume_id = await store_resume_in_database(file_name, file_content, text)

            await self.encode_and_store_chunks(chunks, resume_id)
            
            logger.info("Resume chunked, embedded, and added to the index and database")
            return True
        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            return False


    async def get_relevant_context(self, query: str, k: int = 10):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        
        resumes = await get_relevant_context(indices)
        # Combine the results into the desired format: id followed by text, separated by "\n"
        relevant_texts = "\n\n".join(f"{resume.name}\n{resume.text}" for resume in resumes)
        return " ".join(relevant_texts)

def extract_text_from_resume(file_content: bytes):
        # Text converter
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()

        return text 

def chunk_text(text):
        chunk_size = settings.CHUNK_SIZE
        nltk.download('punkt_tab')
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length <= chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

if __name__ == "__main__":
    resume_processor = ResumeProcessor()
    logger.info("ResumeProcessor initialized")
