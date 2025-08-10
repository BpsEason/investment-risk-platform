import 'package:flutter/material.dart';
import 'package:provider/provider.dart'; // Import provider
import 'package:flutter_app/widgets/risk_metric_card.dart'; // Assuming AI generates this
import 'package:http/http.dart' as http; // For API calls
import 'dart:convert'; // For JSON decoding

void main() {
  runApp(
    MultiProvider(
      providers: [
        // Add your Providers here, e.g.:
        // ChangeNotifierProvider(create: (_) => RiskDataProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '投資組合風險平台',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: '風險儀表板'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List<Map<String, dynamic>> _riskData = [];
  bool _isLoading = true;
  String _error = '';

  @override
  void initState() {
    super.initState();
    _fetchRiskData();
  }

  Future<void> _fetchRiskData() async {
    setState(() {
      _isLoading = true;
      _error = '';
    });
    try {
      // Assuming Django API is at localhost:8000
      final response = await http.get(Uri.parse('http://localhost:8000/api/portfolio-risks/'));
      if (response.statusCode == 200) {
        List<dynamic> data = json.decode(utf8.decode(response.bodyBytes));
        _riskData = data.map((item) => {
          'metric': item['metric'],
          'value': item['value'],
        }).toList();
      } else {
        _error = 'Failed to load risk data: ${response.statusCode}';
        // Fallback to sample data if API fails
        _riskData = [
          {'metric': 'VaR', 'value': 0.05},
          {'metric': 'CVaR', 'value': 0.07},
          {'metric': 'Sharpe Ratio', 'value': 1.2},
        ];
      }
    } catch (e) {
      _error = 'Error fetching risk data: $e';
      // Fallback to sample data if API fails
      _riskData = [
        {'metric': 'VaR', 'value': 0.05},
        {'metric': 'CVaR', 'value': 0.07},
        {'metric': 'Sharpe Ratio', 'value': 1.2},
      ];
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: _isLoading
              ? const CircularProgressIndicator()
              : _error.isNotEmpty
                  ? Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('錯誤: $_error', style: const TextStyle(color: Colors.red, fontSize: 16)),
                        const SizedBox(height: 10),
                        ElevatedButton(
                          onPressed: _fetchRiskData,
                          child: const Text('重試'),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          '使用預設範例數據顯示。',
                          textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 16, color: Colors.grey),
                        ),
                      ],
                    )
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: <Widget>[
                        const Text(
                          '您的投資組合風險指標概覽:',
                          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 20),
                        Expanded(
                          child: ListView.builder(
                            itemCount: _riskData.length,
                            itemBuilder: (context, index) {
                              final data = _riskData[index];
                              return RiskMetricCard(
                                metric: data['metric'],
                                value: data['value'],
                              );
                            },
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'AI 生成的 Widget 將在此處顯示更多詳細資訊。',
                          textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 16, color: Colors.grey),
                        ),
                      ],
                    ),
        ),
      ),
    );
  }
}
