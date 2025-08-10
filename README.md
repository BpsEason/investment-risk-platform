# AI 驅動的投資組合風險評估與報告平台

[![AI-Powered](https://img.shields.io/badge/AI-Powered-OpenAI-blue)](https://github.com/BpsEason/investment-risk-platform)  
倉庫連結: https://github.com/BpsEason/investment-risk-platform.git  

---

## 🚀 專案亮點

- **AI 驅動程式碼生成**  
  使用 `generate_ai_code.py` 與 OpenAI API，一鍵自動產出 Django model、DRF serializer、FastAPI 測試、React 組件、Flutter Widget 及其測試檔案。  

- **全棧微服務架構**  
  - Django 負責 VaR、CVaR、Sharpe Ratio 計算  
  - FastAPI 處理 ETL 和 API Gateway  
  - React + D3.js 展示互動式儀表板  
  - Flutter 提供行動端體驗  

- **一鍵啟動**  
  Docker Compose 同時編排 PostgreSQL、RabbitMQ、Redis、Django、FastAPI、React、Flutter，快速搭建開發與測試環境。  

- **自動化測試與 CI/CD**  
  單元、集成、E2E 测试覆蓋後端與前端；Mutation Testing (Mutpy、Stryker) 驗證測試品質；GitHub Actions 自動跑測試、產生報告並上傳 Codecov。  

---

## ⚡️ 快速啟動

1. Clone 倉庫並切換目錄  
   ```bash
   git clone https://github.com/BpsEason/investment-risk-platform.git
   cd investment-risk-platform
   ```

2. 複製並編輯環境變數  
   ```bash
   cp .env.example .env
   # 填入 OPENAI_API_KEY 與資料庫設定
   ```

3. 啟動所有服務  
   ```bash
   docker-compose up -d
   ```

4. 初始化 Django 資料庫  
   ```bash
   docker-compose exec django_app python manage.py makemigrations risk_metrics
   docker-compose exec django_app python manage.py migrate
   docker-compose exec django_app python manage.py createsuperuser
   ```

5. （選用）設定 Tailwind CSS for React  
   ```bash
   cd frontend-react
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   # 修改 tailwind.config.js 掃描 src 目錄
   ```

6. 存取應用  
   - React 網頁： http://localhost:3000  
   - Django Admin： http://localhost:8000/admin  
   - DRF Swagger： http://localhost:8000/swagger/  
   - FastAPI Docs： http://localhost:8001/docs  

---

## 🧠 AI 代碼生成示例

利用 `generate_ai_code.py` 讀取各模組下 `*/prompts/*.txt`，呼叫 OpenAI 生成 scaffold：

```bash
# 生成 Django Model
python generate_ai_code.py django_models

# 生成 React 組件
python generate_ai_code.py react_component

# 生成 FastAPI 測試
python generate_ai_code.py fastapi_main_test
```

生成的程式碼會以註釋標示：  
```python
# AI 生成程式碼開始
# 請審閱後移除註釋並使用
class PortfolioRisk(models.Model):
    ...
# AI 生成程式碼結束
```

---

## 🔑 關鍵程式碼範例

### Django Model (帶中文註解)

```python
# backend/django_risk_app/risk_metrics/models.py

import uuid
from django.db import models

class PortfolioRisk(models.Model):
    """
    投資組合風險模型：儲存每次計算結果
    """
    # UUID 作為主鍵、自動生成、不可修改
    portfolio_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="投資組合 ID"
    )
    # 風險指標名稱（VaR、CVaR、Sharpe Ratio）
    metric = models.CharField(max_length=100, verbose_name="風險指標")
    # 計算結果數值
    value = models.FloatField(verbose_name="指標數值")
    # 自動設定計算時間
    calculated_at = models.DateTimeField(auto_now_add=True, verbose_name="計算時間")

    class Meta:
        verbose_name = "投資組合風險"
        verbose_name_plural = "投資組合風險"
        unique_together = ("portfolio_id", "metric")  # 同一投資組合同一指標不可重複

    def __str__(self):
        # 管理介面顯示：「ID – 指標」
        return f"{self.portfolio_id} – {self.metric}"
```

---

### FastAPI 計算端點 (帶中文註解)

```python
# backend/fastapi_etl_service/main.py

@app.post("/calculate-risk", response_model=RiskCalculationResponse)
async def calculate_risk(request: RiskCalculationRequest):
    """
    根據歷史價格計算指定風險指標
    """
    if not request.data:
        raise HTTPException(status_code=400, detail="請提供要計算的數據。")

    # 將價格抽取為 pandas Series，計算日收益率
    prices = pd.Series(d["price"] for d in request.data)
    returns = prices.pct_change().dropna()
    if returns.empty:
        raise HTTPException(status_code=400, detail="數據不足以計算收益率。")

    # 支援三種指標：VaR、CVaR、Sharpe Ratio
    if request.metric == "VaR":
        cl = request.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses) * (1 - cl))
        result = losses[idx]  # 歷史模擬法 VaR
        unit = "%"
    elif request.metric == "CVaR":
        cl = request.parameters.get("confidence_level", 0.95)
        losses = -returns.sort_values().values
        idx = int(len(losses) * (1 - cl))
        result = losses[idx:].mean() if len(losses) > idx else 0.0
        unit = "%"
    else:  # Sharpe Ratio
        rf = request.parameters.get("risk_free_rate", 0.0)
        mean_ret, std_ret = returns.mean(), returns.std()
        result = (mean_ret - rf) / std_ret if std_ret else 0.0
        unit = "ratio"

    return RiskCalculationResponse(
        metric=request.metric,
        value=float(result),
        unit=unit,
        description=f"{request.metric} 計算完成"
    )
```

---

### React 顯示組件 (帶中文註解)

```jsx
// frontend-react/src/components/PortfolioRiskDisplay.js

import React from 'react';

/**
 * 風險指標顯示元件
 * @param {Array<{ metric: string, value: number }>} riskData
 */
function PortfolioRiskDisplay({ riskData }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {riskData.map(({ metric, value }) => (
        <div key={metric} className="p-4 bg-white rounded shadow">
          {/* 顯示風險指標名稱 */}
          <h3 className="text-xl font-semibold">{metric}</h3>
          {/* 根據指標格式化數值 */}
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

### Flutter Widget (帶中文註解)

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
        // 顯示指標名稱
        title: Text(metric, style: const TextStyle(fontSize: 18)),
        // 右側顯示指標數值，非比率轉為百分比
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

歡迎提交 Issues、Pull Requests。請先 Fork 本專案並建立 feature branch。  
本專案採用 [MIT License](LICENSE)。  

---

感謝你的關注，立即體驗 AI 驅動的開發流程！
