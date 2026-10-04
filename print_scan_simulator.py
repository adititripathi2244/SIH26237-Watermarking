import cv2
import numpy as np
from PIL import Image, ImageFilter


class PrintScanSimulator:

    # =================================================
    # PRINT-SCAN SIMULATION
    # =================================================

    def simulate_print_scan(
        self,
        image,
        dpi=300,
        jpeg_quality=95
    ):
        """
        Simulate a basic print-scan process.
        """

        if image is None:
            raise ValueError("Input image cannot be None.")

        image = np.asarray(image)

        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255).astype(np.uint8)

        height, width = image.shape[:2]

        # Simulate printing resolution
        scale = dpi / 300.0

        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))

        printed = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_CUBIC
        )

        # Simulate scanning
        scanned = cv2.resize(
            printed,
            (width, height),
            interpolation=cv2.INTER_LINEAR
        )

        # Simulate JPEG compression
        success, encoded = cv2.imencode(
            ".jpg",
            scanned,
            [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
        )

        if not success:
            raise RuntimeError("JPEG encoding failed.")

        result = cv2.imdecode(
            encoded,
            cv2.IMREAD_COLOR
        )

        if result is None:
            raise RuntimeError("JPEG decoding failed.")

        return result


    # =================================================
    # SCREENSHOT SIMULATION
    # =================================================

    def simulate_screenshot(
        self,
        image,
        scale=1.0,
        jpeg_quality=90
    ):
        """
        Simulate taking a screenshot of an image.
        """

        if image is None:
            raise ValueError("Input image cannot be None.")

        image = np.asarray(image)

        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255).astype(np.uint8)

        height, width = image.shape[:2]

        # Simulate screenshot scaling
        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))

        screenshot = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_LINEAR
        )

        # Simulate JPEG compression
        success, encoded = cv2.imencode(
            ".jpg",
            screenshot,
            [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
        )

        if not success:
            raise RuntimeError(
                "Screenshot JPEG encoding failed."
            )

        result = cv2.imdecode(
            encoded,
            cv2.IMREAD_COLOR
        )

        if result is None:
            raise RuntimeError(
                "Screenshot decoding failed."
            )

        return result


    # =================================================
    # PSNR CALCULATION
    # =================================================

    def simulate_gaussian_blur(self, image, sigma=1.0):
        img = image if isinstance(image, Image.Image) else Image.fromarray(image)
        return img.filter(ImageFilter.GaussianBlur(radius=float(sigma)))

    def simulate_scanner_noise(self, image, mean=0.0, std=5.0):
        img = image if isinstance(image, Image.Image) else Image.fromarray(image)
        arr = np.array(img).astype(np.float32)
        rng = np.random.default_rng(42)
        noise = rng.normal(mean, std, arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(arr)

    def _calculate_psnr(self, original, processed):
        """
        Calculate Peak Signal-to-Noise Ratio (PSNR).

        Higher PSNR means the processed image
        is more similar to the original image.
        """

        if original is None or processed is None:
            raise ValueError(
                "Images cannot be None."
            )

        original = np.asarray(original)
        processed = np.asarray(processed)

        # Make dimensions equal
        if original.shape != processed.shape:
            processed = cv2.resize(
                processed,
                (original.shape[1], original.shape[0])
            )

        # Convert to float
        original = original.astype(np.float64)
        processed = processed.astype(np.float64)

        # Mean Squared Error
        mse = np.mean(
            (original - processed) ** 2
        )

        # Identical images
        if mse == 0:
            return float("inf")

        # Maximum pixel value
        max_pixel = 255.0

        # PSNR formula
        psnr = 10 * np.log10(
            (max_pixel ** 2) / mse
        )

        return float(psnr)


    # =================================================
    # SSIM CALCULATION
    # =================================================

    def _calculate_ssim(self, original, processed):
        """
        Calculate Structural Similarity Index (SSIM).

        SSIM ranges approximately from 0 to 1.
        A value closer to 1 means higher similarity.
        """

        if original is None or processed is None:
            raise ValueError(
                "Images cannot be None."
            )

        original = np.asarray(original)
        processed = np.asarray(processed)

        # Make dimensions equal
        if original.shape != processed.shape:
            processed = cv2.resize(
                processed,
                (original.shape[1], original.shape[0])
            )

        # Convert images to grayscale
        if len(original.shape) == 3:
            original_gray = cv2.cvtColor(
                original,
                cv2.COLOR_BGR2GRAY
            )
        else:
            original_gray = original

        if len(processed.shape) == 3:
            processed_gray = cv2.cvtColor(
                processed,
                cv2.COLOR_BGR2GRAY
            )
        else:
            processed_gray = processed

        # Convert to float
        original_gray = original_gray.astype(
            np.float64
        )

        processed_gray = processed_gray.astype(
            np.float64
        )

        # Constants from standard SSIM
        L = 255.0
        C1 = (0.01 * L) ** 2
        C2 = (0.03 * L) ** 2

        # Local means
        mu_original = cv2.GaussianBlur(
            original_gray,
            (11, 11),
            1.5
        )

        mu_processed = cv2.GaussianBlur(
            processed_gray,
            (11, 11),
            1.5
        )

        # Squared means
        mu_original_sq = mu_original ** 2
        mu_processed_sq = mu_processed ** 2

        # Mean product
        mu_product = (
            mu_original * mu_processed
        )

        # Local variances
        sigma_original_sq = (
            cv2.GaussianBlur(
                original_gray ** 2,
                (11, 11),
                1.5
            )
            - mu_original_sq
        )

        sigma_processed_sq = (
            cv2.GaussianBlur(
                processed_gray ** 2,
                (11, 11),
                1.5
            )
            - mu_processed_sq
        )

        # Local covariance
        sigma_original_processed = (
            cv2.GaussianBlur(
                original_gray * processed_gray,
                (11, 11),
                1.5
            )
            - mu_product
        )

        # SSIM formula
        numerator = (
            (2 * mu_product + C1)
            *
            (2 * sigma_original_processed + C2)
        )

        denominator = (
            (mu_original_sq + mu_processed_sq + C1)
            *
            (sigma_original_sq + sigma_processed_sq + C2)
        )

        ssim_map = numerator / (
            denominator + 1e-10
        )

        return float(np.mean(ssim_map))


    # =================================================
    # ROBUSTNESS TESTING
    # =================================================

    def test_robustness(self, image):
        """
        Run all required robustness tests.

        Tests:
            - Print-scan 150 DPI
            - Print-scan 300 DPI
            - JPEG quality 50
            - JPEG quality 30
            - JPEG quality 10

        Calculates:
            - PSNR
            - SSIM
        """

        if image is None:
            raise ValueError(
                "Input image cannot be None."
            )

        results = {}

        # -----------------------------------------
        # 150 DPI
        # -----------------------------------------

        result = self.simulate_print_scan(
            image,
            dpi=150,
            jpeg_quality=95
        )

        results["print_scan_150dpi"] = {
            "image": result,
            "psnr": self._calculate_psnr(
                image,
                result
            ),
            "ssim": self._calculate_ssim(
                image,
                result
            )
        }

        # -----------------------------------------
        # 300 DPI
        # -----------------------------------------

        result = self.simulate_print_scan(
            image,
            dpi=300,
            jpeg_quality=95
        )

        results["print_scan_300dpi"] = {
            "image": result,
            "psnr": self._calculate_psnr(
                image,
                result
            ),
            "ssim": self._calculate_ssim(
                image,
                result
            )
        }

        # -----------------------------------------
        # JPEG QUALITY 50
        # -----------------------------------------

        result = self.simulate_print_scan(
            image,
            dpi=300,
            jpeg_quality=50
        )

        results["jpeg_quality_50"] = {
            "image": result,
            "psnr": self._calculate_psnr(
                image,
                result
            ),
            "ssim": self._calculate_ssim(
                image,
                result
            )
        }

        # -----------------------------------------
        # JPEG QUALITY 30
        # -----------------------------------------

        result = self.simulate_print_scan(
            image,
            dpi=300,
            jpeg_quality=30
        )

        results["jpeg_quality_30"] = {
            "image": result,
            "psnr": self._calculate_psnr(
                image,
                result
            ),
            "ssim": self._calculate_ssim(
                image,
                result
            )
        }

        # -----------------------------------------
        # JPEG QUALITY 10
        # -----------------------------------------

        result = self.simulate_print_scan(
            image,
            dpi=300,
            jpeg_quality=10
        )

        results["jpeg_quality_10"] = {
            "image": result,
            "psnr": self._calculate_psnr(
                image,
                result
            ),
            "ssim": self._calculate_ssim(
                image,
                result
            )
        }

        # -----------------------------------------
        # SCREENSHOT RECOMPRESSION
        # -----------------------------------------

        result = self.simulate_screenshot(
            image,
            jpeg_quality=85
        )

        results["screenshot_recompression"] = {
            "image": result,
            "psnr": self._calculate_psnr(image, result),
            "ssim": self._calculate_ssim(image, result)
        }

        # -----------------------------------------
        # GAUSSIAN BLUR 0.5
        # -----------------------------------------

        result = self.simulate_gaussian_blur(
            image,
            sigma=0.5
        )

        results["gaussian_blur_sigma_0.5"] = {
            "image": result,
            "psnr": self._calculate_psnr(image, result),
            "ssim": self._calculate_ssim(image, result)
        }

        # -----------------------------------------
        # GAUSSIAN BLUR 1.0
        # -----------------------------------------

        result = self.simulate_gaussian_blur(
            image,
            sigma=1.0
        )

        results["gaussian_blur_sigma_1.0"] = {
            "image": result,
            "psnr": self._calculate_psnr(image, result),
            "ssim": self._calculate_ssim(image, result)
        }

        # -----------------------------------------
        # GAUSSIAN BLUR 1.5
        # -----------------------------------------

        result = self.simulate_gaussian_blur(
            image,
            sigma=1.5
        )

        results["gaussian_blur_sigma_1.5"] = {
            "image": result,
            "psnr": self._calculate_psnr(image, result),
            "ssim": self._calculate_ssim(image, result)
        }

        # -----------------------------------------
        # SCANNER NOISE
        # -----------------------------------------

        result = self.simulate_scanner_noise(
            image,
            mean=0.0,
            std=5.0
        )

        results["scanner_noise"] = {
            "image": result,
            "psnr": self._calculate_psnr(image, result),
            "ssim": self._calculate_ssim(image, result)
        }

        return results


# =================================================
# TESTING
# =================================================

if __name__ == "__main__":

    print("PrintScanSimulator loaded successfully!")

    simulator = PrintScanSimulator()

    # Create test image
    test_image = np.ones(
        (500, 500, 3),
        dtype=np.uint8
    ) * 255

    cv2.putText(
        test_image,
        "SIH WATERMARK TEST",
        (60, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2
    )

    # -----------------------------------------
    # Basic print-scan test
    # -----------------------------------------

    print("\nTesting print-scan simulation...")

    scanned_image = simulator.simulate_print_scan(
        test_image,
        dpi=300,
        jpeg_quality=95
    )

    cv2.imwrite(
        "test_print_scan.jpg",
        scanned_image
    )

    print("Print-scan simulation: PASS")

    # -----------------------------------------
    # Screenshot test
    # -----------------------------------------

    print("\nTesting screenshot simulation...")

    screenshot_image = simulator.simulate_screenshot(
        test_image,
        scale=1.0,
        jpeg_quality=90
    )

    cv2.imwrite(
        "test_screenshot.jpg",
        screenshot_image
    )

    print("Screenshot simulation: PASS")

    # -----------------------------------------
    # Robustness tests
    # -----------------------------------------

    print("\n========== ROBUSTNESS TESTS ==========")

    robustness_results = simulator.test_robustness(
        test_image
    )

    for test_name, data in robustness_results.items():

        filename = test_name + ".jpg"

        output_image = data["image"]
        if isinstance(output_image, Image.Image):
            output_image = cv2.cvtColor(
                np.array(output_image),
                cv2.COLOR_RGB2BGR
            )

        cv2.imwrite(
            filename,
            output_image
        )

        print(
            f"{test_name}: PASS"
        )

        print(
            f"    PSNR : {data['psnr']:.2f} dB"
        )

        print(
            f"    SSIM : {data['ssim']:.4f}"
        )

    print("\n======================================")
    print("ALL ROBUSTNESS TESTS COMPLETED")
    print("PSNR + SSIM CALCULATION COMPLETED")
    print("======================================")