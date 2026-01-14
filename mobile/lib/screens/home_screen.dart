import 'package:flutter/material.dart';
import 'camera_screen.dart';
import '../core/api_client.dart';
import 'product_detail_screen.dart';
import 'sales_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiClient _apiClient = ApiClient();
  List<dynamic> _products = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchProducts();
  }

  Future<void> _fetchProducts() async {
      setState(() => _isLoading = true);
      final products = await _apiClient.getProducts();
      setState(() {
          _products = products;
          _isLoading = false;
      });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      appBar: AppBar(
        title: const Text('My Harvests'),
        backgroundColor: Colors.white,
        elevation: 0,
        actions: [
            IconButton(icon: const Icon(Icons.refresh), onPressed: _fetchProducts)
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const UserAccountsDrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF1B5E20)),
              accountName: Text("Coopérative Taroka"),
              accountEmail: Text("+261 34 05 123 45"),
              currentAccountPicture: CircleAvatar(
                backgroundColor: Colors.white,
                child: Text("T", style: TextStyle(fontSize: 24.0, color: Color(0xFF1B5E20))),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.monetization_on, color: Colors.green),
              title: const Text('Sales Dashboard'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(
                  builder: (_) => SalesScreen(apiClient: _apiClient)
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.dashboard),
              title: const Text('My Harvests'),
              onTap: () {
                Navigator.pop(context); // Close drawer
              },
            ),
            ListTile(
              leading: const Icon(Icons.qr_code_scanner),
              title: const Text('Scan New Batch'),
              onTap: () async {
                Navigator.pop(context); // Close drawer
                final result = await Navigator.push(
                    context, 
                    MaterialPageRoute(builder: (_) => const CameraScreen())
                );
                if (result == true) {
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Produce Published Successfully! 🚀"))
                      );
                    }
                    _fetchProducts();
                }
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.logout, color: Colors.red),
              title: const Text('Logout', style: TextStyle(color: Colors.red)),
              onTap: () {
                 Navigator.pop(context);
                 Navigator.pushReplacementNamed(context, '/login');
              },
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
            // Navigate to Camera
            final result = await Navigator.push(
                context, 
                MaterialPageRoute(builder: (_) => const CameraScreen())
            );
            if (result == true) {
                ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text("Produce Published Successfully! 🚀"))
                );
                _fetchProducts(); // Refresh list after upload
            }
        },
        backgroundColor: const Color(0xFF1B5E20),
        foregroundColor: Colors.white,
        icon: const Icon(Icons.camera_alt),
        label: const Text("Scan Vanilla"),
      ),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : ListView(
            padding: const EdgeInsets.all(16),
            children: [
                _buildStatCard(context),
                const SizedBox(height: 24),
                const Text("Recent Batches", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                if (_products.isEmpty)
                    const Center(child: Text("No harvests yet. Start scanning!", style: TextStyle(color: Colors.grey))),
                
                ..._products.map((p) => _buildProductCard(p)).toList().reversed, // Show newest first (naive reverse)
            ],
        ),
    );
  }

  Widget _buildStatCard(BuildContext context) {
      // Calculate total potential earnings
      // double total = _products.fold(0, (sum, item) => sum + (item['price_fob'] as num).toDouble());
      
      return Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [Color(0xFF1B5E20), Color(0xFF2E7D32)]),
              borderRadius: BorderRadius.circular(16),
              boxShadow: [BoxShadow(color: Colors.green.withOpacity(0.3), blurRadius: 10, offset: const Offset(0, 4))]
          ),
          child: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                  Text("Total Potential Value", style: TextStyle(color: Colors.white70)),
                  SizedBox(height: 8),
                  Text("\$ 14,200", style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)), // Mocked total for MVP
                  SizedBox(height: 8),
                  Row(
                      children: [
                          Icon(Icons.trending_up, color: Colors.lightGreenAccent, size: 16),
                          SizedBox(width: 4),
                          Text("+ One new batch added", style: TextStyle(color: Colors.lightGreenAccent))
                      ],
                  )
              ],
          ),
      );
  }

  Widget _buildProductCard(Map<String, dynamic> product) {
      final String title = product['name'] ?? 'Unknown Product';
      final String subtitle = "${product['quantity_available'] ?? 500} kg • ${product['price_fob']} \$/kg";
      final String status = product['status'] ?? 'PENDING';
      final int id = product['id'];

      return Card(
          margin: const EdgeInsets.only(bottom: 12),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: ListTile(
              onTap: () {
                Navigator.push(context, MaterialPageRoute(
                    builder: (_) => ProductDetailScreen(product: product)
                ));
              },
              leading: Container(
                  width: 50, height: 50,
                  decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(8)),
                  child: const Icon(Icons.inventory_2, color: Colors.grey),
              ),
              title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text(subtitle),
              trailing: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                          color: status == "SECURED" ? Colors.orange[100] : Colors.green[100],
                          borderRadius: BorderRadius.circular(8)
                      ),
                      child: Text(status, style: TextStyle(
                          color: status == "SECURED" ? Colors.orange[800] : Colors.green[800],
                          fontSize: 12, fontWeight: FontWeight.bold
                      )),
                  ),
                  if (status != "SECURED") 
                    IconButton(
                      icon: const Icon(Icons.delete_outline, color: Colors.red),
                      onPressed: () => _confirmDelete(id, title), 
                    )
                ],
              ),
          ),
      );
  }

  Future<void> _confirmDelete(int id, String productName) {
    return showDialog(context: context, builder: (ctx) => AlertDialog(
       title: const Text("Withdraw Batch?"),
       content: Text("Are you sure you want to remove $productName from marketplace?"),
       actions: [
         TextButton(onPressed: () => Navigator.pop(ctx), child: const Text("Cancel")),
         TextButton(onPressed: () async { 
           Navigator.pop(ctx); // Close dialog
           try {
             await _apiClient.deleteProduct(id);
             ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("$productName withdrawn.")));
             _fetchProducts(); // Refresh list
           } catch (e) {
             ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Failed to withdraw produt.")));
           }
         }, child: const Text("Withdraw", style: TextStyle(color: Colors.red))),
       ]
    ));
  }
}
