from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from app.dao.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(LargeBinary)
    text = Column(String)

    # Establishes a one-to-many relationship with the Chunks table
    chunks = relationship("Chunks", back_populates="resume")
