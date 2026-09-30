from pathlib import Path
from docx_watermarker import DOCXWatermarker

watermarked_file = Path("watermarked_sample.docx")

watermarked_bytes = watermarked_file.read_bytes()

print("Reading:", watermarked_file)
print("File size:", len(watermarked_bytes), "bytes")

watermarker = DOCXWatermarker()

result = watermarker.extract_watermark(watermarked_bytes)

print()
print("========== EXTRACTED WATERMARK ==========")
print("Recipient ID:", result["recipient_id"])
print("Timestamp:", result["timestamp"])
print("Version:", result["version"])
print("Checksum valid:", result["checksum_valid"])
print("==========================================")