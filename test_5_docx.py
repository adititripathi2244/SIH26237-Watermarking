from pathlib import Path
import time

from multi_format_watermarker import MultiFormatWatermarker


watermarker = MultiFormatWatermarker()

total_tests = 5
passed_tests = 0

print("========== 5-DOCX ACCURACY TEST ==========")

for i in range(1, 6):

    input_file = Path(f"test_doc_{i}.docx")

    original_bytes = input_file.read_bytes()

    recipient_id = f"RECIPIENT_{i:03d}"
    timestamp = int(time.time())

    # Embed watermark
    watermarked_bytes = watermarker.watermark_document(
        original_bytes,
        input_file.name,
        recipient_id,
        timestamp
    )

    # Extract watermark
    result = watermarker.extract_watermark(
        watermarked_bytes,
        input_file.name
    )

    passed = (
        result["recipient_id"] == recipient_id
        and result["timestamp"] == timestamp
        and result["checksum_valid"]
    )

    if passed:
        passed_tests += 1

    print()
    print(f"Document {i}: {input_file.name}")
    print("Expected Recipient :", recipient_id)
    print("Extracted Recipient:", result["recipient_id"])
    print("Expected Timestamp :", timestamp)
    print("Extracted Timestamp:", result["timestamp"])
    print("Checksum Valid     :", result["checksum_valid"])
    print("Result             :", "PASS" if passed else "FAIL")


accuracy = (passed_tests / total_tests) * 100

print()
print("==========================================")
print("Total Tests :", total_tests)
print("Passed      :", passed_tests)
print("Failed      :", total_tests - passed_tests)
print(f"Accuracy    : {accuracy:.2f}%")
print("==========================================")

if accuracy > 85:
    print("CHECKPOINT: >85% ACCURACY PASSED")
else:
    print("CHECKPOINT: >85% ACCURACY FAILED")