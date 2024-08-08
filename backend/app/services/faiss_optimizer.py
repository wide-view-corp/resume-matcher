import time
import schedule
import faiss
import numpy as np
from app.core.config import settings
from app.services.llm import LLMService

class FAISSOptimizer:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def optimize_index(self):
        print("Starting FAISS index optimization...")
        
        # Get the current index
        current_index = self.llm_service.faiss_index
        
        # Extract all vectors and IDs from the current index
        all_ids = []
        all_vectors = []
        for i in range(current_index.ntotal):
            vector = current_index.reconstruct(i)
            all_vectors.append(vector)
            all_ids.append(i)
        
        all_vectors = np.array(all_vectors)
        all_ids = np.array(all_ids)
        
        # Create a new index with the same parameters
        new_index = faiss.index_factory(current_index.d, current_index.index_factory_string)
        
        # Train the new index if necessary
        if not new_index.is_trained:
            new_index.train(all_vectors)
        
        # Add all vectors to the new index
        new_index.add_with_ids(all_vectors, all_ids)
        
        # Replace the old index with the new one
        self.llm_service.faiss_index = new_index
        
        print("FAISS index optimization completed.")

    def run_periodic_optimization(self):
        schedule.every(settings.FAISS_OPTIMIZATION_INTERVAL_HOURS).hours.do(self.optimize_index)

        while True:
            schedule.run_pending()
            time.sleep(60)  # Sleep for 1 minute before checking again

faiss_optimizer = FAISSOptimizer(LLMService())

def start_faiss_optimizer():
    faiss_optimizer.run_periodic_optimization()