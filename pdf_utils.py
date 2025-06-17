import fitz  # PyMuPDF
import re
import os

def extract_invoice_number(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    # Look for numbers starting with 1248473 followed by a dash and more digits
    match = re.search(r"1248473-\d{2,}", text)
    return match.group(0).strip() if match else None

def rename_pdf_file(original_path, invoice_number, output_dir="renamed"):
    os.makedirs(output_dir, exist_ok=True)
    new_path = os.path.join(output_dir, f"{invoice_number}.pdf")
    os.rename(original_path, new_path)
    return new_path
