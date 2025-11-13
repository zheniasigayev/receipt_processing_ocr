#!/bin/bash
set -e

cd ~/Downloads/

git clone https://github.com/zheniasigayev/receipt_processing_ocr.git
cd receipt_processing_ocr

brew install ollama
ollama pull openbmb/minicpm-v2.6

read -p "Confirm you have opened a new terminal and have ran 'ollama serve' (y/n): " confirm
if [ "$confirm" != "y" ]; then
    exit 1
fi

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 demo.py