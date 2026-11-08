import json
import os
from html import escape
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ------------------------------------------------------------------------------
# 1. 環境變數與 API Key 設定 (相容本機 .env 與 Streamlit Cloud Secrets)
# ------------------------------------------------------------------------------
load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ------------------------------------------------------------------------------
# 2. 定義 JSON Schema (活動公告整理器: event_name, event_date, location)
# ------------------------------------------------------------------------------
EVENT_SCHEMA = {
    "type": "object",
    "properties": {
        "event_name": {
            "type": "string",
            "description": "活動名稱，若未提及請填寫'未提及'",
        },
        "event_date": {
            "type": "string",
            "description": "活動日期與時間，若未提及請填寫'未提及'",
        },
        "location": {
            "type": "string",
            "description": "活動地點，若未提及請填寫'未提及'",
        },
    },
    "required": ["event_name", "event_date", "location"],
    "additionalProperties": False,
}

SYSTEM_INSTRUCTIONS = """
你是一個專業的活動資訊擷取助手。請分析使用者輸入的活動公告文字，並精確擷取以下資訊：
1. event_name: 活動名稱
2. event_date: 活動日期與時間
3. location: 活動地點

規則：
- 必須嚴格依據原文內容回答，不可憑空造假。
- 若原文未提供某項資訊，該欄位請填寫 '未提及'。
"""

# ------------------------------------------------------------------------------
# 3. Streamlit UI 介面設計
# ------------------------------------------------------------------------------
st.set_page_config(page_title="活動公告整理器", page_icon="📅")
st.title("📅 活動公告整理器 (Midterm Mini-Project)")
st.caption("自動將落落長的活動公告提煉出關鍵資訊：活動名稱、時間與地點。")

# 警示或金鑰檢查
if not api_key:
    st.error("⚠️ 未偵測到 API Key！請檢查 .env 或 Streamlit Secrets 設定。")

# API 開關與輸入欄位
enable_api = st.checkbox("啟用 API 呼叫 (預設關閉)", value=False)
user_input = st.text_area("請貼上活動公告原文：", height=200, placeholder="在此貼上活動公告內容...")

submit_btn = st.button("🚀 開始分析", type="primary")

# ------------------------------------------------------------------------------
# 4. 觸發分析與 API 呼叫處理
# ------------------------------------------------------------------------------
if submit_btn:
    # --- 離線防護檢查 (不發送 API 請求) ---
    if not enable_api:
        st.warning("⚠️ API 目前處於關閉狀態，請勾選「啟用 API 呼叫」後再送出。")
    elif not user_input or not user_input.strip():
        st.error("❌ 輸入不可為空白！")
    elif len(user_input) > 6000:
        st.error(f"❌ 輸入文字過長 (目前 {len(user_input)} 字)，上限為 6000 字元。")
    else:
        # --- 開始請求 API ---
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner("AI 正在分析公告內容..."):
                response = client.responses.create(
                    model=MODEL,
                    input=user_input,
                    instructions=SYSTEM_INSTRUCTIONS,
                    store=False,
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "event_extractor",
                            "schema": EVENT_SCHEMA,
                            "strict": True,
                        }
                    },
                )

            # --- 回應檢查機制 ---
            if response.status != "completed":
                raise ValueError(f"回應未完成或失敗，狀態：{response.status}")

            for output in response.output:
                if output.type == "message":
                    for content in output.content:
                        if content.type == "refusal":
                            raise ValueError(f"模型拒答：{content.refusal}")

            if not response.output_text or not response.output_text.strip():
                raise ValueError("模型未傳回可解析的文字成果。")

            # JSON 解析與呈現
            result_data = json.loads(response.output_text)
            
            st.success("🎉 分析完成！")
            st.subheader("📊 結構化提取結果")

            st.markdown(
                """
                <style>
                .result-card {
                    min-height: 92px;
                    padding-top: 2px;
                }
                .result-label {
                    margin-bottom: 12px;
                    color: #4f79d1;
                    font-size: 17px;
                    font-weight: 600;
                }
                .result-value {
                    color: #111827;
                    font-size: 42px;
                    font-weight: 700;
                    line-height: 1.15;
                    white-space: normal;
                    overflow-wrap: anywhere;
                    word-break: normal;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    '<div class="result-card"><div class="result-label">🎯 活動名稱</div>'
                    '<div class="result-value">'
                    + escape(str(result_data.get("event_name", "未提及")))
                    + "</div></div>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    '<div class="result-card"><div class="result-label">⏰ 日期時間</div>'
                    '<div class="result-value">'
                    + escape(str(result_data.get("event_date", "未提及")))
                    + "</div></div>",
                    unsafe_allow_html=True,
                )
            with col3:
                st.markdown(
                    '<div class="result-card"><div class="result-label">📍 活動地點</div>'
                    '<div class="result-value">'
                    + escape(str(result_data.get("location", "未提及")))
                    + "</div></div>",
                    unsafe_allow_html=True,
                )

            with st.expander("🔍 檢視原始 JSON 輸出"):
                st.json(result_data)

        except Exception as e:
            st.error(f"❌ 處理過程中發生錯誤：{e}")