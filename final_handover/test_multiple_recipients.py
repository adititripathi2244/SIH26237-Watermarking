from pathlib import Path
import time

from docx_watermarker import DOCXWatermarker


input_file = Path("sample.docx")
original_bytes = input_file.read_bytes()

watermarker = DOCXWatermarker()

test_recipients = [
    "RECIPIENT_001",
    "RECIPIENT_ABC",
    "USER_12345"
]

print("========== MULTI-RECIPIENT TEST ==========")

for recipient_id in test_recipients:

    timestamp = int(time.time())

    watermarked_bytes = watermarker.embed_watermark(
        original_bytes,
        recipient_id,
        timestamp
    )

    extracted = watermarker.extract_watermark(
        watermarked_bytes
    )

    print()
    print("Original Recipient :", recipient_id)
    print("Extracted Recipient:", extracted["recipient_id"])
    print("Original Timestamp :", timestamp)
    print("Extracted Timestamp:", extracted["timestamp"])
    print("Checksum Valid     :", extracted["checksum_valid"])

    if (
        extracted["recipient_id"] == recipient_id
        and extracted["timestamp"] == timestamp
        and extracted["checksum_valid"]
    ):
        print("RESULT             : PASS ✅")
    else:
        print("RESULT             : FAIL ❌")

print()
print("===========================================")