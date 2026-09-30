import cv2
import numpy as np

from print_scan_simulator import PrintScanSimulator


def create_test_image():
    """
    Create a simple test image for robustness testing.
    """

    image = np.ones(
        (800, 1000, 3),
        dtype=np.uint8
    ) * 255

    # Main heading
    cv2.putText(
        image,
        "SIH WATERMARK ROBUSTNESS TEST",
        (80, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.4,
        (0, 0, 0),
        3
    )

    # Recipient information
    cv2.putText(
        image,
        "Recipient: RECIPIENT_001",
        (100, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 0),
        2
    )

    # Timestamp
    cv2.putText(
        image,
        "Timestamp: 1790703418",
        (100, 320),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 0),
        2
    )

    # Test information
    cv2.putText(
        image,
        "Print-Scan and Compression Test",
        (100, 450),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 0),
        2
    )

    # Rectangle for visual structure
    cv2.rectangle(
        image,
        (70, 70),
        (930, 550),
        (0, 0, 0),
        2
    )

    return image


def main():

    print("=" * 60)
    print("IMAGE ROBUSTNESS TEST")
    print("=" * 60)

    # -----------------------------------------
    # Step 1: Create test image
    # -----------------------------------------

    original_image = create_test_image()

    cv2.imwrite(
        "robustness_original.png",
        original_image
    )

    print("\nOriginal image created:")
    print("robustness_original.png")

    # -----------------------------------------
    # Step 2: Create simulator
    # -----------------------------------------

    simulator = PrintScanSimulator()

    # -----------------------------------------
    # Step 3: Run robustness tests
    # -----------------------------------------

    print("\nRunning robustness tests...")

    results = simulator.test_robustness(
        original_image
    )

    # -----------------------------------------
    # Step 4: Save results
    # -----------------------------------------

    for test_name, data in results.items():

        filename = (
            "robustness_"
            + test_name
            + ".jpg"
        )

        cv2.imwrite(
            filename,
            data["image"]
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
    print("IMAGE ROBUSTNESS TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()