import fitz  # PyMuPDF
from pdf2docx import Converter
from docx import Document
from docx.shared import Pt, RGBColor
import pytesseract
from PIL import Image
import io
import os
from googletrans import Translator
from docx2pdf import convert
import time

MAX_WORDS = 4500

def page_has_text(page):
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b["type"] == 0 and b["lines"]:
            return True
    return False

def extract_ocr_text_from_page(page):
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang='eng+ind')
    return text.strip()

def extract_text_per_page(pdf_path):
    print("📄 Mengekstrak teks per halaman dari PDF...")
    doc = fitz.open(pdf_path)
    pages_text = []

    for i, page in enumerate(doc):
        print(f"📃 Halaman {i+1}")
        if page_has_text(page):
            text = page.get_text()
        else:
            print("🧠 OCR karena tidak ada teks...")
            text = extract_ocr_text_from_page(page)

        pages_text.append(text.strip())

    return pages_text

def translate_in_chunks(text_list, max_words=MAX_WORDS):
    print("🌍 Menerjemahkan ke Bahasa Indonesia...")
    translator = Translator()
    translated_list = []
    buffer = ""
    chunk_map = []
    word_count = 0

    for i, text in enumerate(text_list):
        words = text.split()
        if word_count + len(words) > max_words:
            translated_chunk = safe_translate(translator, buffer)
            translated_list.extend(translated_chunk)
            buffer, chunk_map, word_count = "", [], 0

        buffer += text + "\n"
        word_count += len(words)

    if buffer:
        translated_chunk = safe_translate(translator, buffer)
        translated_list.extend(translated_chunk)

    return translated_list

def safe_translate(translator, text):
    try:
        translated = translator.translate(text, src='auto', dest='id')
        return translated.text.split('\n')
    except Exception as e:
        print(f"❌ Error saat translate: {e}")
        time.sleep(5)
        return text.split('\n')  # fallback

def save_to_docx(translated_pages, output_docx):
    print("📦 Menyusun dokumen .docx hasil translate...")
    doc = Document()

    for i, page_text in enumerate(translated_pages):
        p = doc.add_paragraph(page_text)
        for run in p.runs:
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0, 0, 0)
        if i < len(translated_pages) - 1:
            doc.add_page_break()

    doc.save(output_docx)
    print(f"✅ Disimpan sebagai: {output_docx}")

def export_to_pdf(input_docx, output_pdf):
    print("📤 Mengekspor ke PDF...")
    convert(input_docx, output_pdf)
    print(f"✅ PDF disimpan: {output_pdf}")

def full_translate_pdf_to_pdf(pdf_path):
    translated_docx = "translated_final.docx"
    translated_pdf = "translated_final.pdf"

    pages_text = extract_text_per_page(pdf_path)
    translated_pages = translate_in_chunks(pages_text)
    save_to_docx(translated_pages, translated_docx)
    export_to_pdf(translated_docx, translated_pdf)

    print("🎉 Semua selesai!")

# Jalankan
if __name__ == "__main__":
    full_translate_pdf_to_pdf("input.pdf")
