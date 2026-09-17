import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("🤖 Gemini AI Chat App")

# APIキーの取得
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("APIキーが設定されていません。StreamlitのSecretsに GEMINI_API_KEY を設定してください。")
    st.stop()

# Clientの初期化
client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# サイドバーでAIの性格を選択する機能
# ---------------------------------------------------------
st.sidebar.title("⚙️ 設定")

# 性格の選択肢とプロンプトの定義
persona_options = {
    "標準（標準語で親切）": "あなたは親切で丁寧なAIアシスタントです。標準語で分かりやすく答えてください。",
    "関西弁キャラ": "あなたは明るくフレンドリーな関西弁のAIです。『〜やで』『〜やんか』『ほんま？』などを使って会話してください。",
    "ツンデレキャラ": "あなたはツンデレなAIです。最初は少し素っ気なく『べ、別にあなたのために教えるんじゃないんだからね！』という雰囲気を出しつつ、最後は親切に教えてください。",
    "猫耳メイド": "あなたは語尾に『ニャ』がつくるお給仕メイドAIです。ご主人様（ユーザー）に丁寧かつ可愛らしく『〜ですニャ！』と答えてください。"
}

selected_persona = st.sidebar.selectbox(
    "AIの性格を選んでね",
    list(persona_options.keys())
)

# 選択された性格の指示文（システムプロンプト）
system_instruction = persona_options[selected_persona]

# ---------------------------------------------------------
# セッション状態（会話履歴）の初期化
# ---------------------------------------------------------
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
                # 会話履歴の作成
                chat_history = [
                    {"role": m["role"], "parts": [{"text": m["content"]}]}
                    for m in st.session_state.messages
                ]
                
                # 性格（system_instruction）を指定して応答生成
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=chat_history,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                )
                response_text = response.text
                st.markdown(response_text)
                
                # アシスタントの応答を保存
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
