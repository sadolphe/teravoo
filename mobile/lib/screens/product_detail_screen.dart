import 'package:flutter/material.dart';
import 'package:mobile/core/api_client.dart';
import '../core/theme.dart';
import 'package:mobile/widgets/price_tier_widget.dart';

class ProductDetailScreen extends StatefulWidget {
  final Map<String, dynamic> product;

  const ProductDetailScreen({super.key, required this.product});

  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  final ApiClient _api = ApiClient();
  Map<String, dynamic>? _pricingInfo;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadPricingInfo();
  }

  Future<void> _loadPricingInfo() async {
    final productId = widget.product['id'] as int?;
    if (productId != null) {
      final info = await _api.getProductPriceTiers(productId);
      if (mounted) {
        setState(() {
          _pricingInfo = info;
          _isLoading = false;
        });
      }
    } else {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    // Extract data with safe defaults
    final String name = widget.product['name'] ?? 'Unknown Product';
    final String grade = widget.product['grade'] ?? 'A';
    final double price = (widget.product['price_fob'] as num?)?.toDouble() ?? 0.0;
    final double moisture = (widget.product['moisture_content'] as num?)?.toDouble() ?? 0.0;
    final double vanillin = (widget.product['vanillin_content'] as num?)?.toDouble() ?? 0.0;
    final int quantity = widget.product['quantity_available'] ?? 500;
    final String status = widget.product['status'] ?? 'PENDING';
    final String imageUrl = widget.product['image_url'] ?? 'https://placehold.co/600x400';
    final int productId = widget.product['id'] ?? 0;

    // Pricing info
    final List<dynamic> tiers = _pricingInfo?['tiers'] ?? [];
    final double moqKg = (_pricingInfo?['moq_kg'] as num?)?.toDouble() ?? 1.0;
    final String pricingMode = _pricingInfo?['pricing_mode'] ?? 'SINGLE';
    
    final bool isSecured = status == "SECURED" || status == "CONFIRMED";

    return Scaffold(
      backgroundColor: AppTheme.backgroundCream,
      body: CustomScrollView(
        slivers: [
            SliverAppBar(
                expandedHeight: 300,
                pinned: true,
                backgroundColor: AppTheme.backgroundCream,
                flexibleSpace: FlexibleSpaceBar(
                    background: Stack(
                        fit: StackFit.expand,
                        children: [
                            Image.network(imageUrl, fit: BoxFit.cover),
                            Container(
                                decoration: BoxDecoration(
                                    gradient: LinearGradient(
                                        begin: Alignment.topCenter,
                                        end: Alignment.bottomCenter,
                                        colors: [Colors.transparent, Colors.black.withOpacity(0.7)]
                                    )
                                ),
                            ),
                            Positioned(
                                bottom: 20,
                                left: 20,
                                right: 20,
                                child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                        Container(
                                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                            decoration: BoxDecoration(
                                                color: isSecured ? AppTheme.accentGold : AppTheme.primaryGreen,
                                                borderRadius: BorderRadius.circular(20)
                                            ),
                                            child: Text(
                                                isSecured ? "SECURED" : "AVAILABLE", 
                                                style: TextStyle(
                                                    color: isSecured ? Colors.black : Colors.white, 
                                                    fontWeight: FontWeight.bold, fontSize: 12
                                                )
                                            ),
                                        ),
                                        const SizedBox(height: 8),
                                        Text(name, style: AppTheme.textTheme.displayMedium?.copyWith(color: Colors.white)),
                                        Text("Batch #$productId  •  Grade $grade", style: const TextStyle(color: Colors.white70)),
                                    ],
                                ),
                            )
                        ],
                    ),
                ),
                actions: [
                    Container(
                        margin: const EdgeInsets.only(right: 16),
                        decoration: const BoxDecoration(color: Colors.white24, shape: BoxShape.circle),
                        child: IconButton(
                            icon: const Icon(Icons.edit, color: Colors.white),
                            onPressed: () => _showEditDialog(context),
                        ),
                    )
                ],
            ),
            
            SliverToBoxAdapter(
                child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                            Text("Quality Metrics", style: AppTheme.textTheme.headlineMedium),
                            const SizedBox(height: 16),
                            Row(
                                children: [
                                    _buildMetricCard(Icons.water_drop_outlined, "Moisture", "${moisture.toStringAsFixed(1)}%"),
                                    const SizedBox(width: 16),
                                    _buildMetricCard(Icons.science_outlined, "Vanillin", "${vanillin.toStringAsFixed(1)}%"),
                                ],
                            ),
                            
                            const SizedBox(height: 32),
                            
                            // Pricing Section
                            Text("Pricing & Stock", style: AppTheme.textTheme.headlineMedium),
                            const SizedBox(height: 16),
                            Container(
                                padding: const EdgeInsets.all(24),
                                decoration: BoxDecoration(
                                    color: Colors.white,
                                    borderRadius: BorderRadius.circular(20),
                                    border: Border.all(color: Colors.grey.withOpacity(0.1))
                                ),
                                child: Column(
                                    children: [
                                         if (_isLoading)
                                            const Center(child: CircularProgressIndicator())
                                        else if (tiers.isNotEmpty && pricingMode != 'SINGLE')
                                            PriceTierWidget(
                                                productId: productId,
                                                basePriceFob: price,
                                                tiers: tiers,
                                                moqKg: moqKg,
                                                quantityAvailable: quantity,
                                                onPriceCalculated: (qty, pricePerKg, total) {},
                                            )
                                        else ...[
                                            _buildDetailRow(Icons.monetization_on, "FOB Price", "\$ ${price.toStringAsFixed(2)} / kg"),
                                        ],
                                        const Padding(padding: EdgeInsets.symmetric(vertical: 16), child: Divider()),
                                        _buildDetailRow(Icons.inventory_2_outlined, "Available Stock", "$quantity kg"),
                                        const SizedBox(height: 16),
                                        _buildDetailRow(Icons.location_on_outlined, "Origin", widget.product['origin'] ?? "SAVA Region, Madagascar"),
                                        const SizedBox(height: 16),
                                        _buildDetailRow(Icons.calendar_today_outlined, "Harvest Date", widget.product['harvest_date'] ?? "Oct 15, 2025"),
                                    ],
                                ),
                            ),
                            
                             if (isSecured) ...[
                                const SizedBox(height: 32),
                                Container(
                                    width: double.infinity,
                                    padding: const EdgeInsets.all(20),
                                    decoration: BoxDecoration(
                                        color: AppTheme.primaryGreen.withOpacity(0.05),
                                        borderRadius: BorderRadius.circular(20),
                                        border: Border.all(color: AppTheme.primaryGreen.withOpacity(0.2))
                                    ),
                                    child: Column(
                                    children: [
                                        const Icon(Icons.check_circle, color: AppTheme.primaryGreen, size: 32),
                                        const SizedBox(height: 8),
                                        Text("Batch Secured", style: AppTheme.textTheme.headlineMedium?.copyWith(fontSize: 18, color: AppTheme.primaryGreen)),
                                        const SizedBox(height: 8),
                                        const Text("Check Sales Dashboard for logistics details.", textAlign: TextAlign.center, style: TextStyle(color: AppTheme.textGrey)),
                                    ],
                                    ),
                                )
                            ],
                            
                            const SizedBox(height: 48),
                        ],
                    ),
                ),
            )
        ],
      ),
    );
  }

  Widget _buildMetricCard(IconData icon, String label, String value) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
            color: Colors.white, 
            borderRadius: BorderRadius.circular(20), 
            border: Border.all(color: Colors.grey.withOpacity(0.1)),
            boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 4))]
        ),
        child: Column(
          children: [
            Icon(icon, color: AppTheme.primaryGreen, size: 28),
            const SizedBox(height: 8),
            Text(label, style: const TextStyle(color: AppTheme.textGrey, fontSize: 12)),
            const SizedBox(height: 4),
            Text(value, style: AppTheme.textTheme.headlineMedium?.copyWith(fontSize: 20)),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: AppTheme.backgroundCream, borderRadius: BorderRadius.circular(12)),
          child: Icon(icon, color: AppTheme.primaryGreen, size: 20),
        ),
        const SizedBox(width: 16),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(color: AppTheme.textGrey, fontSize: 12)),
            Text(value, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16)),
          ],
        )
      ],
    );
  }

  void _showEditDialog(BuildContext context) {
      final nameController = TextEditingController(text: widget.product['name']);
      final priceController = TextEditingController(text: widget.product['price_fob'].toString());
      final moistureController = TextEditingController(text: widget.product['moisture_content'].toString());
      final vanillinController = TextEditingController(text: widget.product['vanillin_content'].toString());
      String selectedGrade = widget.product['grade'] ?? "A";
      final List<String> grades = ["A", "B", "C", "D", "SPLITS", "CUTS", "VRAC"];

      showDialog(context: context, builder: (ctx) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          title: const Text("Edit Batch Details"),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(controller: nameController, decoration: const InputDecoration(labelText: "Batch Name")),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                    value: grades.contains(selectedGrade) ? selectedGrade : "A",
                    decoration: const InputDecoration(labelText: "Grade"),
                    items: grades.map((g) => DropdownMenuItem(value: g, child: Text("Grade $g"))).toList(),
                    onChanged: (val) => setState(() => selectedGrade = val!)
                ),
                const SizedBox(height: 12),
                TextField(controller: priceController, decoration: const InputDecoration(labelText: "Price FOB (\$ / kg)"), keyboardType: TextInputType.number),
                const SizedBox(height: 12),
                Row(
                  children: [
                    Expanded(child: TextField(controller: moistureController, decoration: const InputDecoration(labelText: "Moisture %"), keyboardType: TextInputType.number)),
                    const SizedBox(width: 8),
                    Expanded(child: TextField(controller: vanillinController, decoration: const InputDecoration(labelText: "Vanillin %"), keyboardType: TextInputType.number)),
                  ],
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
                onPressed: () => Navigator.pop(ctx), 
                child: const Text("Cancel", style: TextStyle(color: AppTheme.textGrey))
            ),
            ElevatedButton(
                onPressed: () async {
                    final updatedData = {
                        "name": nameController.text,
                        "grade": selectedGrade,
                        "price_fob": double.tryParse(priceController.text) ?? 0.0,
                        "moisture_content": double.tryParse(moistureController.text),
                        "vanillin_content": double.tryParse(vanillinController.text),
                    };
                    
                    Navigator.pop(ctx);
                    
                    final result = await _api.updateProduct(widget.product['id'], updatedData);
                    if (result != null) {
                        if (mounted) {
                            setState(() {
                                widget.product.addAll(result); // Update local state
                            });
                            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Batch updated successfully!"), backgroundColor: AppTheme.successGreen));
                        }
                    } else {
                        if (mounted) ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Failed to update."), backgroundColor: AppTheme.errorRed));
                    }

            }, child: const Text("Save"))
          ],
        ),
      ));
  }
}
