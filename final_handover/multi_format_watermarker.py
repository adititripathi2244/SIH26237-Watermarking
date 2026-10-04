from pathlib import Path

from docx_watermarker import DOCXWatermarker


class MultiFormatWatermarker:

    def __init__(self):
        self.docx_watermarker = DOCXWatermarker()

    def _detect_format(self, filename):
        extension = Path(filename).suffix.lower()

        if extension == ".docx":
            return "docx"

        elif extension == ".pdf":
            return "pdf"

        elif extension in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
            return "image"

        else:
            raise ValueError(
                f"Unsupported file format: {extension}"
            )

    def watermark_document(
        self,
        file_bytes,
        filename,
        recipient_id,
        timestamp
    ):
        file_format = self._detect_format(filename)

        if file_format == "docx":
            return self.docx_watermarker.embed_watermark(
                file_bytes,
                recipient_id,
                timestamp
            )

        raise NotImplementedError(
            f"Watermarking for {file_format} is not implemented yet."
        )

    def extract_watermark(self, file_bytes, filename):
        file_format = self._detect_format(filename)

        if file_format == "docx":
            return self.docx_watermarker.extract_watermark(
                file_bytes
            )

        raise NotImplementedError(
            f"Extraction for {file_format} is not implemented yet."
        )


if __name__ == "__main__":
    watermarker = MultiFormatWatermarker()

    print("MultiFormatWatermarker loaded successfully!")

    print(
        "DOCX format:",
        watermarker._detect_format("sample.docx")
    )

    print(
        "PDF format:",
        watermarker._detect_format("sample.pdf")
    )

    print(
        "Image format:",
        watermarker._detect_format("sample.png")
    )