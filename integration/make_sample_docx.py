"""Creates contract.docx (a formatted Word file with enough text for the watermark).
Run:  python make_sample_docx.py
"""
from tests.api.test_docx import real_docx_bytes

if __name__ == "__main__":
    with open("contract.docx", "wb") as f:
        f.write(real_docx_bytes())
    print("Created contract.docx")
