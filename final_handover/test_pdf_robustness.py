
import fitz
import cv2
import numpy as np

from print_scan_simulator import PrintScanSimulator


def create_test_pdf():
    """
    Create a simple PDF for robustness testing.
    """

    pdf = fitz.open()

    page = pdf.new_page(
        width=595,
        height=842
    )

    # Title
    page.insert_text(
        (60, 100),
        "SIH WATERMARK PDF ROBUSTNESS TEST",
        fontsize=20
    )

    # Recipient
    page.insert_text(
        (60, 180),
        "Recipient: RECIPIENT_001",
        fontsize=14
    )

    # Timestamp
    page.insert_text(
        (60, 220),
        "Timestamp: 1790703418",
        fontsize=14
    )

    # Test description
    page.insert_text(
        (60, 300),
        "This PDF is being used to test",
        fontsize=14
    )

    page.insert_text(
        (60, 330),
        "print-scan and JPEG compression robustness.",
        fontsize=14
    )

    # Rectangle
    page.draw_rect(
        fitz.Rect(40, 50, 550, 400),
        color=(0, 0, 0),
        width=2
    )

    pdf.save("test_robustness.pdf")
    pdf.close()


def render_pdf_to_image(pdf_path):
    """
    Render the first PDF page into a NumPy image.
    """

    pdf = fitz.open(pdf_path)

    page = pdf[0]

    # Render at 150 DPI
    zoom = 150 / 72

    matrix = fitz.Matrix(
        zoom,
        zoom
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

    pdf.close()

    return image


def main():

    print("=" * 60)
    print("PDF ROBUSTNESS TEST")
    print("=" * 60)

    # -----------------------------------------
    # Step 1: Create PDF
    # -----------------------------------------

    create_test_pdf()

    print("\nPDF created:")
    print("test_robustness.pdf")

    # -----------------------------------------
    # Step 2: Convert PDF page to image
    # -----------------------------------------

    print("\nRendering PDF page...")

    pdf_image = render_pdf_to_image(
        "test_robustness.pdf"
    )

    cv2.imwrite(
        "pdf_rendered_original.png",
        pdf_image
    )

    print(
        "Rendered image: pdf_rendered_original.png"
    )

    # -----------------------------------------
    # Step 3: Create simulator
    # -----------------------------------------

    simulator = PrintScanSimulator()

    # -----------------------------------------
    # Step 4: Run robustness tests
    # -----------------------------------------

    print("\nRunning PDF robustness tests...")

    results = simulator.test_robustness(
        pdf_image
    )

    # -----------------------------------------
    # Step 5: Save results
    # -----------------------------------------

    for test_name, data in results.items():

        filename = (
            "pdf_"
            + test_name
            + ".jpg"
        )

        image = data["image"]

        # Convert PIL Image to NumPy array if needed
        if not isinstance(image, np.ndarray):
            image = np.array(image)

        # Convert RGB to BGR for OpenCV
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(
                image,
                cv2.COLOR_RGB2BGR
            )

        cv2.imwrite(
            filename,
            image
        )

        print("\n" + test_name)
        print("-" * 40)

        print(
            f"Output file : {filename}"
        )

        print(
            f"PSNR        : {data['psnr']:.2f} dB"
        )

        print(
            f"SSIM        : {data['ssim']:.4f}"
        )

    print("\n" + "=" * 60)
    print("PDF ROBUSTNESS TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()