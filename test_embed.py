from pathlib import Path
import time

from docx_watermarker import DOCXWatermarker


# ---------------------------------------------------------
# 1. Read original DOCX
# ---------------------------------------------------------

input_file = Path("sample.docx")

original_bytes = input_file.read_bytes()

print("Original DOCX size:", len(original_bytes), "bytes")


# ---------------------------------------------------------
# 2. Create watermarker
# ---------------------------------------------------------

watermarker = DOCXWatermarker()


# ---------------------------------------------------------
# 3. Information we want to embed
# ---------------------------------------------------------

recipient_id = "RECIPIENT_001"

timestamp = int(time.time())

print("Recipient ID:", recipient_id)
print("Timestamp:", timestamp)


# ---------------------------------------------------------
# 4. Embed watermark
# ---------------------------------------------------------

watermarked_bytes = watermarker.embed_watermark(
    original_bytes,
    recipient_id,
    timestamp
)


# ---------------------------------------------------------
# 5. Save watermarked DOCX
# ---------------------------------------------------------

output_file = Path("watermarked_sample.docx")

output_file.write_bytes(watermarked_bytes)

print()
print("Watermark embedded successfully!")
print("Watermarked file:", output_file)
print(
    "Watermarked DOCX size:",
    len(watermarked_bytes),
    "bytes"
)