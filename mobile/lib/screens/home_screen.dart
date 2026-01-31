import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'camera_screen.dart';
import '../core/api_client.dart';
import '../core/theme.dart';
import 'product_detail_screen.dart';
import 'sales_screen.dart';
import 'pricing_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiClient _apiClient = ApiClient();
  List<dynamic> _products = [];
  bool _isLoading = true;
  Map<String, dynamic>? _producerProfile;  // NEW: Producer profile data

  @override
  void initState() {
    super.initState();
    _fetchProducts();
    _loadProducerProfile();  // NEW: Load producer profile
  }

  Future<void> _fetchProducts() async {
      setState(() => _isLoading = true);
      final products = await _apiClient.getProducts();
      setState(() {
          _products = products;
          _isLoading = false;
      });
  }

  // NEW: Load producer profile from API
  Future<void> _loadProducerProfile() async {
    try {
      final profile = await _apiClient.getProducerProfile(ApiClient.currentProducerId ?? 1);
      if (mounted) {
        setState(() => _producerProfile = profile);
      }
    } catch (e) {
      print("Error loading producer profile: $e");
      // Use default values on error
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundCream,
      appBar: AppBar(
        title: Text('My Harvests', style: AppTheme.textTheme.headlineMedium),
        backgroundColor: Colors.transparent,
        elevation: 0,
        actions: [
            IconButton(icon: const Icon(Icons.refresh, color: AppTheme.primaryGreen), onPressed: _fetchProducts)
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            UserAccountsDrawerHeader(
              decoration: const BoxDecoration(
                  gradient: LinearGradient(
                      colors: [AppTheme.primaryGreen, AppTheme.darkGreen],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight
                  )
              ),
              // UPDATED: Use real producer data instead of hardcoded "Coopérative Taroka"
              accountName: Text(
                _producerProfile?['name'] ?? 'Loading...',
                style: GoogleFonts.playfairDisplay(fontWeight: FontWeight.bold),
              ),
              accountEmail: Text(_producerProfile?['phone'] ?? ''),
              currentAccountPicture: CircleAvatar(
                backgroundColor: Colors.white,
                child: Text(
                  _producerProfile?['name']?.substring(0, 1).toUpperCase() ?? 'P',
                  style: const TextStyle(fontSize: 24.0, color: AppTheme.primaryGreen),
                ),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.monetization_on, color: AppTheme.primaryGreen),
              title: const Text('Sales Dashboard'),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(
                  builder: (_) => SalesScreen(apiClient: _apiClient)
                ));
              },
            ),
            // NEW: Profile menu item
            ListTile(
              leading: const Icon(Icons.person, color: AppTheme.primaryGreen),
              title: const Text('Mon Profil'),
              onTap: () async {
                Navigator.pop(context);
                final result = await Navigator.pushNamed(context, '/profile');
                // Reload profile if updated
                if (result == true) {
                  _loadProducerProfile();
                }
              },
            ),
            ListTile(
              leading: const Icon(Icons.price_change, color: Colors.blue),
              title: const Text('Gestion des Tarifs'),
              subtitle: const Text('Paliers dégressifs', style: TextStyle(fontSize: 11)),
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context, MaterialPageRoute(
                  builder: (_) => PricingScreen(apiClient: _apiClient)
                ));
              },
            ),
            ListTile(
              leading: const Icon(Icons.dashboard),
              title: const Text('My Harvests'),
              selected: true,
              selectedTileColor: AppTheme.primaryGreen.withOpacity(0.1),
              onTap: () {
                Navigator.pop(context); // Close drawer
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.logout, color: AppTheme.errorRed),
              title: const Text('Logout', style: TextStyle(color: AppTheme.errorRed)),
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
                    const SnackBar(content: Text("Produce Published Successfully! 🚀"), backgroundColor: AppTheme.successGreen)
                );
                _fetchProducts(); // Refresh list after upload
            }
        },
        backgroundColor: AppTheme.accentGold,
        foregroundColor: Colors.black,
        icon: const Icon(Icons.camera_alt),
        label: const Text("SCAN VANILLA", style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.0)),
      ),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator(color: AppTheme.primaryGreen))
        : RefreshIndicator(
            onRefresh: _fetchProducts,
            color: AppTheme.primaryGreen,
            child: ListView(
                padding: const EdgeInsets.all(20),
                children: [
                    _buildStatCard(context),
                    const SizedBox(height: 32),
                    Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                            Text("Recent Batches", style: AppTheme.textTheme.headlineMedium),
                            Text("${_products.length} Items", style: AppTheme.textTheme.bodyMedium),
                        ],
                    ),
                    const SizedBox(height: 16),
                    if (_products.isEmpty)
                        const Center(
                            child: Padding(
                              padding: EdgeInsets.all(48.0),
                              child: Text("No harvests yet.\nStart scanning your vanilla!", textAlign: TextAlign.center, style: TextStyle(color: Colors.grey)),
                            )
                        ),
                    
                    ..._products.map((p) => _buildProductCard(p)).toList().reversed, // Show newest first (naive reverse)
                    const SizedBox(height: 80), // Fab space
                ],
            ),
        ),
    );
  }

  Widget _buildStatCard(BuildContext context) {
      // Calculate total potential earnings
      double total = _products.fold(0, (sum, item) {
          final double price = (item['price_fob'] as num?)?.toDouble() ?? 0.0;
          final int quantity = item['quantity_available'] ?? 500;
          return sum + (price * quantity);
      });
      
      return Container(
          padding: const EdgeInsets.all(24),
          decoration: BoxDecoration(
              gradient: const LinearGradient(
                  colors: [AppTheme.primaryGreen, Color(0xFF2E7D32)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight
              ),
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                  BoxShadow(color: AppTheme.primaryGreen.withOpacity(0.3), blurRadius: 20, offset: const Offset(0, 10))
              ]
          ),
          child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                  Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                          const Text("Total Potential Value", style: TextStyle(color: Colors.white70)),
                          Container(
                              padding: const EdgeInsets.all(8),
                              decoration: BoxDecoration(color: Colors.white.withOpacity(0.2), borderRadius: BorderRadius.circular(12)),
                              child: const Icon(Icons.trending_up, color: Colors.white, size: 20),
                          )
                      ],
                  ),
                  const SizedBox(height: 16),
                  Text("\$ ${total.toStringAsFixed(0)}", style: GoogleFonts.playfairDisplay(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  const Text("Estimated based on FOB prices", style: TextStyle(color: Colors.white54, fontSize: 12))
              ],
          ),
      );
  }

  Widget _buildProductCard(Map<String, dynamic> product) {
      final String title = product['name'] ?? 'Unknown Product';
      final String grade = product['grade'] ?? 'A';
      final int quantity = product['quantity_available'] ?? 500;
      final double price = (product['price_fob'] as num?)?.toDouble() ?? 0.0;
      final String status = product['status'] ?? 'PENDING';
      final int id = product['id'];

      final bool isSecured = status == "SECURED" || status == "CONFIRMED";

      return Container(
          margin: const EdgeInsets.only(bottom: 16),
          decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              boxShadow: [
                  BoxShadow(color: Colors.grey.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))
              ],
              border: Border.all(color: Colors.grey.withOpacity(0.1))
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              borderRadius: BorderRadius.circular(20),
              onTap: () {
                Navigator.push(context, MaterialPageRoute(
                    builder: (_) => ProductDetailScreen(product: product)
                ));
              },
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                    children: [
                        // Icon / Image Placeholder
                        Container(
                            width: 60, height: 60,
                            decoration: BoxDecoration(color: AppTheme.backgroundCream, borderRadius: BorderRadius.circular(16)),
                            child: Center(
                                child: Text(grade, style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppTheme.primaryGreen.withOpacity(0.5)))
                            ),
                        ),
                        const SizedBox(width: 16),
                        // Info
                        Expanded(
                            child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                    Text(title, style: AppTheme.textTheme.headlineMedium?.copyWith(fontSize: 16)),
                                    const SizedBox(height: 4),
                                    Text("$quantity kg  •  \$ $price / kg", style: TextStyle(color: AppTheme.textGrey)),
                                ],
                            ),
                        ),
                        // Status Badge
                        Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                            decoration: BoxDecoration(
                                color: isSecured ? AppTheme.accentGold.withOpacity(0.2) : const Color(0xFFE8F5E9),
                                borderRadius: BorderRadius.circular(12)
                            ),
                            child: Text(
                                status, 
                                style: TextStyle(
                                    color: isSecured ? const Color(0xFF8D6E63) : AppTheme.primaryGreen,
                                    fontSize: 10, 
                                    fontWeight: FontWeight.bold
                                )
                            ),
                        ),
                    ],
                ),
              ),
            ),
          ),
      );
  }
}
