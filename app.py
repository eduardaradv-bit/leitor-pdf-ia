import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
from openai import OpenAI

# Configuração da página
st.set_page_config(page_title="Leitor de PDF com IA")

st.title("Leitor de PDF com IA")

# Upload do PDF
uploaded_file = st.file_uploader("Envie seu PDF", type="pdf")

# Pergunta
pergunta = st.text_area("O que você quer encontrar no PDF?")

# Função para extrair texto
def extrair_texto_pdf(file):
    texto_total = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")

    for i, page in enumerate(doc):
        texto = page.get_text()

        if texto.strip():
            texto_total += f"\n--- Página {i+1} ---\n{texto}"
        else:
            # OCR se não tiver texto
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            texto_ocr = pytesseract.image_to_string(img)
            texto_total += f"\n--- Página {i+1} (OCR) ---\n{texto_ocr}"

    return texto_total

# Botão de análise
if st.button("Analisar PDF com IA"):
    if uploaded_file and pergunta:

        texto = extrair_texto_pdf(uploaded_file)

        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é uma advogada especialista em execução bancária. Seja objetiva e direta."
                },
                {
                    "role": "user",
                    "content": f"""
Analise o texto abaixo e responda a pergunta de forma objetiva:

PERGUNTA:
{pergunta}

TEXTO:
{texto[:15000]}
"""
                }
            ]
        )

        st.subheader("Resposta:")
        st.write(resposta.choices[0].message.content)

    else:
        st.warning("Envie um PDF e escreva a pergunta.")
