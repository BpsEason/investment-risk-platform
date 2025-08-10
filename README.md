# AI 驅動的投資組合風險評估與報告平台

[![AI-Powered](https://img.shields.io/badge/AI-Powered-OpenAI-blue)]()

---

## 🚀 專案功能

- **自動化風險計算**  
  支援 VaR、CVaR、Sharpe Ratio，結合歷史模擬與統計方法，一鍵取回核心指標。

- **AI 驅動程式碼生成**  
  利用 `generate_ai_code.py` 搭配 OpenAI API，自動 scaffold 後端模型、API、前端組件、行動端 Widget 及對應測試。

- **互動式 API 文件**  
  - Django REST Framework + drf-yasg：`/swagger/`、`/redoc/`  
  - FastAPI 原生：`/docs`、`/redoc`

- **多端可視化展示**  
  - **React + D3.js**：動態長條圖  
  - **Flutter**：卡片式風險指標

- **微服務 ＋ 容器化**  
  Docker Compose 一鍵啟動 PostgreSQL、RabbitMQ、Redis、Django、FastAPI、React、Flutter

- **全面測試 ＆ CI/CD**  
  - 單元、集成、E2E 測試  
  - Mutation Testing (Mutpy、Stryker)  
  - GitHub Actions 自動跑測試、上傳 Codecov

---

## 🗺 系統架構

```
┌──────────────┐       ┌──────────────┐
│  React Web   │◀──────▶│   Django     │
│ + D3.js 圖表 │       │ 風險計算微服務 │
└──────────────┘       └───────┬──────┘
        ▲                        │
        │                        ▼
┌──────────────┐       ┌──────────────┐
│ Flutter App  │◀──────▶│   FastAPI    │
│ (行動端 UI)   │       │ ETL ＆ Gateway│
└──────────────┘       └───────┬──────┘
        │                        │
        ▼                        ▼
┌──────────────┐       ┌──────────────┐
│ PostgreSQL   │       │ RabbitMQ ＋  │
│ (資料庫)      │       │ Redis / Celery│
└──────────────┘       └──────────────┘
```

---

## 🛠 技術棧

- **後端**：Django 4.x, DRF, FastAPI, Celery, PostgreSQL, RabbitMQ, Redis  
- **前端**：React 18, Redux, D3.js, Tailwind CSS  
- **行動端**：Flutter, Provider  
- **自動化**：Docker Compose, GitHub Actions, Codecov  
- **AI 生成**：OpenAI API via `generate_ai_code.py`  

---

## ⚡️ 快速啟動

1. 複製並編輯環境設定  
   ```bash
   cp .env.example .env
   # 填入 OPENAI_API_KEY、資料庫與 Broker 資訊
   ```

2. 啟動所有服務  
   ```bash
   docker-compose up -d
   ```

3. 初始化 Django  
   ```bash
   docker-compose exec django_app python manage.py makemigrations risk_metrics
   docker-compose exec django_app python manage.py migrate
   docker-compose exec django_app python manage.py createsuperuser
   ```

4. （選用）安裝 React Tailwind CSS  
   ```bash
   cd frontend-react
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

5. 存取應用  
   - **React 網頁**：http://localhost:3000  
   - **Django Admin**：http://localhost:8000/admin  
   - **DRF Swagger**：http://localhost:8000/swagger/  
   - **FastAPI Docs**：http://localhost:8001/docs  

---

## 🧠 AI 代碼生成 & Prompt 使用說明

本專案將「意圖驅動」的 prompt 存放於專案目錄下，搭配 `generate_ai_code.py` 自動產生程式骨架與測試：

### 1. Prompt 目錄結構

- `backend/prompts/`  
  - `django_models_prompt.txt`  
  - `django_serializers_prompt.txt`  
  - `django_views_prompt.txt`  
  - `django_models_test_prompt.txt`  
  - `...`

- `frontend-react/prompts/`  
  - `react_component_prompt.txt`  
  - `react_component_test_prompt.txt`

- `flutter-app/prompts/`  
  - `flutter_widget_prompt.txt`  
  - `flutter_widget_test_prompt.txt`

### 2. 編輯 Prompt

打開對應 `.txt` 檔，修改或補充需求描述，例如：

```txt
# backend/prompts/django_models_prompt.txt
請生成 Django model 定義檔，名稱為 PortfolioRisk。
欄位有：
- portfolio_id (UUIDField...)
- metric (CharField...)
...
```

### 3. 執行生成

```bash
# 生成 Django Model
python generate_ai_code.py django_models

# 生成 React 組件
python generate_ai_code.py react_component

# 生成 FastAPI 測試
python generate_ai_code.py fastapi_main_test
```

> **可用生成類型**  
> `django_models`, `django_serializers`, `django_views`, `django_urls`,  
> `django_models_test`, `django_serializers_test`, `django_views_test`,  
> `fastapi_main_test`,  
> `react_component`, `react_component_test`,  
> `flutter_widget`, `flutter_widget_test`

### 4. 審閱與啟用

生成後會在目標檔案頂部／底部加入：

```python
# AI 生成程式碼開始
# 請審閱後移除註解並使用
…
# AI 生成程式碼結束
```

審閱內容無誤後，移除這些標記註解，即可正式啟用自動生成的程式碼。

---

## 🔍 常見問題 (FAQ)

1. **怎麼新增自訂風險指標？**  
   編輯 `backend/fastapi_etl_service/main.py` 中的 `/calculate-risk` 分支，實作新的指標計算；同步新增對應測試。

2. **如何調整 Prompt？**  
   修改 `*/prompts/*.txt`，然後重跑 `generate_ai_code.py <類型>` 即可。

3. **如何整合到現有 CI/CD？**  
   參考 `.github/workflows/main.yml`，將安裝依賴、遷移、測試、覆蓋率、Documentation 檢查等步驟納入既有流水線。

4. **Mutation Testing 怎麼用？**  
   - Python：`mut.py backend/django_risk_app/risk_metrics`  
   - JavaScript：`npx stryker run`

5. **如何安全管理機密？**  
   建議採用雲端 Secret Manager 或 Kubernetes Secret，避免將真實憑證提交至版本庫。

---

## 🔑 關鍵程式碼範例

### 1. Django Model

```python
# backend/django_risk_app/risk_metrics/models.py

import uuid
from django.db import models

class PortfolioRisk(models.Model):
    # 主鍵：使用 UUID，自動生成
    portfolio_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="投資組合 ID"
    )
    # 風險指標名稱
    metric = models.CharField(max_length=100, verbose_name="風險指標")
    # 指標數值
    value = models.FloatField(verbose_name="指標數值")
    # 自動填入計算時間
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name="計算時間")

    class Meta:
        unique_together = ("portfolio_id", "metric")  # 同一組合同一指標不可重複
        verbose_name = "投資組合風險"
        verbose_name_plural = "投資組合風險"

    def __str__(self):
        # 管理介面顯示：UUID – 指標
        return f"{self.portfolio_id} – {self.metric}"
```

---

### 2. FastAPI 計算端點

```python
# backend/fastapi_etl_service/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

class RiskCalculationRequest(BaseModel):
    data: list[dict[str, float]]
    metric: str
    parameters: dict[str, float] = {}

class RiskCalculationResponse(BaseModel):
    metric: str
    value: float
    unit: str
    description: str

@app.post("/calculate-risk", response_model=RiskCalculationResponse)
async def calculate_risk(req: RiskCalculationRequest):
    # 驗證輸入
    if not req.data:
        raise HTTPException(400, "請提供價格數據。")

    # 建立收益率序列
    prices = pd.Series(item["price"] for item in req.data)
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise HTTPException(400, "數據不足以計算收益率。")

    # 計算邏輯
    if req.metric == "VaR":
        cl = req.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses)*(1-cl))
        val = losses[idx]
        unit = "%"
    elif req.metric == "CVaR":
        cl = req.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses)*(1-cl))
        val = losses[idx:].mean() if len(losses)>idx else 0.0
        unit = "%"
    elif req.metric == "Sharpe Ratio":
        rf = req.parameters.get("risk_free_rate", 0.0)
        mean = returns.mean()
        std = returns.std()
        val = (mean - rf)/std if std else 0.0
        unit = "ratio"
    else:
        raise HTTPException(400, f"不支援的指標：{req.metric}")

    return RiskCalculationResponse(
        metric=req.metric,
        value=float(val),
        unit=unit,
        description=f"{req.metric} 計算完成"
    )
```

---

### 3. React 顯示組件

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

### 4. Flutter Widget

```dart
// flutter-app/lib/widgets/risk_metric_card.dart

import 'package:flutter/material.dart';

/// 顯示單一風險指標的卡片
class RiskMetricCard extends StatelessWidget {
  final String metric;
  final double value;

  const RiskMetricCard({
    Key? key,
    required this.metric,
    required this.value,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: ListTile(
        title: Text(metric, style: const TextStyle(fontSize: 18)),
        trailing: Text(
          metric == 'Sharpe Ratio'
              ? value.toStringAsFixed(2)
              : '${(value * 100).toStringAsFixed(2)}%',
          style: const TextStyle(fontSize: 20, color: Colors.blue),
        ),
      ),
    );
  }
}
```

---

## 🤝 貢獻與授權

歡迎開啟 Issue 或 Pull Request。  
本專案採用 MIT License，詳見 [LICENSE](LICENSE)。  

---

祝開發順利，盡情體驗 **AI 驅動** 的全流程開發！
