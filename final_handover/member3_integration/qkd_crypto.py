import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class SimulatedQKD:
    """
    Simulated Quantum Key Distribution (QKD).

    This is NOT real quantum hardware.

    It simulates the result of a QKD process by
    generating a cryptographically secure 256-bit key.
    """

    def __init__(self, key_size=32):
        """
        key_size = 32 bytes = 256 bits
        """
        self.key_size = key_size

    def generate_key(self):
        """
        Generate a random 256-bit secret key.

        os.urandom() provides cryptographically
        secure random bytes.
        """

        return os.urandom(
            self.key_size
        )

    def generate_key_id(self, key):
        """
        Create a SHA-256 identifier for the key.

        The actual secret key is never used as
        the identifier.
        """

        return hashlib.sha256(
            key
        ).hexdigest()


class WatermarkCrypto:
    """
    AES-256-GCM encryption for watermark transmission.

    AES-GCM provides:

        1. Confidentiality
        2. Integrity
        3. Authentication
    """

    def __init__(self, key):
        """
        key must be exactly 32 bytes
        for AES-256.
        """

        if not isinstance(
            key,
            bytes
        ):
            raise TypeError(
                "Key must be bytes."
            )

        if len(key) != 32:
            raise ValueError(
                "AES-256 requires "
                "a 32-byte key."
            )

        self.key = key

        self.aes = AESGCM(
            self.key
        )

    # ============================================================
    # ENCRYPT
    # ============================================================

    def encrypt(
        self,
        plaintext
    ):
        """
        Encrypt watermark data using AES-256-GCM.

        Returns:
            nonce
            ciphertext
        """

        if isinstance(
            plaintext,
            str
        ):

            plaintext = (
                plaintext.encode(
                    "utf-8"
                )
            )

        if not isinstance(
            plaintext,
            bytes
        ):

            raise TypeError(
                "Plaintext must be "
                "bytes or string."
            )

        # GCM requires a unique nonce
        # for every encryption operation.

        nonce = os.urandom(
            12
        )

        ciphertext = self.aes.encrypt(
            nonce,
            plaintext,
            None
        )

        return {
            "nonce": nonce,
            "ciphertext": ciphertext
        }

    # ============================================================
    # DECRYPT
    # ============================================================

    def decrypt(
        self,
        nonce,
        ciphertext
    ):
        """
        Decrypt and authenticate AES-GCM data.
        """

        if not isinstance(
            nonce,
            bytes
        ):

            raise TypeError(
                "Nonce must be bytes."
            )

        if not isinstance(
            ciphertext,
            bytes
        ):

            raise TypeError(
                "Ciphertext must be bytes."
            )

        plaintext = self.aes.decrypt(
            nonce,
            ciphertext,
            None
        )

        return plaintext


# ================================================================
# CONVENIENCE FUNCTIONS
# ================================================================

def generate_qkd_key():
    """
    Generate a simulated 256-bit QKD key.
    """

    qkd = SimulatedQKD()

    return qkd.generate_key()


def encrypt_watermark(
    watermark_id,
    key
):
    """
    Encrypt a watermark ID using AES-256-GCM.
    """

    crypto = WatermarkCrypto(
        key
    )

    return crypto.encrypt(
        watermark_id
    )


def decrypt_watermark(
    encrypted_data,
    key
):
    """
    Decrypt an AES-256-GCM encrypted
    watermark ID.
    """

    crypto = WatermarkCrypto(
        key
    )

    plaintext = crypto.decrypt(
        encrypted_data["nonce"],
        encrypted_data["ciphertext"]
    )

    return plaintext.decode(
        "utf-8"
    )
