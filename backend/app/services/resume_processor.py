import io
import logging
from PyPDF2 import PdfFileReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.core.config import settings
from app.dao.dao import load_embeddings_from_database, store_resume_in_database, store_chunk_in_database, get_relevant_context
from nltk import sent_tokenize

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

    # Function to chunk text into smaller pieces
    def chunk_text(self, text):
        chunk_size = settings.CHUNK_SIZE
        sentences = sent_tokenize(text)
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

    async def process_pdf(self, file_content: bytes):
        try:

            #Text convertor
            pdf_reader = PdfFileReader(io.BytesIO(file_content))
            text = ""
            for page in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page).extractText()
            
            #store resume
            resume_id = await store_resume_in_database(file_content, text)

            chunks = self.chunk_text(text)
            
            for chunk in chunks :
                embedding = self.model.encode(chunk)
                self.index.add(embedding)
                embedding_id = self.index.ntotal - 1
                await store_chunk_in_database(chunk, embedding_id, resume_id)
    
            
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