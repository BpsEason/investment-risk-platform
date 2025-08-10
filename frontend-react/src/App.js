import React, { useEffect, useState } from 'react';
import './index.css'; // Tailwind CSS 導入
import PortfolioRiskDisplay from './components/PortfolioRiskDisplay';
import RiskChart from './components/RiskChart'; // 導入 RiskChart
import axios from 'axios';

function App() {
  const [riskData, setRiskData] = useState([]);
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'; // Django API Gateway URL

  useEffect(() => {
    // 範例：從 Django API 獲取數據
    // 實際應用中，您可能會從 FastAPI 的 /calculate-risk 端點獲取，然後存儲到 Django
    const fetchRiskData = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/portfolio-risks/`);
        const fetchedData = response.data.map(item => ({
          metric: item.metric,
          value: item.value
        }));
        setRiskData(fetchedData);
      } catch (error) {
        console.error('獲取風險數據失敗:', error);
        // 如果 API 無法訪問或無數據，使用模擬數據
        setRiskData([
          { metric: 'VaR', value: 0.05 },
          { metric: 'CVaR', value: 0.07 },
          { metric: 'Sharpe Ratio', value: 1.2 }
        ]);
      }
    };

    fetchRiskData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl w-full"> {/* 調整 max-w-2xl 為 max-w-4xl 以容納圖表 */}
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">投資組合風險概覽</h1>
        {riskData.length > 0 ? (
          <>
            <PortfolioRiskDisplay riskData={riskData} />
            <RiskChart riskData={riskData.filter(d => d.metric !== 'Sharpe Ratio')} /> {/* 假設圖表不展示Sharpe */}
          </>
        ) : (
          <p className="text-center text-gray-600">正在載入風險數據或無可用數據...</p>
        )}
        <p className="mt-8 text-center text-gray-600 text-sm">
          數據來源於後端 API 或使用預設範例數據。
        </p>
      </div>
    </div>
  );
}

export default App;
