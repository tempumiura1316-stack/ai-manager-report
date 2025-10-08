import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI報告書メーカー", page_icon="🧠")
st.title("🧠 AI報告書メーカー（テスト版）")
st.write("こんにちは！これは初期テスト用のStreamlitアプリです。")

text = st.text_area("日報を入力してください")
if st.button("週報を作成"):
    st.success("ここにAIの出力が表示されます（後で実装）")
    st.markdown(client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content": f"以下は日報です。週報(見出し/実績/課題/来週のPlan)を日本語でMarkdown出力してください。\n\n{text}"}]).choices[0].message.content)
