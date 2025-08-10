# 投資組合風險評估與報告平台

**倉庫連結**  
https://github.com/BpsEason/investment-risk-platform.git

---

## 🚀 亮點

- AI 驅動的程式碼生成  
  • 利用 OpenAI prompts 自動產出 Django models、DRF serializers/viewsets、FastAPI 測試、React 組件、Flutter widgets 及其測試檔案。  

- 微服務與模組化設計  
  • Django 負責核心風險指標計算（VaR、CVaR、Sharpe Ratio）  
  • FastAPI 作為 ETL 與 API Gateway  
  • React + D3.js 提供互動式網頁儀表板  
  • Flutter 行動端隨時掌握風險  

- 一鍵啟動、多語言環境  
  • Docker Compose 編排 PostgreSQL、RabbitMQ、Redis、Django、FastAPI、React、Flutter  
  • 環境隔離、易於部署  

- 全面測試覆蓋  
  • Django: `pytest` + `coverage`  
  • FastAPI: `pytest` + `TestClient`  
  • React: Jest + React Testing Library  
  • Flutter: `flutter_test` + `integration_test`  
  • Mutation Testing: Mutpy (Python) & Stryker (JavaScript)  

- CI/CD 自動化  
  • GitHub Actions 實現程式碼檢出、安裝依賴、跑測試、產生覆蓋率報告、並上傳 Codecov  
  • 部署前自動檢查 Swagger / Redoc 文檔可用性  

---

## 🏗 系統架構概覽

```
┌────────────┐          ┌──────────────┐
│  React Web │◀───API──▶│   Django     │
└────────────┘          │ Microservice │
      ▲                 └───┬──────────┘
      │                     │
      │                     ▼
┌────────────┐          ┌──────────────┐
│ Flutter    │◀───API──▶│  FastAPI     │
│ Mobile App │          │ ETL & Gateway│
└────────────┘          └───┬──────────┘
      │                     │
      ▼                     ▼
┌────────────┐          ┌──────────────┐
│ PostgreSQL │          │ RabbitMQ +   │
│   Database │          │ Redis / Celery│
└────────────┘          └──────────────┘
```

---

## 🛠 技術棧

### 後端

- Django 4.x + Django REST Framework  
- FastAPI + Uvicorn  
- PostgreSQL  
- RabbitMQ + Celery + Redis  
- OpenAI API

### 前端

- React 18 + Redux + D3.js + Tailwind CSS  
- Flutter + Provider

### DevOps & CI/CD

- Docker Compose  
- GitHub Actions  
- Codecov  
- Mutpy & Stryker

---

## ⚡️ 快速啟動

1. Clone 倉庫  
   ```bash
   git clone https://github.com/BpsEason/investment-risk-platform.git
   cd investment-risk-platform
   ```

2. 複製 `.env` 並設定  
   ```bash
   cp .env.example .env
   # 編輯 .env 填入 OPENAI_API_KEY、資料庫與 broker 資訊
   ```

3. 啟動整個服務  
   ```bash
   docker-compose up -d
   ```

4. 執行 Django 遷移並建立管理員帳號  
   ```bash
   docker-compose exec django_app python manage.py makemigrations risk_metrics
   docker-compose exec django_app python manage.py migrate
   docker-compose exec django_app python manage.py createsuperuser
   ```

5. （選用）設定 Tailwind CSS  
   ```bash
   cd frontend-react
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   # 修改 tailwind.config.js 扫描 src，並在 src/index.css 撰寫 Tailwind 指令
   ```

6. 存取服務  
   - React 網頁： http://localhost:3000  
   - Django Admin： http://localhost:8000/admin  
   - DRF Swagger： http://localhost:8000/swagger/  
   - FastAPI Docs： http://localhost:8001/docs  

---

## 📂 專案結構

```
investment-risk-platform/
├── backend/
│   ├── django_risk_app/         # Django 風險指標微服務
│   └── fastapi_etl_service/     # ETL 與 API Gateway
├── frontend-react/              # React 網頁端
├── flutter-app/                 # Flutter 行動端
├── .github/workflows/           # CI/CD Pipeline
├── docker-compose.yml
├── generate_ai_code.py          # AI 代碼自動生成引擎
├── .env.example
└── README.md
```

---

## 🗝 關鍵程式碼示例（附中文註解）

### Django Model 範例

```python
# backend/django_risk_app/risk_metrics/models.py

import uuid
from django.db import models
from django.utils import timezone

class PortfolioRisk(models.Model):
    """
    投資組合風險模型，儲存每次風險計算結果
    """
    portfolio_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="投資組合 ID"
    )
    metric = models.CharField(
        max_length=100,
        verbose_name="風險指標名稱"
    )
    value = models.FloatField(
        verbose_name="指標數值"
    )
    calculated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="計算時間"
    )

    class Meta:
        verbose_name = "投資組合風險"
        verbose_name_plural = "投資組合風險"
        unique_together = ('portfolio_id', 'metric')  # 同一投資組合同一指標只能有一筆

    def __str__(self):
        # 回傳「ID – 指標」方便管理介面顯示
        return f"{self.portfolio_id} – {self.metric}"
```

### FastAPI 計算端點

```python
# backend/fastapi_etl_service/main.py

@app.post("/calculate-risk", response_model=RiskCalculationResponse)
async def calculate_risk(request: RiskCalculationRequest):
    """
    根據傳入的價格歷史數據計算指定風險指標（VaR、CVaR、Sharpe Ratio）
    """
    # 驗證輸入是否存在
    if not request.data:
        raise HTTPException(status_code=400, detail="請提供要計算的數據。")

    # 將價格列表轉為 pandas Series，計算日收益率
    prices = pd.Series(d["price"] for d in request.data)
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise HTTPException(status_code=400, detail="數據不足以計算收益率。")

    # 根據 metric 類型切換計算
    if request.metric == "VaR":
        cl = request.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses) * (1 - cl))
        result = losses[idx]
        description = f"歷史模擬法 VaR ({cl*100:.1f}%)"
        unit = "%"
    elif request.metric == "CVaR":
        cl = request.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses) * (1 - cl))
        result = losses[idx:].mean() if len(losses) > idx else 0.0
        description = f"歷史模擬法 CVaR ({cl*100:.1f}%)"
        unit = "%"
    elif request.metric == "Sharpe Ratio":
        rf = request.parameters.get("risk_free_rate", 0.0)
        mean_ret = returns.mean()
        std_ret = returns.std()
        result = (mean_ret - rf) / std_ret if std_ret else 0.0
        description = "基於歷史收益率的 Sharpe Ratio"
        unit = "ratio"
    else:
        raise HTTPException(status_code=400, detail=f"不支援的指標：{request.metric}")

    return RiskCalculationResponse(
        metric=request.metric,
        value=float(result),
        unit=unit,
        description=description
    )
```

### React 顯示組件

```jsx
// frontend-react/src/components/PortfolioRiskDisplay.js

import React from 'react';

/**
 * PortfolioRiskDisplay
 * @param {{ metric: string, value: number }[]} riskData - 風險數據陣列
 */
function PortfolioRiskDisplay({ riskData }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {riskData.map(({ metric, value }) => (
        <div key={metric} className="p-4 bg-white rounded shadow">
          <h3 className="text-xl font-semibold">{metric}</h3>
          <p className="mt-2 text-3xl text-blue-500">
            {(metric === 'Sharpe Ratio' ? value.toFixed(2) : (value * 100).toFixed(2) + '%')}
          </p>
        </div>
      ))}
    </div>
  );
}

export default PortfolioRiskDisplay;
```

### Flutter Widget 範例

```dart
// flutter-app/lib/widgets/risk_metric_card.dart

import 'package:flutter/material.dart';

/**
 * RiskMetricCard
 * 顯示單個風險指標的卡片
 */
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
    // Card 包裹 ListTile，標題顯示指標名稱，右側顯示指標數值
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: ListTile(
        title: Text(metric, style: const TextStyle(fontSize: 18)),
        trailing: Text(
          // 若不是比率則轉為百分比顯示
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

## 🤝 貢獻指南

1. Fork 本專案  
2. 建立 feature branch (`git checkout -b feat/your-feature`)  
3. Commit 並 push (`git commit -m "feat: add new feature"`；`git push`)  
4. 開 PR，待通過測試與審查後合併  

---

## 📄 授權條款

本專案採用 MIT License，詳見 [LICENSE](LICENSE)。
