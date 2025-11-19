from google_cloud_vision_ocr import scan_receipt
from receipt_ocr_text_tiny_llm import extract_receipt_data_from_text

import logging
logger = logging.getLogger("receipt_ocr")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)5s | %(message)s",
)


if __name__ == "__main__":
    # Use Google Cloud Vision 
    # https://docs.cloud.google.com/vision/docs/ocr
        # https://cloud.google.com/vision/docs/features-list
        # https://cloud.google.com/vision/docs/reference/rest/v1/Feature

    raw_text: str = scan_receipt("receipts/restaurant_catering_invoice.png")

    try:
        receipt = extract_receipt_data_from_text(raw_text)
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise
