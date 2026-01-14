import 'package:flutter/material.dart';

class ProductDetailScreen extends StatelessWidget {
  final Map<String, dynamic> product;

  const ProductDetailScreen({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    // Extract data with safe defaults
    final String name = product['name'] ?? 'Unknown Product';
    final double price = (product['price_fob'] as num?)?.toDouble() ?? 0.0;
    final double moisture = (product['moisture_content'] as num?)?.toDouble() ?? 0.0;
    final double vanillin = (product['vanillin_content'] as num?)?.toDouble() ?? 0.0;
    final int quantity = product['quantity_available'] ?? 500;
    final String status = product['status'] ?? 'PENDING';
    final String imageUrl = product['image_url'] ?? 'https://placehold.co/600x400';

    return Scaffold(
      appBar: AppBar(
        title: const Text("Batch Details"),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black),
        titleTextStyle: const TextStyle(color: Colors.black, fontSize: 20, fontWeight: FontWeight.bold),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Image Header
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.network(
                imageUrl, 
                height: 200, 
                width: double.infinity, 
                fit: BoxFit.cover,
                errorBuilder: (ctx, err, stack) => Container(
                  height: 200, 
                  color: Colors.grey[300], 
                  child: const Center(child: Icon(Icons.broken_image, size: 50, color: Colors.grey))
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Header Info
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                 Expanded(
                   child: Text(
                    name, 
                    style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20))
                   ),
                 ),
                 Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                        color: status == "SECURED" ? Colors.orange[100] : Colors.green[100],
                        borderRadius: BorderRadius.circular(20)
                    ),
                    child: Text(status, style: TextStyle(
                        color: status == "SECURED" ? Colors.orange[800] : Colors.green[800],
                        fontWeight: FontWeight.bold
                    )),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text("Batch ID: #${product['id']}", style: const TextStyle(color: Colors.grey)),

            const SizedBox(height: 32),
            
            // Quality Metrics
            const Text("Quality Metrics", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Row(
              children: [
                _buildMetricCard(Icons.water_drop, "Moisture", "${moisture.toStringAsFixed(1)}%"),
                const SizedBox(width: 16),
                _buildMetricCard(Icons.science, "Vanillin", "${vanillin.toStringAsFixed(1)}%"),
              ],
            ),

            const SizedBox(height: 32),
             _buildDetailRow(Icons.monetization_on, "FOB Price", "\$ ${price.toStringAsFixed(2)} / kg"),
             const SizedBox(height: 16),
             _buildDetailRow(Icons.inventory, "Available Stock", "$quantity kg"), 
             const SizedBox(height: 16),
             _buildDetailRow(Icons.location_on, "Region", "SAVA Region, Madagascar"), // Mocked for now if specific field missing
             const SizedBox(height: 16),
             _buildDetailRow(Icons.calendar_today, "Harvest Date", "Oct 15, 2025"), // Mocked
 
             if (status == "SECURED" || status == "CONFIRMED") ...[
                const SizedBox(height: 32),
                 Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(color: Colors.green[50], borderRadius: BorderRadius.circular(12), border: Border.all(color: Colors.green[200]!)),
                    child: Column(
                        children: [
                            const Text("This batch has been sold/secured!", style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 8),
                            const Text("Check Sales Dashboard for order details and logistics.", textAlign: TextAlign.center, style: TextStyle(fontSize: 12, color: Colors.grey)),
                        ],
                    ),
                 )
             ],

            const SizedBox(height: 48),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () => Navigator.pop(context), 
                icon: const Icon(Icons.arrow_back),
                label: const Text("Back to Dashboard"),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  side: const BorderSide(color: Color(0xFF1B5E20)),
                  foregroundColor: const Color(0xFF1B5E20)
                ),
              ),
            )

          ],
        ),
      ),
    );
  }

  Widget _buildMetricCard(IconData icon, String label, String value) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.grey.shade200),
          boxShadow: [BoxShadow(color: Colors.grey.shade100, blurRadius: 4, offset: const Offset(0, 2))]
        ),
        child: Column(
          children: [
            Icon(icon, color: const Color(0xFF1B5E20), size: 28),
            const SizedBox(height: 8),
            Text(label, style: const TextStyle(color: Colors.grey, fontSize: 12)),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: Colors.green[50], borderRadius: BorderRadius.circular(8)),
          child: Icon(icon, color: const Color(0xFF1B5E20), size: 20),
        ),
        const SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(color: Colors.grey, fontSize: 12)),
            Text(value, style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 16)),
          ],
        )
      ],
    );
  }
}
