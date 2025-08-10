import os
import openai
import sys

# Set your OpenAI API key
# It's recommended to set this key as an environment variable:
# export OPENAI_API_KEY='YOUR_API_KEY'
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    # This check is now also in the main setup script, but keep it for direct calls to this script
    print("錯誤: OPENAI_API_KEY 環境變數未設定。請先設定您的金鑰。")
    sys.exit(1)

# Define configuration for different generation types
GENERATION_CONFIG = {
    # Django Backend
    "django_models": {
        "prompt_path": "backend/prompts/django_models_prompt.txt",
        "output_path": "backend/django_risk_app/risk_metrics/models.py",
        "system_message": "你是專業的 Django 工程師。"
    },
    "django_serializers": {
        "prompt_path": "backend/prompts/django_serializers_prompt.txt",
        "output_path": "backend/django_risk_app/risk_metrics/serializers.py",
        "system_message": "你是專業的 Django REST Framework 工程師。"
    },
    "django_views": {
        "prompt_path": "backend/prompts/django_views_prompt.txt",
        "output_path": "backend/django_risk_app/risk_metrics/views.py",
        "system_message": "你是專業的 Django REST Framework 工程師。"
    },
    "django_urls": { # Optional: for generating app-specific urls
        "prompt_path": "backend/prompts/django_urls_prompt.txt",
        "output_path": "backend/django_risk_app/risk_metrics/urls.py",
        "system_message": "你是專業的 Django URL 配置工程師。"
    },
    "django_models_test": {
        "prompt_path": "backend/prompts/django_models_test_prompt.txt",
        "output_path": "backend/django_risk_app/risk_metrics/tests/test_models.py",
        "system_message": "你是專業的 Django 測試工程師，擅長使用 Django TestCase。"
    },
    "django_serializers_test": {
        "prompt_path": "backend/prompts/django_serializers_test_prompt.txt",
        "output_path": "backend/django_risk_app/risk_metrics/tests/test_serializers.py",
        "system_message": "你是專業的 Django 測試工程師，擅長使用 Django REST Framework 的測試工具。"
    },
    "django_views_test": {
        "prompt_path": "backend/prompts/django_views_test_prompt.txt",
        "output_path": "backend/django_risk_app/risk_metrics/tests/test_views.py",
        "system_message": "你是專業的 Django 測試工程師，擅長使用 Django REST Framework 的 APITestCase。"
    },
    # FastAPI Backend
    "fastapi_main_test": {
        "prompt_path": "backend/prompts/fastapi_main_test_prompt.txt",
        "output_path": "backend/fastapi_etl_service/tests/test_main.py",
        "system_message": "你是專業的 FastAPI 測試工程師，擅長使用 TestClient。"
    },
    # React Frontend
    "react_component": {
        "prompt_path": "frontend-react/prompts/react_component_prompt.txt",
        "output_path": "frontend-react/src/components/PortfolioRiskDisplay.js",
        "system_message": "你是專業的 React 開發者，擅長使用 Tailwind CSS。"
    },
    "react_component_test": {
        "prompt_path": "frontend-react/prompts/react_component_test_prompt.txt",
        "output_path": "frontend-react/src/components/__tests__/PortfolioRiskDisplay.test.jsx",
        "system_message": "你是專業的 React 測試工程師，擅長使用 React Testing Library 和 Jest。"
    },
    # Flutter App
    "flutter_widget": {
        "prompt_path": "flutter-app/prompts/flutter_widget_prompt.txt",
        "output_path": "flutter-app/lib/widgets/risk_metric_card.dart",
        "system_message": "你是專業的 Flutter 開發者，擅長使用 Material Design。"
    },
    "flutter_widget_test": {
        "prompt_path": "flutter-app/prompts/flutter_widget_test_prompt.txt",
        "output_path": "flutter-app/integration_test/risk_metric_card_test.dart",
        "system_message": "你是專業的 Flutter 測試工程師，擅長使用 flutter_test 和 integration_test。"
    }
}

def generate_code(gen_type: str):
    """
    Based on the specified type, reads content from a prompt file, calls OpenAI API
    to generate code, and writes it to the target file.
    """
    if gen_type not in GENERATION_CONFIG:
        print(f"錯誤: 不支援的生成類型 '{gen_type}'。支援的類型有: {', '.join(GENERATION_CONFIG.keys())}")
        sys.exit(1)

    config = GENERATION_CONFIG[gen_type]
    prompt_path = config["prompt_path"]
    output_path = config["output_path"]
    system_message = config["system_message"]

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
    except FileNotFoundError:
        print(f"錯誤: Prompt 檔案 '{prompt_path}' 不存在。")
        sys.exit(1)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"正在呼叫 OpenAI API 生成 {gen_type} 程式碼，prompt 來自: {prompt_path}...")
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",  # You can choose a different model, e.g., "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2  # Adjust to control randomness of generated content
        )
        code = resp.choices[0].message.content
    except openai.error.OpenAIError as e:
        print(f"呼叫 OpenAI API 時發生錯誤: {e}")
        print("請檢查您的 API 金鑰和網路連線。")
        sys.exit(1)
    except Exception as e:
        print(f"發生未知錯誤: {e}")
        sys.exit(1)

    # Wrap the generated code with comments indicating it's AI-generated
    # This helps in distinguishing generated content and allows the user to uncomment
    # code after reviewing.
    final_code = f"# AI 生成程式碼開始\n# 請審閱後移除註釋並使用\n{code}\n# AI 生成程式碼結束\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_code)

    print(f"{gen_type} 程式碼生成完畢，儲存至: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python generate_ai_code.py <生成類型>")
        print(f"可用生成類型: {', '.join(GENERATION_CONFIG.keys())}")
        sys.exit(1)

    gen_type = sys.argv[1]
    generate_code(gen_type)
