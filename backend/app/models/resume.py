from sqlalchemy import Column, Integer, String, LargeBinary
from app.db.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    embedding = Column(LargeBinary)