#!/bin/bash

# Create and Activate Python Virtual Environment

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip


if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Skipping package installation."
fi

echo "Virtual environment setup complete!"
echo "To activate manually later, run: source venv/bin/activate"
