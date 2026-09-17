import os
import time
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("🤖 Gemini AI Chat App")

# アイコン画像の設定（GitHubに icon.png があれば使用、なければ絵文字）
ASSISTANT_AVATAR = "icon.png" if os.path.exists("icon.png") else "🤖"

# APIキーの取得
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("APIキーが設定されていません。StreamlitのSecretsに GEMINI_API_KEY を設定してください。")
    st.stop()

# Clientの初期化
client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# サイドバー設定
# ---------------------------------------------------------
st.sidebar.title("⚙️ チャット設定")

# 1. AIの性格・設定
st.sidebar.subheader("🤖 AIの性格")
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
    ai_setting = persona_options[selected_persona]
else:
    user_custom_setting = st.sidebar.text_area(
        "AIの性格・特徴",
        value="自分のことが好きな女子高生。少し照れくさそうにしつつ、常にユーザーを肯定して仲良く会話してください。",
        height=100
    )
    ai_setting = user_custom_setting

# 2. ユーザー自身の情報（設定）
st.sidebar.subheader("👤 あなたの情報（プロフィール）")
user_profile = st.sidebar.text_area(
    "AIに知っておいてほしいあなたに関する設定",
    value="名前：たくみ\n職業：学生\n好きなもの：ゲーム、音楽\n呼び方：たくみ君と呼んでほしい",
    height=120,
    help="AIがあなたと話す時に参照するプロフィール情報です。"
)

# 3. システム指示の結合
system_instruction = f"""
あなたは以下のルールと指示に厳格に従って会話してください。

【AIの性格・役割】
{ai_setting}

【会話相手（ユーザー）の情報】
{user_profile}
"""

# ---------------------------------------------------------
# 会話リセットの確認ダイアログ機能
# ---------------------------------------------------------
@st.dialog("会話のリセット確認")
def confirm_reset():
    st.write("本当にこれまでの会話履歴を削除してリセットしますか？")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("いいえ", use_container_width=True):
            st.rerun()

if st.sidebar.button("💬 会話をリセット"):
    confirm_reset()

# ---------------------------------------------------------
# セッション状態（会話履歴）の初期化
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去の会話履歴を画面に表示
for message in st.session_state.messages:
    avatar = ASSISTANT_AVATAR if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ユーザーからの入力処理
if prompt := st.chat_input("メッセージを入力してください..."):
    # ユーザーメッセージの表示と保存
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Geminiからの応答を取得
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        with st.spinner("考え中..."):
            chat_history = [
                {"role": m["role"], "parts": [{"text": m["content"]}]}
                for m in st.session_state.messages
            ]
            
            # 503エラー（一時的高負荷）に強い自動リトライ処理（最大3回）
            max_retries = 3
            response_text = None
            
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=chat_history,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction
                        )
                    )
                    response_text = response.text
                    break  # 成功したらループを抜ける
                except Exception as e:
                    if "503" in str(e) and attempt < max_retries - 1:
                        time.sleep(2)  # 2秒待ってから再試行
                        continue
                    else:
                        st.error(f"エラーが発生しました: {e}")
                        break

            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
