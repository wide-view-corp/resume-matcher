from sqlalchemy import Column, Integer, LargeBinary
from app.dao.database import Base

class IndexData(Base):
    __tablename__ = "faiss_index_data"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(LargeBinary, nullable=False)
