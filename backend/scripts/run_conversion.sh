#!/bin/bash

# Check if the model has already been converted
if [ ! -f "/models/llama/conversion_complete" ]; then
    echo "Starting model conversion..."
    python /app/convert_model_once.py
    if [ $? -eq 0 ]; then
        echo "Model conversion completed successfully."
    else
        echo "Model conversion failed."
        exit 1
    fi
else
    echo "Model has already been converted. Skipping conversion."
fi

# Start Triton server
exec tritonserver --model-repository=/models