# AI 驅動的投資組合風險評估與報告平台

- **自動化風險計算**  
  支援 VaR、CVaR、Sharpe Ratio，結合歷史模擬與統計模型，一鍵取得風險指標。

- **AI 驅動程式碼生成**  
  透過 `generate_ai_code.py` 與 OpenAI API，自動 scaffold Django、FastAPI、React、Flutter 的程式骨架與測試檔。

- **互動式 API 文件**  
  - Django: `/swagger/`、`/redoc/`（drf-yasg）  
  - FastAPI: `/docs`、`/redoc`（原生支援）

- **多端可視化**  
  - **React + D3.js**：動態長條圖展示風險指標  
  - **Flutter**：原生行動端卡片式顯示

- **微服務與容器化**  
  Docker Compose 一鍵啟動 PostgreSQL、RabbitMQ、Redis、Django、FastAPI、React、Flutter

- **全面測試 & CI/CD**  
  - 單元、集成、E2E 測試  
  - Mutation Testing (Mutpy、Stryker)  
  - GitHub Actions 自動跑測試、覆蓋率上傳 Codecov

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
│ (行動端 UI)   │       │ ETL & Gateway│
└──────────────┘       └───────┬──────┘
        │                        │
        ▼                        ▼
┌──────────────┐       ┌──────────────┐
│ PostgreSQL   │       │ RabbitMQ +   │
│ (資料庫)      │       │ Redis / Celery│
└──────────────┘       └──────────────┘
```

---

## ⚡️ 快速啟動

1. 複製並編輯環境設定  
   ```bash
   cp .env.example .env
   # 填入 OPENAI_API_KEY 及資料庫、Broker 資訊
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

4. （選用）React 安裝 Tailwind CSS  
   ```bash
   cd frontend-react
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

5. 存取應用  
   - React 前端： http://localhost:3000  
   - Django Admin： http://localhost:8000/admin  
   - DRF Swagger： http://localhost:8000/swagger/  
   - FastAPI Docs： http://localhost:8001/docs  

---

## 🔍 常見問題 (FAQ)

**1. 如何新增自訂風險指標？**  
編輯 `backend/fastapi_etl_service/main.py` 中 `/calculate-risk` 邏輯，為新的 `request.metric` 分支撰寫計算程式，並新增對應單元測試。

**2. 怎麼調整 AI 生成的骨架程式？**  
修改 `*/prompts/*.txt` 中的 prompt，執行：  
```bash
python generate_ai_code.py <生成類型>
```  
再審閱標記區段（`# AI 生成程式碼開始` 到 `# AI 生成程式碼結束`），移除註解即可啟用。

**3. 如何整合到現有 CI/CD？**  
參考 `.github/workflows/main.yml`，將步驟匯入現有 pipeline：  
- 安裝依賴  
- 執行遷移  
- 跑測試＋覆蓋率報告  
- 上傳 Codecov  
- 驗證 Swagger/Docs 可用性

**4. 如何使用 Mutation Testing？**  
- Python (Mutpy)：  
  ```bash
  mut.py backend/django_risk_app/risk_metrics
  ```  
- JavaScript (Stryker)：  
  ```bash
  npx stryker run
  ```  
修補未被中和（killed）的 mutation，提升測試強度。

**5. 機密如何安全管理？**  
建議使用 AWS Secrets Manager、Azure Key Vault 或 Kubernetes Secret，避免將敏感資訊推上 Git。

---

## 🔑 關鍵程式碼範例

### Django Model

```python
# backend/django_risk_app/risk_metrics/models.py

import uuid
from django.db import models

class PortfolioRisk(models.Model):
    portfolio_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="投資組合 ID"
    )
    metric = models.CharField(max_length=100, verbose_name="風險指標")
    value = models.FloatField(verbose_name="指標數值")
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name="計算時間")

    class Meta:
        unique_together = ("portfolio_id", "metric")
        verbose_name = "投資組合風險"
        verbose_name_plural = "投資組合風險"

    def __str__(self):
        return f"{self.portfolio_id} – {self.metric}"
```

### FastAPI 計算端點

```python
# backend/fastapi_etl_service/main.py

@app.post("/calculate-risk", response_model=RiskCalculationResponse)
async def calculate_risk(request: RiskCalculationRequest):
    if not request.data:
        raise HTTPException(400, "請提供要計算的數據。")

    prices = pd.Series(d["price"] for d in request.data)
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise HTTPException(400, "數據不足以計算收益率。")

    if request.metric == "VaR":
        cl = request.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses) * (1 - cl))
        result = losses[idx]
        unit = "%"
    elif request.metric == "Sharpe Ratio":
        rf = request.parameters.get("risk_free_rate", 0.0)
        mean_ret, std_ret = returns.mean(), returns.std()
        result = (mean_ret - rf) / std_ret if std_ret else 0.0
        unit = "ratio"
    else:
        # CVaR 或其他指標
        ...

    return RiskCalculationResponse(
        metric=request.metric,
        value=float(result),
        unit=unit,
        description=f"{request.metric} 計算完成"
    )
```

### React 顯示組件

```jsx
// frontend-react/src/components/PortfolioRiskDisplay.js

import React from 'react';

/**
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

### Flutter Widget

```dart
// flutter-app/lib/widgets/risk_metric_card.dart

import 'package:flutter/material.dart';

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

歡迎開 issue、Pull Request；請先 Fork 並建立 feature branch。  
本專案採用 MIT License，詳見 [LICENSE](LICENSE)。  

祝開發順利，盡情體驗 AI 驅動的全流程開發！
