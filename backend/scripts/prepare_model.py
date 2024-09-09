from transformers import AutoModelForCausalLM, AutoTokenizer
import os

def prepare_model():
    if os.environ.get('PREPARE_MODEL', 'false').lower() != 'true':
        print("Model preparation skipped. Set PREPARE_MODEL=true to enable preparation.")
        return

    model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    cache_dir = "/root/.cache/huggingface/hub"
    output_dir = "/models/llama/1"
    preparation_flag = "/models/llama/preparation_complete"

    if os.path.exists(preparation_flag):
        print("Model has already been prepared. Skipping preparation.")
        return

    print(f"Preparing model: {model_name}")
    
    # Download and save the model
    model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, torch_dtype=torch.float32)
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

    print(f"Saving model to: {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    with open(preparation_flag, 'w') as f:
        f.write('Preparation completed')

    print("Model preparation complete")

if __name__ == "__main__":
    prepare_model()