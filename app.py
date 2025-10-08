import streamlit as st
import io
from openai import OpenAI
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI報告書メーカー", page_icon="🧠")
st.title("🧠 AI報告書メーカー")
st.write("こんにちは！これは週報作成用のアプリです。")

text = st.text_area("日報を入力してください")
if st.button("週報を作成"):
    st.success("ここにAIの出力が表示されます")
    md = client.chat.completions.create(model="gpt-4o-mini",
    messages=[{"role":"user","content": f"以下は日報です。週報(見出し/実績/課題/来週のPlan)を日本語でMarkdown出力してください。\n\n{text}"}]
).choices[0].message.content
    st.markdown(md)
    
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(name="NormalJP", parent=styles["Normal"], fontName="HeiseiMin-W3", fontSize=11, leading=16)
    
    story = []
    lines = md.splitlines()
    for line in lines:
        pass
