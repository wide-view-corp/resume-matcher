import io
import logging
from PyPDF2 import PdfFileReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.core.config import settings
from app.dao.dao import load_embeddings_from_database, store_embeddings_in_database, get_relevant_context

logger = logging.getLogger(__name__)


class ResumeProcessor:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(settings.VECTOR_DIMENSION)

    async def load_index(self):
        embeddings = await load_embeddings_from_database()
        if embeddings:
            self.index = faiss.IndexFlatL2(settings.VECTOR_DIMENSION)
            self.index.add(np.vstack([np.frombuffer(e, dtype=np.float32) for e in embeddings]))

    def chunk_text(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words), settings.CHUNK_SIZE - settings.CHUNK_OVERLAP):
            chunk = ' '.join(words[i:i + settings.CHUNK_SIZE])
            chunks.append(chunk)
        return chunks

    async def process_pdf(self, file_content: bytes):
        try:
            pdf_reader = PdfFileReader(io.BytesIO(file_content))
            text = ""
            for page in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page).extractText()
            
            chunks = self.chunk_text(text)
            embeddings = self.model.encode(chunks)
            
            await store_embeddings_in_database(chunks, embeddings)
            self.index.add(embeddings)
            
            logger.info("Resume processed and added to the index and database")
            return True
        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            return False

    async def get_relevant_context(self, query: str, k: int = 3):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        
        relevant_texts = await get_relevant_context(indices)

        return " ".join(relevant_texts)

resume_processor = ResumeProcessor()