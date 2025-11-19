#!/usr/bin/env python3
"""
Simplified Receipt Scanner
Extract raw text from receipt using Google Cloud Vision
"""

from google.cloud import vision
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scan_receipt(image_path: str) -> str:
    """
    Upload receipt image to Google Cloud Vision and extract raw text.
    JPG, PNG formats supported, less than 20MB
    PDF supported, less than 5 pages, and less than 2MB
    """
    client: vision.ImageAnnotatorClient = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content: bytes = image_file.read()
    
    image = vision.Image(content=content)
    response: vision.AnnotateImageResponse = client.document_text_detection(image=image)
    
    text = response.full_text_annotation.text

    return text
