import logging
import faiss
from app.dao.dao import save_index_to_database,load_index_from_database
import numpy as np
from app.core.config import settings

logger = logging.getLogger(__name__)

async def load_or_create_index():
        # Attempt to load the index from the database
        index_data = await load_index_from_database()
        if index_data:
            index = faiss.deserialize_index(np.frombuffer(index_data, dtype=np.uint8))
            logger.info("Index loaded from database")
        else:
            index = faiss.IndexFlatL2(settings.VECTOR_DIMENSION)
            logger.info("New FAISS index created")
        return index

async def save_index(index):
        # Serialize the index and store it in the database
        index_data = faiss.serialize_index(index).tobytes()
        await save_index_to_database(index_data)
        logger.info("FAISS index saved to database")