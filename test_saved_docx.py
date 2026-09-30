from pathlib import Path
import time

from docx_watermarker import DOCXWatermarker


input_file = Path("sample.docx")
output_file = Path("saved_watermarked.docx")

watermarker = DOCXWatermarker()

recipient_id = "SIH_RECIPIENT_001"
timestamp = int(time.time())

# Read original DOCX
original_bytes = input_file.read_bytes()

# Embed watermark
watermarked_bytes = watermarker.embed_watermark(
    original_bytes,
    recipient_id,
    timestamp
)

# Save actual DOCX file
output_file.write_bytes(watermarked_bytes)

print("Watermarked file saved:", output_file)
print("Saved file size:", output_file.stat().st_size, "bytes")

# Read the saved DOCX again
saved_bytes = output_file.read_bytes()

# Extract watermark from the saved file
result = watermarker.extract_watermark(saved_bytes)

print()
print("========== SAVED DOCX TEST ==========")
print("Original Recipient :", recipient_id)
print("Extracted Recipient:", result["recipient_id"])
print("Original Timestamp :", timestamp)
print("Extracted Timestamp:", result["timestamp"])
print("Checksum Valid     :", result["checksum_valid"])

if (
    result["recipient_id"] == recipient_id
    and result["timestamp"] == timestamp
    and result["checksum_valid"]
):
    print()
    print("RESULT: PASS ✅")
else:
    print()
    print("RESULT: FAIL ❌")

print("=====================================")