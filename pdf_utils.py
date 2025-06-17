import fitz  # PyMuPDF
import re
import os

def extract_invoice_number(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    # NEW: Match 'Invoice No' followed by whitespace and the number
    match = re.search(r"Invoice\s*No\.?\s+([0-9]{5,}-[0-9]{2,})", text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def rename_pdf_file(original_path, invoice_number, output_dir="renamed"):
    os.makedirs(output_dir, exist_ok=True)
    new_path = os.path.join(output_dir, f"{invoice_number}.pdf")
    os.rename(original_path, new_path)
    return new_path
