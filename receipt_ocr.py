"""
Simplified receipt OCR helper for extracting retail totals.
"""

from dataclasses import dataclass, asdict
import json
import logging
from pathlib import Path
import tempfile

import ollama
from PIL import Image, ImageEnhance, ImageOps


DEFAULT_MODEL = "openbmb/minicpm-v2.6"

logger = logging.getLogger("receipt_ocr")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)5s | %(message)s",
)


@dataclass
class ReceiptExtractionResult:
    merchant_name: str
    date: str
    total_amount: float


def build_prompt() -> str:
    return """Extract structured data from the attached receipt image.

Rules:
- The TOTAL line always appears AFTER tax lines and AFTER the word SUBTOTAL.
- Ignore loyalty, cashback, cash received, gift card reloads, or duplicate totals.
- If multiple totals exist, choose the one explicitly paired with the word "TOTAL".
- Dates must be normalized to YYYY-MM-DD regardless of the format found.
- Merchant names should match exactly as printed on the receipt.
- Return strictly valid JSON with numbers as floats, not strings.

Output ONLY the following JSON schema:
{
  "merchant_name": "string",
  "date": "YYYY-MM-DD",
  "total_amount": number
}

Example:
RECEIPT: TRADER JOE'S, DATE 2023-07-14, SUBTOTAL 18.75, TAX 1.31, TOTAL USD 20.06

JSON:
{
  "merchant_name": "TRADER JOE'S",
  "date": "2023-07-14",
  "total_amount": 20.06
}"""


def preprocess_image(image_path: Path) -> Path:
    """Apply grayscale and contrast enhancement to improve OCR accuracy."""
    image = Image.open(image_path)
    
    # Apply EXIF rotation
    image = ImageOps.exif_transpose(image)
    
    # Convert to grayscale
    image = ImageOps.grayscale(image)
    
    # Enhance contrast and sharpness
    image = ImageEnhance.Contrast(image).enhance(1.8)
    image = ImageEnhance.Sharpness(image).enhance(1.2)
    
    max_width = 2048
    if image.width > max_width:
        ratio = max_width / image.width
        new_size = (max_width, int(image.height * ratio))
        image = image.resize(new_size)
    
    tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    image.save(tmp_file.name, format="PNG")
    tmp_path = Path(tmp_file.name)
    tmp_file.close()
    
    return tmp_path


def extract_receipt_data(image_path: str) -> ReceiptExtractionResult:
    """Extract receipt data from image using Ollama vision model."""
    path = Path(image_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    
    processed_path = preprocess_image(path)
    
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a meticulous retail receipt analyst. Always double-check totals, dates, and store names.",
            },
            {
                "role": "user",
                "content": build_prompt(),
                "images": [str(processed_path)],
            },
        ]
        
        response = ollama.chat(
            model=DEFAULT_MODEL,
            messages=messages,
            options={
                "cache": False,
                "seed": 0,
                "temperature": 0,
                "num_ctx": 4096
            },
            format='json'
        )
        
        raw_text = response.get("message", {}).get("content", "").strip()
        
        payload = json.loads(raw_text)
        
        result = ReceiptExtractionResult(
            merchant_name=payload.get("merchant_name"),
            date=payload.get("date"),
            total_amount=float(payload.get("total_amount", 0))
        )
        
        logger.info("Extraction successful")
        return result
        
    finally:
        try:
            processed_path.unlink(missing_ok=True)
        except:
            pass


def save_extracted_receipt_data(receipt: ReceiptExtractionResult, output_path: str) -> None:
    path = Path(output_path)

    with path.open("w") as f:
        json.dump(asdict(receipt), f, indent=2)
    
    logger.info(f"Saved receipt JSON to {path}")
