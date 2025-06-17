import streamlit as st
import os, shutil
from pdf_utils import extract_invoice_number, rename_pdf_file

st.set_page_config(page_title="Invoice Renamer", layout="centered")
st.title("📎 PDF Invoice Renamer")
st.write("Upload PDF invoices and rename them based on invoice numbers found inside the files.")
...
