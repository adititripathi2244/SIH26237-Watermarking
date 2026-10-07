# Member 2 → Member 3 Integration Guide

## 1. Purpose

This package contains the forensic watermarking and cryptographic components developed by Member 2 for SIH26237.

The components currently included are:

- `pdf_watermarker.py` — invisible watermarking for PDF documents
- `image_watermarker.py` — invisible watermarking for images
- `qkd_crypto.py` — simulated QKD key generation + AES-256-GCM encryption
- `watermark_cnn.py` — CNN architecture for watermark detection

The main value passed to the provenance/blockchain layer is the
`watermark_id`.

---

# 2. Overall Integration Flow

```text
Recipient / ZKP information
          |
          v
    Generate watermark_id
          |
          v
   Embed watermark into
      PDF or Image
          |
          v
   Encrypt / distribute
       document
          |
          v
     Decryption event
          |
          v
    Extract watermark
          |
          v
      watermark_id
          |
          v
 Member 3 provenance /
 blockchain component
