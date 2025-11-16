from receipt_ocr_vision_llm import extract_receipt_data

import logging
logger = logging.getLogger("receipt_ocr")


if __name__ == "__main__":
    image_path = "receipts/restaurant_catering_invoice.png"

    logger.info(f"Processing: {image_path}")
        
    try:
        receipt = extract_receipt_data(image_path)

        logger.info(f"Merchant : {receipt.merchant_name}")
        logger.info(f"Date     : {receipt.date}")
        logger.info(f"Total    : ${receipt.total_amount:.2f}")

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise
