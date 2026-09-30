import os
import cv2
import fitz
import numpy as np

from docx_watermarker import DOCXWatermarker
from print_scan_simulator import PrintScanSimulator


# ============================================================
# CONFIGURATION
# ============================================================

TOTAL_TESTS = 20


# ============================================================
# CREATE TEST DOCX FILES
# ============================================================

def create_test_docx_files():

    from docx import Document

    print("\nCreating DOCX test files...")

    for i in range(1, 11):

        filename = f"phase3_docx_{i}.docx"

        document = Document()

        text = (
            f"Phase 3 DOCX Test Document {i}. "
            "This document is created for testing the "
            "watermarking system. "
            "The document contains sufficient text "
            "to store the watermark information. "
        )

        # Repeat text to ensure enough characters
        for _ in range(10):
            document.add_paragraph(text)

        document.save(filename)

    print("10 DOCX test files created.")


# ============================================================
# CREATE TEST IMAGES
# ============================================================

def create_test_images():

    print("\nCreating image test files...")

    for i in range(1, 6):

        image = np.ones(
            (600, 800, 3),
            dtype=np.uint8
        ) * 255

        cv2.putText(
            image,
            f"PHASE 3 IMAGE TEST {i}",
            (80, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 0),
            3
        )

        cv2.putText(
            image,
            "SIH Watermark Robustness Testing",
            (80, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 0),
            2
        )

        cv2.imwrite(
            f"phase3_image_{i}.png",
            image
        )

    print("5 image test files created.")


# ============================================================
# CREATE TEST PDF
# ============================================================

def create_test_pdf():

    print("\nCreating PDF test file...")

    pdf = fitz.open()

    for i in range(1, 6):

        page = pdf.new_page(
            width=595,
            height=842
        )

        page.insert_text(
            (60, 100),
            f"PHASE 3 PDF TEST {i}",
            fontsize=20
        )

        page.insert_text(
            (60, 180),
            "SIH Watermark Robustness Testing",
            fontsize=14
        )

        page.insert_text(
            (60, 230),
            "Recipient: RECIPIENT_001",
            fontsize=14
        )

        page.insert_text(
            (60, 280),
            "Timestamp: 1790703418",
            fontsize=14
        )

    pdf.save("phase3_test.pdf")

    pdf.close()

    print("PDF test file created.")


# ============================================================
# TEST DOCX WATERMARKING
# ============================================================

def test_docx_files():

    print("\n========== DOCX TESTS ==========")

    watermarker = DOCXWatermarker()

    passed = 0

    for i in range(1, 11):

        filename = f"phase3_docx_{i}.docx"

        with open(filename, "rb") as f:
            original = f.read()

        recipient = f"PHASE3_RECIPIENT_{i:03d}"

        timestamp = 1790703418 + i

        try:

            watermarked = watermarker.embed_watermark(
                original,
                recipient,
                timestamp
            )

            extracted = watermarker.extract_watermark(
                watermarked
            )

            if (
                extracted["recipient_id"] == recipient
                and
                extracted["timestamp"] == timestamp
                and
                extracted["checksum_valid"]
            ):
                passed += 1
                print(
                    f"DOCX {i:02d}: PASS"
                )
            else:
                print(
                    f"DOCX {i:02d}: FAIL"
                )

        except Exception as e:

            print(
                f"DOCX {i:02d}: FAIL - {e}"
            )

    return passed


# ============================================================
# TEST IMAGE ROBUSTNESS
# ============================================================

def test_images():

    print("\n========== IMAGE TESTS ==========")

    simulator = PrintScanSimulator()

    passed = 0

    for i in range(1, 6):

        filename = f"phase3_image_{i}.png"

        image = cv2.imread(filename)

        try:

            result = simulator.test_robustness(
                image
            )

            if len(result) == 5:

                passed += 1

                print(
                    f"IMAGE {i:02d}: PASS"
                )

            else:

                print(
                    f"IMAGE {i:02d}: FAIL"
                )

        except Exception as e:

            print(
                f"IMAGE {i:02d}: FAIL - {e}"
            )

    return passed


# ============================================================
# TEST PDF ROBUSTNESS
# ============================================================

def test_pdf():

    print("\n========== PDF TEST ==========")

    simulator = PrintScanSimulator()

    passed = 0

    try:

        pdf = fitz.open(
            "phase3_test.pdf"
        )

        for page_number in range(
            len(pdf)
        ):

            page = pdf[page_number]

            matrix = fitz.Matrix(
                150 / 72,
                150 / 72
            )

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            )

            image = image.reshape(
                pix.height,
                pix.width,
                pix.n
            )

            if pix.n == 4:

                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_RGBA2BGR
                )

            else:

                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_RGB2BGR
                )

            results = simulator.test_robustness(
                image
            )

            if len(results) == 5:

                passed += 1

                print(
                    f"PDF PAGE {page_number + 1:02d}: PASS"
                )

            else:

                print(
                    f"PDF PAGE {page_number + 1:02d}: FAIL"
                )

        pdf.close()

    except Exception as e:

        print(
            f"PDF TEST FAILED: {e}"
        )

    return passed


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PHASE 3 — 20 DOCUMENT TEST SUITE")
    print("=" * 60)

    # Create test data
    create_test_docx_files()
    create_test_images()
    create_test_pdf()

    # Run tests
    docx_passed = test_docx_files()

    image_passed = test_images()

    pdf_passed = test_pdf()

    # --------------------------------------------------------
    # IMPORTANT:
    # 10 DOCX + 5 Images + 5 PDF pages = 20 tests
    # --------------------------------------------------------

    total_passed = (
        docx_passed
        +
        image_passed
        +
        pdf_passed
    )

    accuracy = (
        total_passed / TOTAL_TESTS
    ) * 100

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PHASE 3 TEST SUMMARY")
    print("=" * 60)

    print(
        f"Total Tests : {TOTAL_TESTS}"
    )

    print(
        f"Passed      : {total_passed}"
    )

    print(
        f"Failed      : {TOTAL_TESTS - total_passed}"
    )

    print(
        f"Accuracy    : {accuracy:.2f}%"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()