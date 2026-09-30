from io import BytesIO
import struct
import zlib

from docx import Document
from docx.oxml import OxmlElement


class DOCXWatermarker:
    """
    Prototype DOCX forensic watermarking system.

    Watermark information:
        - recipient ID
        - timestamp

    Encoding method:
        Character spacing

        bit 0 -> normal spacing
        bit 1 -> increased spacing
    """

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    MAGIC = b"VSM1"
    VERSION = 1

    NORMAL_SPACING = 0
    WATERMARK_SPACING = 10

    MAX_RECIPIENT_LENGTH = 64

    # ---------------------------------------------------------
    # Generate watermark bits
    # ---------------------------------------------------------

    def _generate_watermark_bits(
        self,
        recipient_id,
        timestamp
    ):
        """
        Convert recipient ID + timestamp into binary bits.
        """

        recipient_bytes = recipient_id.encode("utf-8")

        if len(recipient_bytes) > self.MAX_RECIPIENT_LENGTH:
            raise ValueError(
                "Recipient ID is too long."
            )

        # Create payload
        payload = (
            self.MAGIC
            + struct.pack(">B", self.VERSION)
            + struct.pack(">Q", timestamp)
            + struct.pack(">B", len(recipient_bytes))
            + recipient_bytes
        )

        # Calculate CRC
        crc = zlib.crc32(payload)

        # Add CRC to payload
        payload += struct.pack(">I", crc)

        # Convert bytes to bits
        bits = []

        for byte in payload:

            for position in range(7, -1, -1):

                bit = (byte >> position) & 1

                bits.append(bit)

        return bits

    # ---------------------------------------------------------
    # Set character spacing
    # ---------------------------------------------------------

    def _set_run_spacing(
        self,
        run,
        bit
    ):
        """
        Set character spacing for a run.

        bit 0 -> normal
        bit 1 -> watermark spacing
        """

        run_properties = run._r.get_or_add_rPr()

        spacing = OxmlElement("w:spacing")

        spacing.set(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val",
            str(
                self.WATERMARK_SPACING
                if bit == 1
                else self.NORMAL_SPACING
            )
        )

        run_properties.append(spacing)

    # ---------------------------------------------------------
    # Modify document
    # ---------------------------------------------------------

    def _modify_character_spacing(
        self,
        document,
        watermark_bits
    ):
        """
        Embed watermark bits into document characters.

        One character/run carries one bit.
        """

        bit_index = 0

        for paragraph in document.paragraphs:

            # Get original text
            original_text = paragraph.text

            if not original_text:
                continue

            # Remove existing runs
            for run in paragraph.runs:
                run._element.getparent().remove(
                    run._element
                )

            # Create one run for each character
            for character in original_text:

                run = paragraph.add_run(character)

                # If all watermark bits are embedded,
                # leave remaining characters untouched.
                if bit_index < len(watermark_bits):

                    bit = watermark_bits[bit_index]

                    self._set_run_spacing(
                        run,
                        bit
                    )

                    bit_index += 1

        # Check capacity
        if bit_index < len(watermark_bits):

            raise ValueError(
                f"Document does not have enough characters "
                f"for watermark. Required: "
                f"{len(watermark_bits)}, "
                f"available: {bit_index}"
            )

    # ---------------------------------------------------------
    # Embed watermark
    # ---------------------------------------------------------

    def embed_watermark(
        self,
        docx_bytes,
        recipient_id,
        timestamp
    ):
        """
        Embed watermark into DOCX bytes.

        Returns:
            Watermarked DOCX as bytes.
        """

        # Generate watermark
        watermark_bits = self._generate_watermark_bits(
            recipient_id,
            timestamp
        )

        # Load DOCX
        document = Document(
            BytesIO(docx_bytes)
        )

        # Modify document
        self._modify_character_spacing(
            document,
            watermark_bits
        )

        # Save to memory
        output = BytesIO()

        document.save(output)

        return output.getvalue()


# -------------------------------------------------------------
# Simple test
# -------------------------------------------------------------
    def _extract_spacing_bits(self, document, required_bits):
        bits = []

        for paragraph in document.paragraphs:
            for run in paragraph.runs:
                for character in run.text:
                    if len(bits) >= required_bits:
                        return bits

                    spacing_element = run._r.rPr
                    if spacing_element is not None:
                        spacing = spacing_element.find(
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}spacing"
                        )
                    else:
                        spacing = None

                    if spacing is not None:
                        value = spacing.get(
                            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"
                        )
                        bits.append(
                            1 if value == str(self.WATERMARK_SPACING) else 0
                        )
                    else:
                        bits.append(0)

        return bits

    def _bits_to_bytes(self, bits):
        data = bytearray()

        for index in range(0, len(bits) - 7, 8):
            byte_value = 0
            for bit in bits[index:index + 8]:
                byte_value = (byte_value << 1) | bit
            data.append(byte_value)

        return bytes(data)

    def extract_watermark(self, docx_bytes):
        document = Document(BytesIO(docx_bytes))

        # Header size: magic + version + timestamp + recipient length
        header_bits = self._extract_spacing_bits(document, 14 * 8)

        if len(header_bits) < 14 * 8:
            raise ValueError("Not enough text to extract watermark.")

        header = self._bits_to_bytes(header_bits)
        if header[:4] != self.MAGIC:
            raise ValueError("Watermark signature not found.")

        version = header[4]
        timestamp = struct.unpack(">Q", header[5:13])[0]
        recipient_length = header[13]

        total_bytes = 14 + recipient_length + 4
        all_bits = self._extract_spacing_bits(document, total_bytes * 8)
        payload = self._bits_to_bytes(all_bits)

        stored_crc = struct.unpack(">I", payload[-4:])[0]
        actual_crc = zlib.crc32(payload[:-4])

        if stored_crc != actual_crc:
            raise ValueError("Watermark checksum failed.")

        recipient_bytes = payload[14:14 + recipient_length]
        recipient_id = recipient_bytes.decode("utf-8")

        return {
            "recipient_id": recipient_id,
            "timestamp": timestamp,
            "version": version,
            "checksum_valid": True,
        }
if __name__ == "__main__":

    print("DOCXWatermarker loaded successfully!")

    watermarker = DOCXWatermarker()

    bits = watermarker._generate_watermark_bits(
        "RECIPIENT_001",
        1759165200
    )

    print("Watermark bits:", len(bits))
    print("First 32 bits:", bits[:32])