import io
import logging
from PyPDF2 import PdfFileReader
from sentence_transformers import SentenceTransformer
import faiss-cpu as faiss
import numpy as np
from app.core.config import settings
from app.dao.dao import ( 
    store_resume_in_database, 
    store_chunk_in_database, 
    get_relevant_context, 
    save_index_to_database, 
    load_index_from_database
)
from nltk import sent_tokenize

logger = logging.getLogger(__name__)

class ResumeProcessor:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.index = self.load_or_create_index()

    def load_or_create_index(self):
        # Attempt to load the index from the database
        index_data = load_index_from_database()
        if index_data:
            index = faiss.deserialize_index(np.frombuffer(index_data, dtype=np.uint8))
            logger.info("Index loaded from database")
        else:
            index = faiss.IndexFlatL2(settings.VECTOR_DIMENSION)
            logger.info("New FAISS index created")
        return index

    def save_index(self):
        # Serialize the index and store it in the database
        index_data = faiss.serialize_index(self.index).tobytes()
        save_index_to_database(index_data)
        logger.info("FAISS index saved to database")

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
            # Text converter
            pdf_reader = PdfFileReader(io.BytesIO(file_content))
            text = ""
            for page in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page).extractText()
            
            # Store resume
            resume_id = await store_resume_in_database(file_content, text)

            chunks = self.chunk_text(text)
            
            for chunk in chunks:
                embedding = self.model.encode(chunk)
                self.index.add(np.array([embedding], dtype=np.float32))
                embedding_id = self.index.ntotal - 1
                await store_chunk_in_database(chunk, embedding_id, embedding.tobytes(), resume_id)
    
            # Save the updated index to the database
            self.save_index()
            
            logger.info("Resume processed and added to the index and database")
            return True
        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            return False

    async def get_relevant_context(self, query: str, k: int = 10):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        
        relevant_texts = await get_relevant_context(indices)

        return " ".join(relevant_texts)

resume_processor = ResumeProcessor()
