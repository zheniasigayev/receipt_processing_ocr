# Receipt/Invoice Processing
This tool can extract structured information from receipt or invoice images using openbmb/MiniCPM-V-2_6.

## Quickstart (MacOS)
Run `setup.sh` 

## Example Output
Given this sample invoice image:

<img src="receipts/restaurant_catering_invoice.png" width="30%">

**Extracted JSON:**
```json
{
  "merchant_name": "Culinary Delights Catering",
  "date": "2030-01-15",
  "total_amount": 8534.00
}
```