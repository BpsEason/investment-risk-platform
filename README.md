# AI 驅動的投資組合風險評估與報告平台

[![AI-Powered](https://img.shields.io/badge/AI-Powered-OpenAI-blue)](https://github.com/BpsEason/investment-risk-platform)

---

## 🚀 專案功能

- 自動化風險指標計算  
  • 支援 VaR、CVaR、Sharpe Ratio 三大常用風險指標  
  • 歷史模擬法 (Historical Simulation) 與統計模型並存  

- AI 驅動程式碼生成  
  • 一鍵產生 Django model、DRF serializer/viewset、FastAPI 測試、React/Flutter 組件與測試檔  
  • 利用 OpenAI API 自動填充模板，減少重複性工時  

- 即時互動式 API 文檔  
  • Django REST Framework + drf-yasg 提供 `/swagger/` 與 `/redoc/`  
  • FastAPI 原生支援 `/docs` (Swagger UI) 與 `/redoc`  

- 多端展示與可視化  
  • React + D3.js 長條圖動態顯示風險指標  
  • Flutter 原生行動端 Widget，隨時掌握組合風險  

- 可擴充微服務架構  
  • Django 負責核心運算微服務  
  • FastAPI 處理 ETL 與 API Gateway  
  • PostgreSQL、RabbitMQ、Redis 透過 Docker Compose 一鍵啟動  

- 全面測試與品質保證  
  • 後端單元測試與集成測試（pytest、Django TestCase、FastAPI TestClient）  
  • 前端測試（Jest + React Testing Library、flutter_test + integration_test）  
  • Mutation Testing：Mutpy (Python)、Stryker (JavaScript)  

- CI/CD 自動化流水線  
  • GitHub Actions 負責建置、測試、覆蓋率報告、API 文件可用性檢查  
  • Codecov 即時上傳多語言報告  

---

## 🗺 系統架構

```
┌─────────────┐       ┌───────────────┐
│  React Web  │◀─────▶│    Django     │
│ + D3.js 圖表│       │  風險微服務   │
└─────────────┘       │(VaR/CVaR/Sharpe)│
      ▲               └───────┬───────┘
      │                       │
      │                       ▼
┌─────────────┐       ┌───────────────┐
│ Flutter App │◀─────▶│    FastAPI    │
│ (行動端 UI) │       │  ETL & Gateway │
└─────────────┘       └───────┬───────┘
      │                       │
      ▼                       ▼
┌─────────────┐       ┌───────────────┐
│ PostgreSQL  │       │ RabbitMQ +    │
│   資料庫    │       │ Redis / Celery │
└─────────────┘       └───────────────┘
```

---

## 🛠 技術棧

- 後端：Django 4.x, DRF, FastAPI, Celery, PostgreSQL, RabbitMQ, Redis  
- 前端：React 18, Redux, D3.js, Tailwind CSS  
- 行動端：Flutter, Provider  
- 自動化：Docker Compose, GitHub Actions, Codecov  
- AI 生成：OpenAI API via `generate_ai_code.py`  

---

## ⚡️ 快速啟動

1. 複製並設定環境變數  
   ```bash
   cp .env.example .env
   # 在 .env 中填入 OPENAI_API_KEY、資料庫帳密等
   ```

2. 啟動服務  
   ```bash
   docker-compose up -d
   ```

3. 初始化 Django  
   ```bash
   docker-compose exec django_app python manage.py makemigrations risk_metrics
   docker-compose exec django_app python manage.py migrate
   docker-compose exec django_app python manage.py createsuperuser
   ```

4. （選配）React 安裝 Tailwind CSS  
   ```bash
   cd frontend-react
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

5. 存取應用  
   - Web 儀表板： http://localhost:3000  
   - Django Admin： http://localhost:8000/admin  
   - DRF Swagger： http://localhost:8000/swagger/  
   - FastAPI Docs： http://localhost:8001/docs  

---

## 🧠 AI 代碼生成

範例：  
```bash
# 產生 Django Model
python generate_ai_code.py django_models

# 產生 React 組件
python generate_ai_code.py react_component

# 產生 FastAPI 測試
python generate_ai_code.py fastapi_main_test
```

生成內容以以下標記開始/結束：  
```python
# AI 生成程式碼開始
# 請審閱後移除此註解並啟用
...
# AI 生成程式碼結束
```

---

## 🔑 關鍵程式碼範例

### Django Model（帶中文註解）
```python
# backend/django_risk_app/risk_metrics/models.py

import uuid
from django.db import models

class PortfolioRisk(models.Model):
    # UUID 作為主鍵、自動生成、不可編輯
    portfolio_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="投資組合 ID"
    )
    # 風險指標名稱
    metric = models.CharField(max_length=100, verbose_name="風險指標")
    # 計算結果數值
    value = models.FloatField(verbose_name="指標數值")
    # 自動設定計算時間
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name="計算時間")

    class Meta:
        unique_together = ("portfolio_id", "metric")  # 同一投資組合同一指標不可重複
        verbose_name = "投資組合風險"
        verbose_name_plural = "投資組合風險"

    def __str__(self):
        # 管理界面顯示「ID – 指標」
        return f"{self.portfolio_id} – {self.metric}"
```

### FastAPI 風險計算端點（帶中文註解）
```python
# backend/fastapi_etl_service/main.py

@app.post("/calculate-risk", response_model=RiskCalculationResponse)
async def calculate_risk(request: RiskCalculationRequest):
    # 驗證輸入是否存在
    if not request.data:
        raise HTTPException(status_code=400, detail="請提供要計算的數據。")

    # 將價格列表轉為 pandas Series，計算日收益率
    prices = pd.Series(d["price"] for d in request.data)
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise HTTPException(status_code=400, detail="數據不足以計算收益率。")

    # 根據 metric 切換計算邏輯
    if request.metric == "VaR":
        cl = request.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses) * (1 - cl))
        result = losses[idx]  # 歷史模擬法 VaR
    elif request.metric == "Sharpe Ratio":
        rf = request.parameters.get("risk_free_rate", 0.0)
        mean_ret, std_ret = returns.mean(), returns.std()
        result = (mean_ret - rf) / std_ret if std_ret else 0.0
    else:
        # 支援 CVaR 或其他自訂指標
        ...

    return RiskCalculationResponse(
        metric=request.metric,
        value=float(result),
        unit="%" if request.metric in ["VaR", "CVaR"] else "ratio",
        description=f"{request.metric} 計算完成"
    )
```

### React 顯示組件（帶中文註解）
```jsx
// frontend-react/src/components/PortfolioRiskDisplay.js

import React from 'react';

/**
 * 風險指標顯示元件
 * @param {{ metric: string, value: number }[]} riskData
 */
function PortfolioRiskDisplay({ riskData }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {riskData.map(({ metric, value }) => (
        <div key={metric} className="p-4 bg-white rounded shadow">
          <h3 className="text-xl font-semibold">{metric}</h3>
          {/* 根據指標型別格式化數值 */}
          <p className="mt-2 text-3xl text-blue-500">
            {metric === "Sharpe Ratio"
              ? value.toFixed(2)
              : `${(value * 100).toFixed(2)}%`}
          </p>
        </div>
      ))}
    </div>
  );
}

export default PortfolioRiskDisplay;
```

---

## 🤝 貢獻與授權

歡迎提交 Issue 或 Pull Request。  
本專案採用 MIT License，詳見 [LICENSE](LICENSE)。  

---
