import os
from docx_watermarker import DOCXWatermarker
from print_scan_simulator import PrintScanSimulator


def test_watermark_robustness():

    print("=" * 60)
    print("WATERMARK ROBUSTNESS TEST")
    print("=" * 60)

    # -----------------------------------------
    # Step 1: Load original DOCX
    # -----------------------------------------

    input_file = "sample.docx"

    if not os.path.exists(input_file):
        print(f"ERROR: {input_file} not found.")
        return

    with open(input_file, "rb") as f:
        original_docx = f.read()

    print(f"\nOriginal document: {input_file}")
    print(f"Original size: {len(original_docx)} bytes")

    # -----------------------------------------
    # Step 2: Embed watermark
    # -----------------------------------------

    watermarker = DOCXWatermarker()

    recipient_id = "ROBUSTNESS_TEST_001"
    timestamp = 1790703418

    watermarked_docx = watermarker.embed_watermark(
        original_docx,
        recipient_id,
        timestamp
    )

    print("\nWatermark embedded successfully.")
    print(f"Recipient ID: {recipient_id}")

    # -----------------------------------------
    # Step 3: Save watermarked DOCX
    # -----------------------------------------

    watermarked_file = "robustness_watermarked.docx"

    with open(watermarked_file, "wb") as f:
        f.write(watermarked_docx)

    print(f"Saved: {watermarked_file}")

    # -----------------------------------------
    # Step 4: Extract watermark
    # -----------------------------------------

    extracted = watermarker.extract_watermark(
        watermarked_docx
    )

    print("\n========== ORIGINAL EXTRACTION ==========")

    print(
        "Extracted Recipient:",
        extracted["recipient_id"]
    )

    print(
        "Extracted Timestamp:",
        extracted["timestamp"]
    )

    print(
        "Checksum:",
        extracted["checksum_valid"]
    )

    if extracted["recipient_id"] == recipient_id:
        print("Original watermark extraction: PASS")
    else:
        print("Original watermark extraction: FAIL")

    # -----------------------------------------
    # Step 5: Initialize simulator
    # -----------------------------------------

    simulator = PrintScanSimulator()

    print("\n==========================================")
    print("ROBUSTNESS PIPELINE READY")
    print("==========================================")

    print("\nNext stage:")
    print("DOCX → Watermark → Print/Scan → Extract")

    print("\nNOTE:")
    print("The current simulator works on images.")
    print("DOCX-to-image conversion will be handled")
    print("in the next step.")


if __name__ == "__main__":
    test_watermark_robustness()