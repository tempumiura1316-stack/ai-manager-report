import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI報告書メーカー", page_icon="🧠")
st.title("🧠 AI報告書メーカー（テスト版）")
st.write("こんにちは！これは初期テスト用のStreamlitアプリです。")

text = st.text_area("日報を入力してください")
if st.button("週報を作成"):
    st.success("ここにAIの出力が表示されます（後で実装）")
    st.write(text)
    st.write("文字数:", len(text))
    st.write([m.id for m in client.models.list().data])
