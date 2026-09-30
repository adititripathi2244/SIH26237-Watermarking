# SIH Watermarking System

## 1. Project Overview

This project implements a document watermarking and robustness testing
system for the SIH problem statement:

"Cryptographic Attribution and Immutable Decryption Provenance for
Multi-Recipient Encrypted Document Distribution."

The system focuses on document-level watermarking, multi-format handling,
and robustness testing against common transformations such as compression,
print-scan simulation, and screenshot simulation.

---

## 2. Technologies Used

- Python 3.13
- python-docx
- OpenCV
- Pillow
- NumPy
- PyMuPDF
- Pandas

---

## 3. DOCX Watermarking

The DOCX watermarking module is implemented using character-spacing
modification.

The watermark contains:

- Magic identifier
- Version
- Timestamp
- Recipient ID
- CRC32 checksum

The watermark is converted into binary bits.

Each bit is represented through character spacing:

- Normal spacing = 0
- Modified spacing = 1

The system can embed and extract the watermark from DOCX documents.

### Main class

`DOCXWatermarker`

### Main functions

- `embed_watermark()`
- `extract_watermark()`
- `_generate_watermark_bits()`
- `_modify_character_spacing()`

---

## 4. Multi-Format Watermarking Interface

The `MultiFormatWatermarker` provides a unified interface for identifying
document formats.

Supported format detection includes:

- DOCX
- PDF
- Image

The interface automatically detects the input format and routes the
document to the appropriate processing logic.

---

## 5. Print-Scan Simulation

The `PrintScanSimulator` simulates the effects of printing and scanning.

The simulator supports:

- 150 DPI simulation
- 300 DPI simulation
- JPEG compression
- Screenshot simulation

The simulator is used to evaluate how much visual information changes
after common transformations.

---

## 6. JPEG Compression Tests

The following JPEG quality levels are tested:

- Quality 50
- Quality 30
- Quality 10

These tests represent increasing levels of compression.

---

## 7. Image Quality Metrics

Two image-quality metrics are calculated.

### PSNR

Peak Signal-to-Noise Ratio (PSNR) measures the difference between the
original and processed image.

Higher PSNR generally indicates less distortion.

### SSIM

Structural Similarity Index (SSIM) measures structural similarity between
the original and processed images.

Values closer to 1 indicate higher structural similarity.

---

## 8. Robustness Results

The following image robustness measurements were obtained:

| Test | PSNR (dB) | SSIM |
|---|---:|---:|
| Print-scan 150 DPI | 25.41 | 0.9783 |
| Print-scan 300 DPI | 56.85 | 0.9999 |
| JPEG Quality 50 | 40.10 | 0.9967 |
| JPEG Quality 30 | 37.22 | 0.9943 |
| JPEG Quality 10 | 32.77 | 0.9885 |

The complete metrics are also stored in:

`robustness_metrics.csv`

---

## 9. Testing

### DOCX Testing

Five DOCX documents were tested.

Result:

- Tests: 5
- Passed: 5
- Failed: 0
- Accuracy: 100%

### Phase 3 Test Suite

The Phase 3 test suite contains:

- 10 DOCX tests
- 5 image tests
- 5 PDF page tests

Result:

- Total tests: 20
- Passed: 20
- Failed: 0
- Basic test accuracy: 100%

---

## 10. Performance Testing

A 10-page PDF was rendered to evaluate processing speed.

Result:

- Pages processed: 10
- Processing time: approximately 0.06 seconds
- Target: less than 2 seconds

The speed target was successfully achieved in the test environment.

---

## 11. Combined Test Suite

A combined test runner executes the main testing modules.

The suite includes:

- DOCX accuracy test
- Image robustness test
- PDF robustness test
- Metrics generation
- 10-page PDF speed test

Latest result:

- Test modules: 5
- Passed: 5
- Failed: 0

Overall test suite status: PASSED

---

## 12. Project Files

Important project files include:

- `docx_watermarker.py`
- `multi_format_watermarker.py`
- `print_scan_simulator.py`
- `test_5_docx.py`
- `test_image_robustness.py`
- `test_pdf_robustness.py`
- `test_20_documents.py`
- `test_10page_speed.py`
- `generate_metrics_table.py`
- `test_suite.py`
- `robustness_metrics.csv`

---

## 13. Current Limitations

The current DOCX watermarking implementation is a prototype based on
character spacing.

Formatting normalization by document editors may affect the embedded
spacing information.

The current print-scan simulator operates on rendered images. Therefore,
the current implementation does not demonstrate end-to-end extraction of
the existing DOCX character-spacing watermark after physical printing,
scanning, or image rendering.

Additional watermark carriers would be required for a complete
print-scan-resistant watermarking pipeline.

---

## 14. Current Status

The current implementation successfully demonstrates:

- DOCX watermark embedding
- DOCX watermark extraction
- Recipient identification
- Timestamp storage
- CRC32 integrity verification
- Multi-format detection
- Print-scan simulation
- Screenshot simulation
- JPEG robustness testing
- PSNR calculation
- SSIM calculation
- Multi-document testing
- PDF performance testing
- Combined automated testing

Phase 3 testing and performance checkpoints have been completed.

Member 2 integration remains pending until the corresponding component
is ready.