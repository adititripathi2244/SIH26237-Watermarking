# SIH26237: DOCX watermark integration (Member 3 module -> backend)

No existing watermarking file is modified. pdf_watermarker.py and
image_watermarker.py in the backend are byte-identical to the handover copies:

917de771fc5505130ddacd2d02f511deb704abf8589aa14ed3b325dcecf55b95  pdf_watermarker.py
c0b61d0e3224a1416639df9f3b356fa4809c17fb1534c67f28988cff9ec8e83b  image_watermarker.py

## Files
- src/provenance/docx_watermarker.py : NEW. DOCX watermark adapter, same bit format as Member 3's DOCXWatermarker.
- src/provenance/apply.py            : CHANGED. Two ".docx" branches added (embed and read), nothing else.
- tests/api/test_docx.py             : NEW. 7 tests.
- make_sample_docx.py                : NEW. Creates contract.docx for demos.

## Why an adapter
1. Privacy: the embedded ID is SHA-256(ZKP proof), 64 hex chars (same rule as PDF/PNG). No recipient identity reaches the watermark code.
2. Formatting: run properties (bold, italic, font, size) are copied onto the one-character runs, only the first ~656 plain-text characters are touched, inline pictures are kept.
3. Schema order: w:spacing is inserted at its correct position in w:rPr.

## Behaviour
- .docx with enough body text (about 656 characters): spacing mark, read back and checked before release.
- .docx too short or not parseable: falls back to the existing metadata mark. A copy is never released unmarked.
- PDF, PNG, JPEG paths are unchanged.

## Apply
1. Copy the files to the same relative paths in the backend.
2. pip install "python-docx>=1.1.0" (and add it to requirements.txt).
3. Restart the server.

## Test
python -m pytest tests/api/test_docx.py -v
python -m pytest tests -q
python make_sample_docx.py
.\flow_test.ps1 -File contract.docx

Our results: test_docx.py 7 passed; tests/api 34 passed; flow_test.ps1 10/10 PASS for PNG, PDF and DOCX; tests/provenance/test_apply.py 11 passed.

## Limits
- Survives copying, forwarding and re-saving as .docx. Does NOT survive print-scan or conversion to PDF.
- Only body paragraphs carry bits (not tables, headers, hyperlinks).
- CRC32 detects corruption, not forgery. Attribution rests on the signed ledger record and the ZKP proof.
