import io
import logging
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.core.config import settings
from app.dao.dao import get_all_resumes_from_database, store_resume_in_database, store_chunk_in_database, get_relevant_context
from app.services.index_manager import load_or_create_index, save_index
import nltk
import asyncio

logger = logging.getLogger(__name__)

class ResumeProcessor:
    def __init__(self):
        self.index = None
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.ensure_nltk_data()

    async def initialize(self):
        if self.index is None:
            self.index = await load_or_create_index()

    def ensure_nltk_data(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("NLTK punkt tokenizer not found. Downloading...")
            nltk.download('punkt', quiet=True)
            logger.info("NLTK punkt tokenizer downloaded successfully.")

    async def encode_and_store_chunks(self, chunks: list, resume_id: int):
        if self.index is None:
            await self.initialize()
        for chunk in chunks:
            embedding = self.model.encode(chunk)
            self.index.add(np.array([embedding], dtype=np.float32))
            embedding_id = self.index.ntotal - 1
            await store_chunk_in_database(chunk, embedding_id, resume_id)
        await save_index(self.index)

    async def get_all_resumes(self):
        try:
            resumes=await get_all_resumes_from_database()
            logger.log(logging.INFO,resumes)
            return [{"id": str(id), "name": name } for id, name in resumes]
        except Exception as e:
            logger.error(f"Error geting resumes : {str(e)}")
            return []
        
    async def chunk_and_embed_and_store_resume_to_db(self, content: bytes, filename: str):
        try:
            if self.index is None:
                await self.initialize()
            text = self.extract_text_from_resume(content)
            chunks = self.chunk_text(text)
            
            resume_id = await store_resume_in_database(filename, content, text)

            await self.encode_and_store_chunks(chunks, resume_id)
            
            logger.info(f"Resume {filename} (originally {filename}) processed and stored successfully")
            return True
        except Exception as e:
            logger.error(f"Error processing resume {filename}: {str(e)}")
            return False

    def extract_text_from_resume(self, file_content: bytes):
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        return text 

    def chunk_text(self, text):
        chunk_size = settings.CHUNK_SIZE
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

    async def get_relevant_context(self, query: str, k: int = 10):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        
        resumes = await get_relevant_context(indices)
        relevant_texts = "\n\n".join(f"{resume.name}\n{resume.text}" for resume in resumes)
        return " ".join(relevant_texts)
    
    async def delete_elements_from_index(self, id_list):
        ids_to_remove = np.array(id_list, dtype='int64')
        self.index.remove_ids(ids_to_remove)