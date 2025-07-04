# PDF Translator

A simple utility to convert and translate PDF or DOCX files using OCR and various document libraries.

## Installation

Install the required dependencies:

```bash
pip install \
  fitz==0.0.1.dev2 \
  pymupdf>=1.21.1 \
  pdf2docx>=0.5.6 \
  python-docx>=0.8.11 \
  pytesseract>=0.3.10 \
  Pillow>=9.5.0 \
  googletrans==4.0.0-rc1 \
  docx2pdf>=0.1.7
```

## Scripts

* `clean.py` — Script for cleaning up files or directories.
* `convertdoc-ocr.py` — Convert and translate scanned DOCX or PDF files using OCR.
* `convertdoc-ori.py` — Convert original digital DOCX or PDF files without OCR.

## Requirements

* Python 3.x
* Tesseract OCR installed on system (for OCR functionality)
* Ghostscript (if required by pdf2docx)

## Notes

* This project does not include the `translatepdf+docx-ocr.py` file as it has been removed.
* Make sure Tesseract is correctly installed and configured in your system PATH.

## License

This project is licensed under the MIT License.
