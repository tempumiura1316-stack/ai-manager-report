import os
import io
import pandas as pd
import streamlit as st

# --- openai が未インストールでも自己解決する ---
try:
    from openai import OpenAI
except ModuleNotFoundError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai==1.51.0"])
    from openai import OpenAI
# ---------------------------------------------------


st.set_page_config(page_title="AI報告書メーカー", page_icon="🧠", layout="centered")
st.title("🧠 AI報告書メーカー（シンプル版）")
st.caption("日報を貼るだけ → 週報＋改善提案を自動生成")

# ==== OpenAI クライアント ====
api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", None))
if not api_key:
    st.error("OPENAI_API_KEY が未設定です。StreamlitのSecretsに登録してください。")
client = OpenAI(api_key=api_key) if api_key else None

# ==== 入力UI ====
tab_text, tab_csv = st.tabs(["テキスト入力", "CSVアップロード（任意）"])

raw_text = ""
with tab_text:
    raw_text = st.text_area(
        "今日/今週の日報・メモ（自由形式OK）",
        height=220,
        placeholder="例）\n・商談3件（A社：見積送付／B社：PoC提案／C社：競合比較）\n・問い合わせ対応7件、CS対応2件\n・KPI：新規リード12件（先週+3）..."
    )

with tab_csv:
    up = st.file_uploader("CSV/Excelをアップロード（UTF-8推奨）", type=["csv", "xlsx"])
    if up:
        try:
            df = pd.read_excel(up) if up.name.endswith(".xlsx") else pd.read_csv(up)
            st.write("プレビュー（上位50行）"); st.dataframe(df.head(50))
            buf = io.StringIO(); df.to_csv(buf, index=False)
            raw_text = (raw_text or "") + "\n\n[CSV抜粋]\n" + buf.getvalue()[:20000]
        except Exception as e:
            st.error(f"読み込みエラー：{e}")

col1, col2 = st.columns([1,1])
with col1:
    gen = st.button("🚀 週報を作成")
with col2:
    clear = st.button("入力をクリア")

if clear:
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# ==== 生成処理 ====
PROMPT = """あなたは有能な営業マネージャーです。以下の原稿（日報やメモ）から、
上司に伝わりやすい「週報」を日本語Markdownで作成してください。

# 出力要件
- 見出し：要約 / 数値・成果 / 課題 / 改善提案 / 来週のアクション
- 箇条書きは簡潔（1項目MAX2行）
- 事実ベースで、前向きなトーン
- 最後に「上司への確認事項」を1〜3点で

# 入力原稿
{raw}
"""

if gen:
    if not client:
        st.stop()
    if not raw_text or not raw_text.strip():
        st.warning("入力が空です。テキストを貼るかCSVをアップロードしてください。")
        st.stop()

    with st.spinner("AIが週報を作成中..."):
        try:
            prompt = PROMPT.format(raw=raw_text[:20000])
            res = client.chat.completions.create(
                model="gpt-4o-mini",  # 速さ/コスト重視
                temperature=0.4,
                messages=[{"role": "user", "content": prompt}],
            )
            md = res.choices[0].message.content
            st.session_state["md"] = md
        except Exception as e:
            st.error(f"生成エラー：{e}")

# ==== 結果表示 ====
if "md" in st.session_state:
    st.markdown("---")
    st.subheader("📄 生成結果（Markdown）")
    st.markdown(st.session_state["md"])
    st.download_button(
        "⬇️ Markdownを保存",
        data=st.session_state["md"].encode("utf-8"),
        file_name="weekly_report.md",
        mime="text/markdown"
    )

st.markdown("---")
with st.expander("注意・今後の予定"):
    st.write("- 入力データはサーバに保存しません（セッション内のみ）\n- 機密情報の投入は避けてください\n- 予定：Slack送信ボタン、テンプレ切り替え、履歴保存など")
