import os
from huggingface_hub import snapshot_download

model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
cache_dir = "/app/model_cache"

def download_model():
    os.makedirs(cache_dir, exist_ok=True)
    snapshot_download(repo_id=model_name, cache_dir=cache_dir)

if __name__ == "__main__":
    download_model()