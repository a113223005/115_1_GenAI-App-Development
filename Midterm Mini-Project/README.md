# 活動公告整理器

## 一、專案簡介

活動公告整理器是一個將活動公告原文轉換為結構化資訊的 Streamlit App。
使用者貼入活動公告後，App 會整理並呈現：

| 欄位 | 說明 |
|---|---|
| 活動名稱 | 公告中的活動名稱；未提供時顯示「未提及」 |
| 日期時間 | 活動公告中的活動日期與時間；未提供時顯示「未提及」 |
| 活動地點 | 公告中的活動地點；未提供時顯示「未提及」 |

目標使用者為需要快速閱讀社團、校園或其他活動公告的人。

## 二、主要功能

- 預設關閉 API 呼叫，可先進行離線介面與輸入檢查。
- 空白輸入與超過 6000 字元的內容會被阻止。
- 啟用 API 後，以 OpenAI Responses API 取得 JSON 結果。
- 使用 JSON Schema 約束活動名稱、日期時間與地點欄位。
- 解析後檢查回應狀態、文字內容與 JSON 結果。
- 結果以三欄卡片呈現，長日期與長地點可完整換行。
- 原始 JSON 可透過展開區檢視。

## 三、專案結構

```text
Midterm Mini-Project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example（如已建立）
└── .streamlit/
    └── secrets.example.toml（如已建立）
```

## 四、本機執行

建議使用 Python 3.14。

```powershell
cd "C:\Users\user\Documents\GitHub\115_1_GenAI-App-Development\Midterm Mini-Project"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
python -m streamlit run app.py
```

啟用 API 前：

1. 選擇「啟用 API 呼叫」。
2. 確認本機環境或 Streamlit Secrets 已設定 API 金鑰。
3. 貼入虛構活動公告。
4. 按「開始分析」。
5. 核對畫面欄位是否與原文一致。

不要提交 `.env`、`.streamlit/secrets.toml`、虛擬環境或任何包含真實金鑰的檔案。
本機設定與雲端 Secrets 名稱使用 `OPENAI_API_KEY`；模型名稱可透過 `OPENAI_MODEL` 設定。

## 五、Streamlit Community Cloud 部署

1. 將程式與 `requirements.txt` Push 到 GitHub 的 `main` 分支。
2. 在 Streamlit Community Cloud 建立 App。
3. Repository 選 `a113223005/115_1_GenAI-App-Development`。
4. Branch 選 `main`。
5. Main file path 選 `app.py`。
6. 在 Advanced settings 選擇可用的 Python 版本。
7. 在 Secrets 設定 `OPENAI_API_KEY` 與 `OPENAI_MODEL`。

也可使用根目錄的部署入口：

```text
Repository：a113223005/115_1_GenAI-App-Development
Branch：main
Main file path：app.py
```

完成 Cloud 部署後，將公開 App 網址填入此處：

```text
Streamlit App URL：待填
```

## 六、操作與驗收

| 測試項目 | 預期結果 |
|---|---|
| API 關閉 | 顯示 API 尚未啟用提示，不送出 API 請求 |
| 空白輸入 | 顯示不可為空白，不送出 API 請求 |
| 超過 6000 字元 | 顯示字數與長度錯誤，不送出 API 請求 |
| 正常虛構公告 | 一次有效提交最多送出一次模型請求；逐欄核對原文 |
| 資訊不足 | 缺少資訊的欄位應填「未提及」，不得補造 |
| 成功後再送出失敗資料 | 舊成功結果不應繼續保留為有效結果 |
| Cloud 真實 API | 至少完成一筆雲端真實 API 成功紀錄 |

驗收紀錄請填寫[第 8 週個人專題設計與驗收紀錄](./第08週_課堂簡化版_專題設計與驗收紀錄.md)，應包含 Cloud 網址、部署分支、入口、驗收日期、實際模型、輸入原文、輸出 JSON、人工核對與請求數。

## 七、套件相依

- Streamlit
- OpenAI SDK
- python-dotenv
- Pydantic
