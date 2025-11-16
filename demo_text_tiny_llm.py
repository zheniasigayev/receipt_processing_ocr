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

    # OR paste raw OCR text directly for testing
    raw_text = "Gmail-Order Invoice\nGmail\nby Google\nOrder Invoice\nBest Buy <orders@bestbuy.com>\nTo: Maverickpaull@gmail.com\nBEST\nBUY\nCall us on 1-888-237-8289.\n> My Account\nInvoice Receipt\nPAID\n05/10/2019 17:59\nMaverick Paul<Maverrickpaull@gmail.com>\n05 October 2019 19:33\nGeek\nSQUAD\nDear Mr Maverick.\nFollowing the despatch of the items shown below, we would like to confirm that we have now billed you via your nominated payment method.\nYOUR ORDER DETAILS Order Date: 05 Oct 2019 Order Number: 3011852293\nBilling Address\nMr Paul Maverick\n9132 50th Ave\n3RD FI\nElmhurst NY 11373-4000\nUnited States\nItem Description\nItem\nNumber\nIPHONE 11 PRO Space Gray 1000164268\n256gb\nImei: 35323910026168\nSerial Number:DNPZ901GN6XR\nDelivery Address\nMr Paul Maverick\n9132 50th Ave\n3RD FI\nElmhurst NY 11373-4000\nUnited States\nNet price\nQuantity\nOrdered\nQuantity\nDespatched\n$930.66\n1\n1\nGross\nPrice\n$865.98\nVAT\nVAT %\n\u00a374.00 0.00%\nPAYMENT METHOD\n$ 865.98 Charged to VISADEBIT xxxx-xxxxxxx-xxxxxxx-7730\nFor a total of \u00a3 865.98\nADDITIONAL DETAILS\nSub Total:\n$ 865.98\nVAT:\n$ 74.00\nTotal\n$ 939.98\nAmount Due: $ 0.00\nInvoice Number\nInvoice Date\n0091427793\n05 October 2019\nPayment Type\nCredit Card\nDispatch Date\n05 October 2019\nFOR ANY QUERIES\nFor more information or If you have any questions about your order, please call us on 1-888-237-8289 (this phone number will remain in operation after\nstore closure. Calls to this number are free on some call plans but may be chargeable).\nThank you for shopping at Best Buy,\nThe Best Buy Team\nThis email is sent to you by Best Buy, a trading division of The Carphone Warehouse Limited, a company registered in United States, under number\n764478 with registered office located at 7601 Penn Avenue S., Richfield, Minnesota, 55423\nBest Buy United States Limited\nhttps://mail.google.com/mail/?ui=2&ik-821655df7d&view=pt&q=bestbuy&qs=true&search query&msg=1342ea478ef04514\nPage 1 of 2"
    logger.info("Processing receipt text")

    try:
        receipt = extract_receipt_data_from_text(raw_text)
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise
