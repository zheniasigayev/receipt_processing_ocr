"""
Receipt text extraction helper for pulling merchant, date, and total
from raw OCR text (already extracted).
"""

import json
import logging
import re
import unicodedata

from dataclasses import dataclass

# Uncomment if you want to see token counts
# from llama_cpp import Llama
import ollama


DEFAULT_MODEL = "smollm2:135m" # Can also use "smollm2:360m", still has 8096 token context
# LLAMA_TOKENIZER = Llama(model_path="INSERT_PATH_HERE", vocab_only=True, seed=0)

logger = logging.getLogger("receipt_extractor")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)5s | %(message)s",
)

@dataclass
class ReceiptExtractionResult:
    merchant_name: str
    date: str
    total_amount: float

# def count_tokens_llama(text: str) -> int:
#     return len(LLAMA_TOKENIZER.tokenize(text.encode("utf-8")))

def clean_receipt_text_minimal(text: str) -> str:
    """
    1. Normalize unicode (safe, prevents weird OCR chars)
    2. Replace tabs with spaces
    3. Trim whitespace from start/end
    """
    if not text:
        return ""

    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\t", " ")
    text = text.strip()

    return text

def build_prompt(raw_text: str) -> str:
    return f"""
You are a retail receipt text analyzer.

You will be given ONLY raw OCR text (no images).
Extract the following three fields:

- merchant_name (exactly as printed)
- date (normalize to YYYY-MM-DD)
- total_amount (float)

Rules:
- "TOTAL" always appears after SUBTOTAL and TAX lines.
- Do NOT include cashback, cash received, or gift card reloads.
- If multiple totals appear, choose the one explicitly associated with the word TOTAL.
- If the date appears in multiple formats, pick the most explicit one.
- If the merchant name is ambiguous, use the top-most store-like name.
- Return strictly valid JSON.

RAW TEXT:
\"\"\"{raw_text}\"\"\"

Respond ONLY with valid JSON like this:
{{
  "merchant_name": "WALL-MART-SUPERSTORE",
  "date": "2020-10-17",
  "total_amount": 27.27
}}
"""

def parse_float(value) -> float:
    if value is None:
        return 0.0

    text = str(value)

    # Extract the first number (integer or decimal)
    match = re.search(r"\d+(?:\.\d+)?", text)

    if not match:
        return 0.0

    try:
        num = float(match.group(0))
        # Totals cannot be negative 
        return max(num, 0.0)
    except ValueError:
        return 0.0

def extract_receipt_data_from_text(raw_text: str) -> ReceiptExtractionResult:
    """Extract receipt structured fields from raw OCR text using Ollama."""
    raw_text = clean_receipt_text_minimal(raw_text)

    if not raw_text:
        logger.warning("Empty raw text provided for extraction")
        return ReceiptExtractionResult("", "", 0.0)

    # llm_token_count = count_tokens_llama(raw_text)
    # logger.info(f"Raw text token count (llama_cpp): {llm_token_count}")

    prompt = build_prompt(raw_text)

    messages = [
        {
            "role": "system",
            "content": "You are an expert receipt parser. Extract only merchant_name, date, and total_amount.",
        },
        {
            "role": "user",
            "content": prompt,
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

    raw_json = response.get("message", {}).get("content", "").strip()

    try:
        payload = json.loads(raw_json)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON from model:\n{raw_json}")
        raise e

    result = ReceiptExtractionResult(
        merchant_name=payload.get("merchant_name"),
        date=payload.get("date"),
        total_amount=parse_float(payload.get("total_amount"))
    )

    logger.info("Found the following details:")
    logger.info(f"Merchant Name: {result.merchant_name}")
    logger.info(f"Date         : {result.date}")
    logger.info(f"Total Amount : ${result.total_amount:.2f}")

    return result
