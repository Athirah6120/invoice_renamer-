import streamlit as st
import os
import shutil
from pdf_utils import extract_invoice_number, rename_pdf_file

st.set_page_config(page_title="Invoice Renamer", layout="centered")
st.title("📎 PDF Invoice Renamer")
st.write("Upload PDF invoices and rename them based on invoice numbers found inside the files.")

# ✅ File uploader
uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

# ✅ Logic after upload
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
