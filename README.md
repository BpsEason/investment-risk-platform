# 投資組合風險評估與報告平台 (Investment Portfolio Risk Assessment and Reporting Platform)

## 專案概覽
本平台旨在為內部投資組合提供自動化的風險指標計算（VaR, CVaR, 夏普比率等）和報告產出。目標是減少人工作業錯誤，加快報告產出速度，並提供即時可視化決策支援，服務於投研部門和風險管理團隊。

## 系統架構
- **前端介面**: React Web, Flutter App
- **API Gateway**: FastAPI
- **風險計算微服務**: Django + FastAPI (VaR/CVaR/夏普比率模組, ETL 資料匯入)
- **主要資料庫**: PostgreSQL
- **任務佇列**: RabbitMQ

## 技術棧
### 後端
- **核心框架**: Django + Django REST Framework
- **微服務**: FastAPI
- **資料庫**: PostgreSQL
- **任務佇列**: RabbitMQ + Celery
### 前端
- **Web**: React + Redux + D3.js
- **行動 App**: Flutter + Provider
### 自動化測試
- **Python**: pytest, Celery testing
- **JavaScript**: Jest + React Testing Library
- **Flutter**: flutter_test + integration_test
### Mutation Test
- **Python**: Mutpy
- **JavaScript**: Stryker
### CI/CD
- GitHub Actions
- Docker
- Kubernetes (可選)

## AI 驅動本機代碼生成
本專案整合 AI 輔助代碼生成流程，使用 `generate_ai_code.py` 腳本與 OpenAI API 協同工作。

## 快速啟動
1.  **設定 OpenAI API 金鑰**:
    在執行腳本前，請確保您的 `OPENAI_API_KEY` 環境變數已設定。否則腳本將提示您設定後再執行。
    ```bash
    export OPENAI_API_KEY='你的金鑰'
    ```
2.  **啟動 Docker 環境**:
    ```bash
    docker-compose up -d
    ```
3.  **所有基礎程式碼已自動生成**：您無需手動執行 `python generate_ai_code.py` 命令。本腳本已在專案建立過程中自動調用 AI 生成了核心的 Django 模型、序列化器、視圖、URL 以及各前端和後端服務的測試骨架。

## 測試覆蓋情況
本專案實施多層次測試策略，涵蓋單元測試、集成測試和 E2E 測試，確保程式碼品質。
- **後端 Django**:
    - `backend/django_risk_app/risk_metrics/tests/test_models.py`: 驗證模型欄位與行為。
    - `backend/django_risk_app/risk_metrics/tests/test_serializers.py`: 測試序列化器數據轉換。
    - `backend/django_risk_app/risk_metrics/tests/test_views.py`: 驗證 API 端點行為。
- **後端 FastAPI ETL**:
    - `backend/fastapi_etl_service/tests/test_main.py`: 測試 ETL 與風險計算端點。
- **前端 React**:
    - `frontend-react/src/components/__tests__/PortfolioRiskDisplay.test.jsx`: 測試組件渲染與交互。
- **Flutter**:
    - `flutter-app/integration_test/risk_metric_card_test.dart`: 測試 Widget 渲染與數據顯示。

## API 文件覆蓋情況
提供互動式與靜態 API 文件，便於開發與整合。
- **Django REST Framework**:
    - 透過 `drf-yasg` 在 `/swagger/` 和 `/redoc/` 提供 Swagger UI 和 ReDoc 互動式文件。
- **FastAPI**:
    - 自動在 `/docs` (Swagger UI) 和 `/redoc` 提供互動式文件。
- **靜態 API 規格**:
    - 可生成 `openapi.yaml` 或 `openapi.json` 靜態文件，供工具使用。

## 檔案結構
```
.
├── backend/
│   ├── django_risk_app/
│   │   ├── Dockerfile
│   │   ├── manage.py
│   │   ├── risk_platform_project/  (Django project settings, urls etc.)
│   │   │   ├── __init__.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   └── asgi.py
│   │   ├── risk_metrics/           (Django App)
│   │   │   ├── __init__.py
│   │   │   ├── models.py           # AI GENERATED
│   │   │   ├── serializers.py      # AI GENERATED
│   │   │   ├── views.py            # AI GENERATED
│   │   │   ├── urls.py             # AI GENERATED
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       ├── test_models.py      # AI GENERATED
│   │   │       ├── test_serializers.py # AI GENERATED
│   │   │       └── test_views.py       # AI GENERATED
│   │   └── requirements.txt
│   ├── fastapi_etl_service/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_main.py          # AI GENERATED
│   └── prompts/
│       ├── django_models_prompt.txt
│       ├── django_serializers_prompt.txt
│       ├── django_views_prompt.txt
│       ├── django_models_test_prompt.txt
│       ├── django_serializers_test_prompt.txt
│       ├── django_views_test_prompt.txt
│       ├── fastapi_main_test_prompt.txt
│       └── ...
├── frontend-react/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── PortfolioRiskDisplay.js # AI GENERATED
│   │   │   └── __tests__/
│   │   │       └── PortfolioRiskDisplay.test.jsx # AI GENERATED
│   └── prompts/
│       ├── react_component_prompt.txt
│       └── react_component_test_prompt.txt
├── flutter-app/
│   ├── pubspec.yaml
│   ├── lib/
│   │   ├── main.dart
│   │   └── widgets/
│   │       └── risk_metric_card.dart     # AI GENERATED
│   ├── integration_test/
│   │   └── risk_metric_card_test.dart  # AI GENERATED
│   └── prompts/
│       ├── flutter_widget_prompt.txt
│       └── flutter_widget_test_prompt.txt
├── .github/
│   └── workflows/
│       └── main.yml
├── docker-compose.yml
├── generate_ai_code.py
└── README.md
```
