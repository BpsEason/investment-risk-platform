from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import os
import openai
from typing import List, Dict
import numpy as np
import pandas as pd
import io

app = FastAPI(
    title="ETL & 風險計算服務",
    version="1.0.0",
    description="負責資料匯入、轉換和部分風險指標的初步計算。提供 VaR, CVaR 等風險指標的計算功能。",
    openapi_tags=[
        {"name": "risk_calculation", "description": "風險指標計算相關操作"},
        {"name": "etl", "description": "數據匯入和轉換操作"},
    ]
)

# Ensure OpenAI API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("錯誤: OPENAI_API_KEY 環境變數未設定。請先設定您的金鑰。")
    # In a production environment, you might want to raise an exception here
    # raise Exception("OpenAI API Key is not set")

class RiskCalculationRequest(BaseModel):
    data: List[Dict[str, float]] # Example: [{"price": 100}, {"price": 101}, ...]
    metric: str # Example: "VaR", "CVaR"
    parameters: Dict[str, float] = {} # Example: {"confidence_level": 0.95}

class RiskCalculationResponse(BaseModel):
    metric: str
    value: float
    unit: str = ""
    description: str = ""

@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint for the ETL & Risk Calculation Service."""
    return {"message": "歡迎來到 ETL 與風險計算服務！"}

@app.post("/calculate-risk", response_model=RiskCalculationResponse, tags=["risk_calculation"])
async def calculate_risk(request: RiskCalculationRequest):
    """
    接收原始數據並計算指定的風險指標。
    這是一個佔位符，實際的風險計算邏輯會更複雜，例如基於歷史模擬、參數模型或蒙地卡羅模擬。
    """
    if not request.data:
        raise HTTPException(status_code=400, detail="請提供要計算的數據。")

    prices = pd.Series([d.get("price", 0) for d in request.data])
    if prices.empty:
        raise HTTPException(status_code=400, detail="數據中沒有有效的價格資訊。")

    # 計算日收益率
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise HTTPException(status_code=400, detail="數據不足以計算收益率。")

    calculated_value = 0.0
    description = ""
    unit = ""

    if request.metric == "VaR":
        confidence_level = request.parameters.get("confidence_level", 0.95)
        # 使用歷史模擬法計算 VaR
        losses = -returns.sort_values().values # Convert to numpy array
        var_index = int(len(losses) * (1 - confidence_level))
        calculated_value = losses[var_index]
        description = f"這是基於歷史模擬的 {request.metric} ({confidence_level*100}%) 計算結果。"
        unit = "%"
    elif request.metric == "CVaR":
        confidence_level = request.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        var_index = int(len(losses) * (1 - confidence_level))
        cvar_losses = losses[var_index:]
        calculated_value = np.mean(cvar_losses) if cvar_losses.size > 0 else 0.0
        description = f"這是基於歷史模擬的 {request.metric} ({confidence_level*100}%) 計算結果。"
        unit = "%"
    elif request.metric == "Sharpe Ratio":
        risk_free_rate = request.parameters.get("risk_free_rate", 0.0)
        avg_return = returns.mean()
        std_dev = returns.std()
        if std_dev == 0:
            calculated_value = 0.0
        else:
            calculated_value = (avg_return - risk_free_rate) / std_dev
        description = f"這是基於歷史收益率的 {request.metric} 計算結果。"
        unit = "ratio"
    else:
        raise HTTPException(status_code=400, detail=f"不支援的風險指標: {request.metric}")

    # Optionally, use AI to generate a more detailed description based on calculation
    # try:
    #     ai_prompt = f"請用一句簡潔的話解釋投資組合中 {request.metric} 值為 {calculated_value:.4f} 的意義。"
    #     ai_resp = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": ai_prompt}],
    #         temperature=0.7
    #     )
    #     ai_explanation = ai_resp.choices[0].message.content.strip()
    #     description += f" AI 解釋: {ai_explanation}"
    # except Exception as e:
    #     print(f"AI 生成描述失敗: {e}")

    return RiskCalculationResponse(
        metric=request.metric,
        value=float(calculated_value),
        unit=unit,
        description=description
    )

@app.post("/etl/import-data", tags=["etl"])
async def import_data(file: UploadFile = File(...)):
    """
    接收 CSV 或 Excel 文件並模擬匯入數據。
    實際應用中，會將文件內容解析並存儲到資料庫。
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="未提供文件名。")

    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO((await file.read()).decode('utf-8')))
    elif file.filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(io.BytesIO(await file.read()))
    else:
        raise HTTPException(status_code=400, detail="只支援 CSV 或 XLSX 格式的文件。")

    print(f"模擬匯入文件: {file.filename}, 讀取到 {len(df)} 行數據。")
    print(f"部分內容預覽:\n{df.head()}")

    # 在這裡實現數據清洗、轉換和存儲到資料庫的邏輯
    # 例如：將 df 存入 PostgreSQL

    return {"message": f"文件 '{file.filename}' 已成功模擬匯入", "rows_processed": len(df)}
