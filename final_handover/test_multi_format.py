from pathlib import Path
import time

from multi_format_watermarker import MultiFormatWatermarker


input_file = Path("sample.docx")
output_file = Path("multi_watermarked.docx")

watermarker = MultiFormatWatermarker()

original_bytes = input_file.read_bytes()

recipient_id = "SIH_RECIPIENT_001"
timestamp = int(time.time())

print("========== MULTI-FORMAT TEST ==========")

# Watermark through unified interface
watermarked_bytes = watermarker.watermark_document(
    original_bytes,
    input_file.name,
    recipient_id,
    timestamp
)

output_file.write_bytes(watermarked_bytes)

print("Format detected:", watermarker._detect_format(input_file.name))
print("Watermarked file:", output_file)

# Extract through unified interface
result = watermarker.extract_watermark(
    watermarked_bytes,
    output_file.name
)

print()
print("Recipient ID:", result["recipient_id"])
print("Timestamp:", result["timestamp"])
print("Checksum valid:", result["checksum_valid"])

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

print("=======================================")