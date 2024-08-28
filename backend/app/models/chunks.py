from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.dao.database import Base

class Chunks(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    embedding_id = Column(Integer)
    
    # ForeignKey setup
    resume_id = Column(Integer, ForeignKey("resumes.id"))

    # Establishes a relationship back to the Resume table
    resume = relationship("Resume", back_populates="chunks")
