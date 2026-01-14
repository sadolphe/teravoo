import 'package:flutter/material.dart';
import '../core/api_client.dart';
import 'dart:convert';
import 'dart:convert';

class SalesScreen extends StatefulWidget {
  final ApiClient apiClient;

  const SalesScreen({Key? key, required this.apiClient}) : super(key: key);

  @override
  _SalesScreenState createState() => _SalesScreenState();
}

class _SalesScreenState extends State<SalesScreen> with SingleTickerProviderStateMixin {
  List<dynamic> _orders = [];
  bool _loading = true;
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
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
      if (mounted) {
         ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading sales: $e')),
        );
      }
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    // Split orders
    final pendingOrders = _orders.where((o) => ['PENDING', 'SECURED'].contains(o['status'])).toList();
    final historyOrders = _orders.where((o) => !['PENDING', 'SECURED'].contains(o['status'])).toList();

    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text('Producer Dashboard', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black),
        bottom: TabBar(
          controller: _tabController,
          labelColor: const Color(0xFF1B5E20),
          unselectedLabelColor: Colors.grey,
          indicatorColor: const Color(0xFF1B5E20),
          tabs: [
            Tab(child: Row(mainAxisAlignment: MainAxisAlignment.center, children: [
               const Text("Inbox"),
               if (pendingOrders.isNotEmpty) ...[
                 const SizedBox(width: 8),
                 Container(
                   padding: const EdgeInsets.all(6),
                   decoration: const BoxDecoration(color: Colors.red, shape: BoxShape.circle),
                   child: Text("${pendingOrders.length}", style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold)),
                 )
               ]
            ])),
            const Tab(text: "History"),
          ],
        ),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(
              controller: _tabController,
              children: [
                _buildInboxList(pendingOrders),
                _buildHistoryList(historyOrders),
              ],
            ),
    );
  }

  Widget _buildInboxList(List<dynamic> orders) {
    if (orders.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inbox, size: 64, color: Colors.grey[300]),
            const SizedBox(height: 16),
            Text("All caught up!", style: TextStyle(color: Colors.grey[400], fontSize: 18)),
            const SizedBox(height: 8),
            Text("No new orders to validate.", style: TextStyle(color: Colors.grey[400])),
          ],
        ),
      );
    }
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: orders.length,
      itemBuilder: (context, index) => _buildActionCard(orders[index]),
    );
  }

  Widget _buildHistoryList(List<dynamic> orders) {
     if (orders.isEmpty) {
      return const Center(child: Text("No history yet.", style: TextStyle(color: Colors.grey)));
    }
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: orders.length,
      itemBuilder: (context, index) => _buildHistoryCard(orders[index]),
    );
  }

  Widget _buildActionCard(dynamic order) {
    return Card(
      elevation: 4,
      shadowColor: Colors.green.withOpacity(0.2),
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: () => _showDecisionSheet(order),
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: Colors.green[50], borderRadius: BorderRadius.circular(12)),
                    child: const Icon(Icons.monetization_on, color: Color(0xFF1B5E20), size: 28),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("New Order Request", style: TextStyle(color: Colors.grey, fontSize: 12)),
                        const SizedBox(height: 4),
                        Text(order['product_name'] ?? 'Unknown Product', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                        const SizedBox(height: 4),
                        Text("from ${order['buyer_name'] ?? 'Anonymous'}", style: TextStyle(color: Colors.grey[600], fontSize: 14)),
                        const SizedBox(height: 4),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(4)),
                          child: const Text("10 kg", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                        )
                      ],
                    ),
                  ),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                       Text("\$${order['amount']?.toStringAsFixed(0)}", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 20, color: Color(0xFF1B5E20))),
                       const SizedBox(height: 4),
                       Container(
                         padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                         decoration: BoxDecoration(color: Colors.orange[100], borderRadius: BorderRadius.circular(4)),
                         child: const Text("Action Required", style: TextStyle(fontSize: 10, color: Colors.orange, fontWeight: FontWeight.bold)),
                       )
                    ],
                  )
                ],
              ),
              const SizedBox(height: 20),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 12),
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey[200]!),
                  borderRadius: BorderRadius.circular(8)
                ),
                child: const Text("Tap to Review Decision", style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF1B5E20))),
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHistoryCard(dynamic order) {
    // ... Simplified card for history
    final status = order['status'];
    Color statusColor = status == 'CONFIRMED' ? Colors.green : (status == 'REJECTED' ? Colors.red : Colors.grey);
    
    return Card(
      elevation: 0,
      color: Colors.white,
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12), side: BorderSide(color: Colors.grey[200]!)),
      child: ListTile(
        onTap: () => _showDecisionSheet(order),
        leading: Icon(
          status == 'CONFIRMED' ? Icons.check_circle : (status == 'REJECTED' ? Icons.cancel : Icons.info),
          color: statusColor
        ),
        title: Text(order['product_name'] ?? ""),
        subtitle: Text(DateFormat('MMM dd, yyyy').format(DateTime.now())), // Mock date for now
        trailing: Text(status, style: TextStyle(fontWeight: FontWeight.bold, color: statusColor)),
      ),
    );
  }
  
  // ignore: unused_element
  void _showDecisionSheet(dynamic order) {
      showModalBottomSheet(
        context: context, 
        isScrollControlled: true,
        backgroundColor: Colors.transparent,
        builder: (_) => _DecisionSheet(order: order, onAction: (action) => _handleAction(order['id'], action))
      );
  }

  Future<void> _handleAction(int orderId, String action) async {
       Navigator.pop(context); // Close sheet
      try {
        if (action == 'ACCEPT') {
          await widget.apiClient.acceptOrder(orderId);
           if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Order Accepted! 🚀")));
        } else {
          await widget.apiClient.rejectOrder(orderId);
           if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Order Rejected.")));
        }
        _fetchSales(); // Refresh UI
      } catch (e) {
          if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Action failed.")));
      }
  }
}

// Separate widget for the Bottom Sheet to keep things clean
class _DecisionSheet extends StatelessWidget {
  final dynamic order;
  final Function(String) onAction;

  const _DecisionSheet({required this.order, required this.onAction});

  @override
  Widget build(BuildContext context) {
    final bool isActionable = ['PENDING', 'SECURED'].contains(order['status']);

    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24))
      ),
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(
            child: Container(width: 40, height: 4, decoration: BoxDecoration(color: Colors.grey[300], borderRadius: BorderRadius.circular(2))),
          ),
          const SizedBox(height: 24),
          Text(isActionable ? "Review Order Request" : "Order Details", style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          
          _buildInfoRow(Icons.person, "Buyer", order['buyer_name'] ?? "Unknown"),
          const SizedBox(height: 16),
          _buildInfoRow(Icons.inventory_2, "Items", order['product_name']),
          const SizedBox(height: 16),
          _buildInfoRow(Icons.scale, "Volume", "10 kg"), // Hardcoded for MVP
          const SizedBox(height: 16),
          _buildInfoRow(Icons.monetization_on, "Total Value", "\$${order['amount']}"),
          
          const SizedBox(height: 32),
          
          if (isActionable) ...[
              const Text("Risk Analysis", style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: Colors.green[50], borderRadius: BorderRadius.circular(8)),
                child: const Row(children: [Icon(Icons.shield, color: Colors.green, size: 20), SizedBox(width: 8), Text("Trusted Buyer (Score 9.8/10)", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold))]),
              ),
              const SizedBox(height: 32),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () => onAction('REJECT'),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        foregroundColor: Colors.red,
                        side: const BorderSide(color: Colors.red)
                      ),
                      child: const Text("Decline Deal"),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () => onAction('ACCEPT'),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        backgroundColor: const Color(0xFF1B5E20),
                        foregroundColor: Colors.white,
                        elevation: 0
                      ),
                      child: const Text("Confirm & Ship"),
                    ),
                  ),
                ],
              ),
          ] else ...[
             Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                    color: order['status'] == 'CONFIRMED' ? Colors.green[50] : Colors.red[50],
                    borderRadius: BorderRadius.circular(12)
                ),
                child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                        Icon(order['status'] == 'CONFIRMED' ? Icons.check_circle : Icons.cancel, color: order['status'] == 'CONFIRMED' ? Colors.green : Colors.red),
                        const SizedBox(width: 8),
                        Text("Order ${order['status']}", style: TextStyle(fontWeight: FontWeight.bold, color: order['status'] == 'CONFIRMED' ? Colors.green : Colors.red, fontSize: 16)),
                    ],
                ),
             ),
             
             // LOGISTICS TRACKER (Mocked for MVP)
             if (order['status'] == 'CONFIRMED') ...[
                const SizedBox(height: 24),
                const Text("Logistics Status", style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(border: Border.all(color: Colors.grey[200]!), borderRadius: BorderRadius.circular(12)),
                    child: Column(
                        children: [
                            _buildTrackerStep("FOB Validated", true, true),
                            _buildTrackerStep("Container Loaded", false, true),
                            _buildTrackerStep("In Transit", false, false),
                            _buildTrackerStep("Delivered to Buyer", false, false),
                        ],
                    ),
                )
             ]
          ],
          const SizedBox(height: 32),
        ],
      ),
    );
  }
  
  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Colors.grey),
        const SizedBox(width: 12),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
            Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          ],
        )
      ],
    );
  }

  Widget _buildTrackerStep(String label, bool isCompleted, bool isNext) {
      return Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: Row(
              children: [
                  Icon(isCompleted ? Icons.check_circle : (isNext ? Icons.radio_button_checked : Icons.radio_button_unchecked), 
                       color: isCompleted ? Colors.green : (isNext ? Colors.orange : Colors.grey), size: 20),
                  const SizedBox(width: 12),
                  Text(label, style: TextStyle(
                      color: isCompleted || isNext ? Colors.black : Colors.grey,
                      fontWeight: isNext ? FontWeight.bold : FontWeight.normal
                  ))
              ],
          ),
      );
  }
}

// Mock DateFormat
class DateFormat {
  final String formatStr;
  DateFormat(this.formatStr);
  String format(DateTime dt) => "${dt.year}-${dt.month}-${dt.day}";
}
