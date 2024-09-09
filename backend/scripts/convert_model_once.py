import os
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

def convert_model():
    if os.environ.get('CONVERT_MODEL', 'false').lower() != 'true':
        print("Model conversion skipped. Set CONVERT_MODEL=true to enable conversion.")
        return

    model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    cache_dir = "/root/.cache/huggingface/hub"
    output_dir = "/models/llama/1"
    conversion_flag = "/models/llama/conversion_complete"

    if os.path.exists(conversion_flag):
        print("Model has already been converted. Skipping conversion.")
        return

    print(f"Loading model: {model_name}")
    try:
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True)
        tokenizer.save_pretrained(output_dir)
        print("Tokenizer saved.")

        # Load model configuration
        config = AutoModelForCausalLM.from_config(AutoModelForCausalLM.from_pretrained(model_name, cache_dir=cache_dir, local_files_only=True).config)

        # Initialize empty model
        with init_empty_weights():
            model = AutoModelForCausalLM.from_config(config)

        # Load checkpoint in parts
        model = load_checkpoint_and_dispatch(
            model,
            cache_dir,
            device_map="auto",
            no_split_module_classes=["LlamaDecoderLayer"],
            dtype=torch.float32,
            offload_folder="/tmp/offload"
        )

        print(f"Saving model to: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)

        # Save model in parts
        model.save_pretrained(output_dir, max_shard_size="1GB", safe_serialization=True)

        with open(conversion_flag, 'w') as f:
            f.write('Conversion completed')

        print("Model preparation complete")
    except Exception as e:
        print(f"Error during model conversion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    convert_model()