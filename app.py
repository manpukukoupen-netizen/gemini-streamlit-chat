import os
import streamlit as st
from google import genai

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("🤖 Gemini AI Chat App")

# APIキーの取得（Streamlit Secretsまたは環境変数から）
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("APIキーが設定されていません。StreamlitのSecretsに GEMINI_API_KEY を設定してください。")
    st.stop()

# Clientの初期化
client = genai.Client(api_key=api_key)

# セッション状態（会話履歴）の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去の会話履歴を画面に表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力処理
if prompt := st.chat_input("メッセージを入力してください..."):
    # ユーザーメッセージの表示と保存
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Geminiからの応答を取得
    with st.chat_message("assistant"):
        with st.spinner("考え中..."):
            try:
                # 過去の会話を反映して応答生成
                chat_history = [
                    {"role": m["role"], "parts": [{"text": m["content"]}]}
                    for m in st.session_state.messages
                ]
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=chat_history
                )
                response_text = response.text
                st.markdown(response_text)
                
                # アシスタントの応答を保存
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
