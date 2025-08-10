// frontend-react/src/components/RiskChart.js (新增)
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

/**
 * 使用 D3.js 繪製投資組合風險指標的長條圖。
 * @param {Array<Object>} riskData - 包含 { metric: string, value: number } 的風險數據陣列。
 */
function RiskChart({ riskData }) {
  const svgRef = useRef();

  useEffect(() => {
    if (!riskData || riskData.length === 0) {
      d3.select(svgRef.current).selectAll("*").remove(); // Clear SVG if no data
      return;
    }

    const margin = { top: 20, right: 30, bottom: 40, left: 60 };
    const width = 600 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    // 清除舊的 SVG 內容
    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // X 軸比例尺
    const x = d3.scaleBand()
      .domain(riskData.map(d => d.metric))
      .range([0, width])
      .padding(0.1);

    // Y 軸比例尺
    const y = d3.scaleLinear()
      .domain([0, d3.max(riskData, d => d.value) * 1.2]) // Y 軸上限略高於最大值
      .range([height, 0]);

    // 繪製長條
    svg.selectAll(".bar")
      .data(riskData)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", d => x(d.metric))
      .attr("y", d => y(d.value))
      .attr("width", x.bandwidth())
      .attr("height", d => height - y(d.value))
      .attr("fill", "#60A5FA"); // Tailwind blue-400

    // 繪製 X 軸
    svg.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("fill", "#374151"); // Tailwind gray-700

    // 繪製 Y 軸
    svg.append("g")
      .call(d3.axisLeft(y).tickFormat(d3.format(".1%"))) // 格式化為百分比
      .selectAll("text")
      .attr("fill", "#374151"); // Tailwind gray-700

    // X 軸標籤
    svg.append("text")
      .attr("x", width / 2)
      .attr("y", height + margin.bottom - 5)
      .attr("text-anchor", "middle")
      .attr("fill", "#4B5563") // Tailwind gray-600
      .text("風險指標");

    // Y 軸標籤
    svg.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", -margin.left + 20)
      .attr("x", -height / 2)
      .attr("text-anchor", "middle")
      .attr("fill", "#4B5563") // Tailwind gray-600
      .text("數值 (%)");

  }, [riskData]); // 當 riskData 改變時重新繪製

  return (
    <div className="flex justify-center my-8 p-4 bg-white rounded-lg shadow-md">
      <svg ref={svgRef}></svg>
    </div>
  );
}

export default RiskChart;
