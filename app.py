import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

st.title("Leitor de PDF com IA")

uploaded_file = st.file_uploader("Envie seu PDF", type="pdf")

pergunta = st.text_area("O que você quer encontrar no PDF?")

def extrair_texto_pdf(file):
    texto_total = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")

    for i, page in enumerate(doc):
        texto = page.get_text()

        if texto.strip():
            texto_total += f"\n--- Página {i+1} ---\n{texto}"
        else:
            # OCR
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            texto_ocr = pytesseract.image_to_string(img)
            texto_total += f"\n--- Página {i+1} (OCR) ---\n{texto_ocr}"

    return texto_total

if st.button("Analisar PDF"):
    if uploaded_file and pergunta:
        with st.spinner("Processando..."):
            texto = extrair_texto_pdf(uploaded_file)

            st.subheader("Texto extraído:")
            st.write(texto[:5000])  # mostra só parte pra não travar

            st.subheader("Pergunta:")
            st.write(pergunta)

            st.success("PDF processado com sucesso!")
    else:
        st.error("Envie um PDF e preencha a pergunta.")
