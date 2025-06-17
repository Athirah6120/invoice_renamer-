# --- app.py ---
import streamlit as st
import os
import shutil
from pdf_utils import extract_invoice_number, rename_pdf_file

st.set_page_config(page_title="Invoice Renamer", layout="centered")
st.title("📎 PDF Invoice Renamer")
st.write("Upload PDF invoices and rename them based on invoice numbers found inside the files.")

# File uploader
uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

# Processing logic
if uploaded_files:
    temp_dir = "temp_uploads"
    output_dir = "renamed"

    shutil.rmtree(temp_dir, ignore_errors=True)
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)

    renamed_files = []

    for file in uploaded_files:
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.read())

        invoice_no = extract_invoice_number(temp_path)
        if invoice_no:
            renamed_path = rename_pdf_file(temp_path, invoice_no, output_dir)
            renamed_files.append(os.path.basename(renamed_path))
        else:
            st.warning(f"No invoice number found in {file.name}")

    if renamed_files:
        st.success("Renaming complete!")
        for name in renamed_files:
            st.write(f"✅ {name}")

        shutil.make_archive("renamed_invoices", 'zip', output_dir)
        with open("renamed_invoices.zip", "rb") as f:
            st.download_button("⬇️ Download Renamed PDFs (ZIP)", f, "renamed_invoices.zip")


# --- pdf_utils.py ---
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


# --- requirements.txt ---
streamlit
PyMuPDF
