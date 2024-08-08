import io
import logging
from PyPDF2 import PdfFileReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.core.config import settings
from sqlalchemy import Column, Integer, String, LargeBinary
from app.db.database import Base, AsyncSessionLocal
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    embedding = Column(LargeBinary)

class ResumeProcessor:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(settings.VECTOR_DIMENSION)

    async def load_index(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Resume.embedding))
            embeddings = result.scalars().all()
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
            
            async with AsyncSessionLocal() as session:
                for chunk, embedding in zip(chunks, embeddings):
                    resume = Resume(content=chunk, embedding=embedding.tobytes())
                    session.add(resume)
                await session.commit()
            
            self.index.add(embeddings)
            
            logger.info("Resume processed and added to the index and database")
            return True
        except Exception as e:
            logger.error(f"Error processing resume: {str(e)}")
            return False

    async def get_relevant_context(self, query: str, k: int = 3):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Resume.content).where(Resume.id.in_(indices[0] + 1)))
            relevant_texts = result.scalars().all()
        
        return " ".join(relevant_texts)

resume_processor = ResumeProcessor()