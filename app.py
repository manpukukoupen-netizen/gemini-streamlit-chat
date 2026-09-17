{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyM4XboNtGI804oZHuOH+gzV",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/manpukukoupen-netizen/gemini-streamlit-chat/blob/main/app_py.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 411
        },
        "id": "Skfohbt9u2Kj",
        "outputId": "11cc67c0-6af6-4d52-b977-e9fbbb108195"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_4126/2764998591.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mos\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mgoogle\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mgenai\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mset_page_config\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpage_title\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\"Gemini Chat\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mpage_icon\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\"🤖\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "import os\n",
        "import streamlit as st\n",
        "from google import genai\n",
        "\n",
        "st.set_page_config(page_title=\"Gemini Chat\", page_icon=\"🤖\")\n",
        "st.title(\"🤖 Gemini AI Chat App\")\n",
        "\n",
        "# APIキーの取得（Streamlit Secretsまたは環境変数から）\n",
        "api_key = st.secrets.get(\"GEMINI_API_KEY\") or os.environ.get(\"GEMINI_API_KEY\")\n",
        "\n",
        "if not api_key:\n",
        "    st.error(\"APIキーが設定されていません。StreamlitのSecretsに GEMINI_API_KEY を設定してください。\")\n",
        "    st.stop()\n",
        "\n",
        "# Clientの初期化\n",
        "client = genai.Client(api_key=api_key)\n",
        "\n",
        "# セッション状態（会話履歴）の初期化\n",
        "if \"messages\" not in st.session_state:\n",
        "    st.session_state.messages = []\n",
        "\n",
        "# 過去の会話履歴を画面に表示\n",
        "for message in st.session_state.messages:\n",
        "    with st.chat_message(message[\"role\"]):\n",
        "        st.markdown(message[\"content\"])\n",
        "\n",
        "# ユーザーからの入力処理\n",
        "if prompt := st.chat_input(\"メッセージを入力してください...\"):\n",
        "    # ユーザーメッセージの表示と保存\n",
        "    st.chat_message(\"user\").markdown(prompt)\n",
        "    st.session_state.messages.append({\"role\": \"user\", \"content\": prompt})\n",
        "\n",
        "    # Geminiからの応答を取得\n",
        "    with st.chat_message(\"assistant\"):\n",
        "        with st.spinner(\"考え中...\"):\n",
        "            try:\n",
        "                # 過去の会話を反映して応答生成\n",
        "                chat_history = [\n",
        "                    {\"role\": m[\"role\"], \"parts\": [{\"text\": m[\"content\"]}]}\n",
        "                    for m in st.session_state.messages\n",
        "                ]\n",
        "                response = client.models.generate_content(\n",
        "                    model=\"gemini-2.5-flash\",\n",
        "                    contents=chat_history\n",
        "                )\n",
        "                response_text = response.text\n",
        "                st.markdown(response_text)\n",
        "\n",
        "                # アシスタントの応答を保存\n",
        "                st.session_state.messages.append({\"role\": \"assistant\", \"content\": response_text})\n",
        "            except Exception as e:\n",
        "                st.error(f\"エラーが発生しました: {e}\")"
      ]
    }
  ]
}
