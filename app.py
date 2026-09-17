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
# サイドバーでユーザーがAIの性格を自由に設定できる機能
# ---------------------------------------------------------
st.sidebar.title("⚙️ AIの性格・設定")

# 設定モードの選択
mode = st.sidebar.radio(
    "設定方法",
    ["プリセットから選ぶ", "自分で自由につくる（カスタム）"]
)

if mode == "プリセットから選ぶ":
    persona_options = {
        "標準（標準語で親切）": "あなたは親切で丁寧なAIアシスタントです。標準語で分かりやすく答えてください。",
        "関西弁キャラ": "あなたは明るくフレンドリーな関西弁のAIです。『〜やで』『〜やんか』などを自然に使ってください。",
        "ツンデレキャラ": "あなたはツンデレなAIです。素っ気ない態度を取りつつも、最後は親切に答えてください。",
        "猫耳メイド": "あなたは語尾に『ニャ』をつけるお給仕メイドAIです。丁寧かつ可愛らしく答えてください。"
    }
    selected_persona = st.sidebar.selectbox("プリセット", list(persona_options.keys()))
    system_instruction = persona_options[selected_persona]

else:
    # ユーザーが自由にテキスト入力できるエリア
    user_custom_setting = st.sidebar.text_area(
        "AIの設定・性格を入力してください",
        value="ユーザーのことが大好きな女子高生。少し照れくさそうにしつつ、常にユーザーを肯定して仲良く会話してください。",
        height=150,
        help="例：「語尾を〜ロボにする」「ツンデレな先生」「自分のことが好きな女子高生」など"
    )
    
    # 入力された内容をそのままシステム指示にする
    system_instruction = f"あなたは以下の設定になりきって会話してください。\n【設定】\n{user_custom_setting}"

# ---------------------------------------------------------
# 会話履歴の消去ボタン（性格を変えた時などに便利）
# ---------------------------------------------------------
if st.sidebar.button("💬 会話をリセット"):
    st.session_state.messages = []
    st.rerun()

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
                
                # ユーザーが作った設定（system_instruction）を反映
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
