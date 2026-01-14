import 'package:flutter/material.dart';
import '../core/api_client.dart';
import 'dart:convert';
import 'package:url_launcher/url_launcher.dart'; // Ensure user adds url_launcher to pubspec if not present, otherwise standard HTTP link

class SalesScreen extends StatefulWidget {
  final ApiClient apiClient;

  const SalesScreen({Key? key, required this.apiClient}) : super(key: key);

  @override
  _SalesScreenState createState() => _SalesScreenState();
}

class _SalesScreenState extends State<SalesScreen> {
  List<dynamic> _orders = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetchSales();
  }

  Future<void> _fetchSales() async {
    try {
      final orders = await widget.apiClient.getMySales();
      setState(() {
        _orders = orders;
        _loading = false;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error loading sales: $e')),
      );
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Sales & Orders'),
        backgroundColor: Colors.green[800],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _orders.isEmpty
              ? const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.shopping_bag_outlined, size: 64, color: Colors.grey),
                      SizedBox(height: 16),
                      Text("No sales yet.", style: TextStyle(color: Colors.grey)),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _orders.length,
                  itemBuilder: (context, index) {
                    final order = _orders[index];
                    return _buildOrderCard(order);
                  },
                ),
    );
  }

  Widget _buildOrderCard(dynamic order) {
    final status = order['status'] ?? 'PENDING';
    final isSecured = status == 'SECURED';
    
    return Card(
      elevation: 2,
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: isSecured ? Colors.green[100] : Colors.orange[100],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    status,
                    style: TextStyle(
                      color: isSecured ? Colors.green[800] : Colors.orange[800],
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ),
                Text(
                  "\$${order['amount']?.toStringAsFixed(0)}",
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              order['product_name'] ?? 'Unknown Product',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
            const SizedBox(height: 4),
            Text("Buyer: ${order['buyer_name'] ?? 'Anonymous'}"),
            const SizedBox(height: 16),
            const Divider(),
            if (order['contract_url'] != null)
              TextButton.icon(
                onPressed: () async {
                   // In a real app we would use url_launcher
                   // launchUrl(Uri.parse(order['contract_url']));
                   ScaffoldMessenger.of(context).showSnackBar(
                     const SnackBar(content: Text('Downloading Contract... (Demo)')),
                   );
                },
                icon: const Icon(Icons.picture_as_pdf),
                label: const Text("Download Contract"),
              )
            else
              const Text("Contract pending...", style: TextStyle(color: Colors.grey, fontStyle: FontStyle.italic)),
          ],
        ),
      ),
    );
  }
}
