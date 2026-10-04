import fitz
import time
import os

PDF_NAME = "speed_test_10_pages.pdf"

def create_10_page_pdf():
    pdf = fitz.open()

    for i in range(1, 11):
        page = pdf.new_page(width=595, height=842)

        page.insert_text(
            (60, 100),
            f"SIH WATERMARK SPEED TEST - PAGE {i}",
            fontsize=20
        )

        page.insert_text(
            (60, 160),
            "Cryptographic Attribution and Immutable "
            "Decryption Provenance Testing",
            fontsize=13
        )

        page.insert_text(
            (60, 220),
            "This document is used to measure PDF processing speed.",
            fontsize=12
        )

        page.insert_text(
            (60, 270),
            "Recipient: RECIPIENT_001",
            fontsize=12
        )

        page.insert_text(
            (60, 320),
            "Watermark robustness and rendering test.",
            fontsize=12
        )

    pdf.save(PDF_NAME)
    pdf.close()


def measure_rendering_speed():
    pdf = fitz.open(PDF_NAME)

    start_time = time.perf_counter()

    for page_number in range(len(pdf)):
        page = pdf[page_number]

        matrix = fitz.Matrix(150 / 72, 150 / 72)

        pix = page.get_pixmap(
            matrix=matrix,
            alpha=False
        )

    end_time = time.perf_counter()

    pdf.close()

    elapsed = end_time - start_time

    return elapsed


def main():

    print("=" * 60)
    print("PHASE 3 — 10-PAGE PDF SPEED TEST")
    print("=" * 60)

    print("\nCreating 10-page PDF...")
    create_10_page_pdf()

    print(f"Created: {PDF_NAME}")
    print(f"File size: {os.path.getsize(PDF_NAME)} bytes")

    print("\nRendering all 10 pages...")

    elapsed = measure_rendering_speed()

    print("\n" + "=" * 60)
    print("SPEED TEST RESULT")
    print("=" * 60)

    print(f"Pages processed : 10")
    print(f"Time taken      : {elapsed:.4f} seconds")
    print(f"Target          : < 2.00 seconds")

    if elapsed < 2.0:
        print("RESULT          : PASS")
    else:
        print("RESULT          : FAIL")

    print("=" * 60)


if __name__ == "__main__":
    main()