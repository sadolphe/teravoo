import 'package:flutter/material.dart';
import 'package:mobile/core/api_client.dart';

// Mock producer ID for MVP
// Mock producer ID removed in favor of ApiClient.currentProducerId

class PricingScreen extends StatefulWidget {
  final ApiClient apiClient;

  const PricingScreen({super.key, required this.apiClient});

  @override
  State<PricingScreen> createState() => _PricingScreenState();
}

class _PricingScreenState extends State<PricingScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  List<dynamic> _products = [];
  List<dynamic> _templates = [];
  bool _isLoading = true;
  dynamic _selectedProduct;
  Map<String, dynamic>? _productPricing;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _loadData();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    try {
      final products = await widget.apiClient.getProducts();
      final templates = await widget.apiClient.getProducerTemplates(null); // Defaults to currentProducerId
      setState(() {
        _products = products;
        _templates = templates;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erreur: $e')),
        );
      }
    }
  }

  Future<void> _selectProduct(dynamic product) async {
    setState(() {
      _selectedProduct = product;
      _productPricing = null;
    });

    final pricing = await widget.apiClient.getProductPriceTiers(product['id']);
    if (mounted) {
      setState(() => _productPricing = pricing);
    }
  }

  String _getPricingModeLabel(String? mode) {
    switch (mode) {
      case 'TIERED':
        return 'Paliers';
      case 'TEMPLATE':
        return 'Template';
      default:
        return 'Prix unique';
    }
  }

  Color _getPricingModeColor(String? mode) {
    switch (mode) {
      case 'TIERED':
        return Colors.green;
      case 'TEMPLATE':
        return Colors.blue;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text('Gestion des Tarifs', style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black),
        bottom: TabBar(
          controller: _tabController,
          labelColor: const Color(0xFF1B5E20),
          unselectedLabelColor: Colors.grey,
          indicatorColor: const Color(0xFF1B5E20),
          tabs: const [
            Tab(text: "Mes Produits"),
            Tab(text: "Mes Templates"),
          ],
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(
              controller: _tabController,
              children: [
                _buildProductsTab(),
                _buildTemplatesTab(),
              ],
            ),
    );
  }

  Widget _buildProductsTab() {
    return Row(
      children: [
        // Products List (1/3 width on tablet, full on phone)
        Expanded(
          flex: MediaQuery.of(context).size.width > 600 ? 1 : 2,
          child: Container(
            color: Colors.white,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Text(
                    "Sélectionner un produit",
                    style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey[700]),
                  ),
                ),
                Expanded(
                  child: _products.isEmpty
                      ? const Center(child: Text("Aucun produit", style: TextStyle(color: Colors.grey)))
                      : ListView.builder(
                          itemCount: _products.length,
                          itemBuilder: (context, index) {
                            final product = _products[index];
                            final isSelected = _selectedProduct?['id'] == product['id'];
                            final mode = product['pricing_mode'] as String?;

                            return Container(
                              margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                              decoration: BoxDecoration(
                                color: isSelected ? const Color(0xFF1B5E20).withValues(alpha: 0.1) : null,
                                borderRadius: BorderRadius.circular(12),
                                border: isSelected
                                    ? Border.all(color: const Color(0xFF1B5E20), width: 2)
                                    : Border.all(color: Colors.grey[200]!),
                              ),
                              child: ListTile(
                                onTap: () => _selectProduct(product),
                                title: Text(
                                  product['name'] ?? 'Produit',
                                  style: const TextStyle(fontWeight: FontWeight.w600),
                                  overflow: TextOverflow.ellipsis,
                                ),
                                subtitle: Text("\$${product['price_fob']}/kg"),
                                trailing: Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                  decoration: BoxDecoration(
                                    color: _getPricingModeColor(mode).withValues(alpha: 0.1),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Text(
                                    _getPricingModeLabel(mode),
                                    style: TextStyle(
                                      color: _getPricingModeColor(mode),
                                      fontSize: 11,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              ),
                            );
                          },
                        ),
                ),
              ],
            ),
          ),
        ),

        // Editor (2/3 width on tablet, hidden on phone until product selected)
        if (MediaQuery.of(context).size.width > 600 || _selectedProduct != null)
          Expanded(
            flex: 2,
            child: _selectedProduct != null
                ? _PriceTierEditorWidget(
                    product: _selectedProduct,
                    pricing: _productPricing,
                    templates: _templates,
                    apiClient: widget.apiClient,
                    onSaved: () {
                      _loadData();
                      _selectProduct(_selectedProduct);
                    },
                  )
                : Container(
                    color: Colors.grey[100],
                    child: const Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.touch_app, size: 64, color: Colors.grey),
                          SizedBox(height: 16),
                          Text(
                            "Sélectionnez un produit\npour configurer ses tarifs",
                            textAlign: TextAlign.center,
                            style: TextStyle(color: Colors.grey),
                          ),
                        ],
                      ),
                    ),
                  ),
          ),
      ],
    );
  }

  Widget _buildTemplatesTab() {
    return Column(
      children: [
        // Header with Add button
        Container(
          color: Colors.white,
          padding: const EdgeInsets.all(16),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("Templates de paliers", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  Text("Créez des templates réutilisables", style: TextStyle(color: Colors.grey[600], fontSize: 12)),
                ],
              ),
              ElevatedButton.icon(
                onPressed: () => _showCreateTemplateDialog(),
                icon: const Icon(Icons.add, size: 18),
                label: const Text("Créer"),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1B5E20),
                  foregroundColor: Colors.white,
                ),
              ),
            ],
          ),
        ),
        const Divider(height: 1),

        // Templates Grid
        Expanded(
          child: _templates.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.description_outlined, size: 64, color: Colors.grey[300]),
                      const SizedBox(height: 16),
                      Text("Aucun template", style: TextStyle(color: Colors.grey[400], fontSize: 18)),
                      const SizedBox(height: 8),
                      Text("Créez votre premier template", style: TextStyle(color: Colors.grey[400])),
                      const SizedBox(height: 24),
                      ElevatedButton(
                        onPressed: () => _showCreateTemplateDialog(),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF1B5E20),
                          foregroundColor: Colors.white,
                        ),
                        child: const Text("Créer un template"),
                      ),
                    ],
                  ),
                )
              : GridView.builder(
                  padding: const EdgeInsets.all(16),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: MediaQuery.of(context).size.width > 600 ? 3 : 2,
                    crossAxisSpacing: 12,
                    mainAxisSpacing: 12,
                    childAspectRatio: 0.85,
                  ),
                  itemCount: _templates.length,
                  itemBuilder: (context, index) => _buildTemplateCard(_templates[index]),
                ),
        ),
      ],
    );
  }

  Widget _buildTemplateCard(dynamic template) {
    final tiers = template['tiers'] as List<dynamic>? ?? [];
    final productsCount = template['products_count'] ?? 0;
    final isDefault = template['is_default'] == true;

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    template['name'] ?? 'Template',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                if (isDefault)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                    decoration: BoxDecoration(
                      color: Colors.blue[100],
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: const Text("Défaut", style: TextStyle(fontSize: 9, color: Colors.blue, fontWeight: FontWeight.bold)),
                  ),
              ],
            ),
            const SizedBox(height: 4),
            Text(
              "$productsCount produit(s)",
              style: TextStyle(color: Colors.grey[600], fontSize: 11),
            ),
            const Divider(height: 16),

            // Tiers preview
            Expanded(
              child: ListView.builder(
                physics: const NeverScrollableScrollPhysics(),
                itemCount: tiers.length.clamp(0, 4),
                itemBuilder: (context, index) {
                  final tier = tiers[index];
                  final minQty = (tier['min_quantity_kg'] as num?)?.toInt() ?? 0;
                  final maxQty = tier['max_quantity_kg'];
                  final discount = (tier['discount_percent'] as num?)?.toDouble() ?? 0;

                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          maxQty == null ? "$minQty+ kg" : "$minQty-${(maxQty as num).toInt()} kg",
                          style: TextStyle(fontSize: 11, color: Colors.grey[600]),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: discount > 0 ? Colors.green[50] : Colors.grey[100],
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            discount > 0 ? "-${discount.toStringAsFixed(0)}%" : "Base",
                            style: TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              color: discount > 0 ? Colors.green : Colors.grey,
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showCreateTemplateDialog() {
    String templateName = "";
    List<Map<String, dynamic>> tiers = [
      {'min_quantity_kg': 1, 'max_quantity_kg': 49, 'discount_percent': 0},
      {'min_quantity_kg': 50, 'max_quantity_kg': 199, 'discount_percent': 5},
      {'min_quantity_kg': 200, 'max_quantity_kg': null, 'discount_percent': 10},
    ];

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => StatefulBuilder(
        builder: (context, setSheetState) => Container(
          height: MediaQuery.of(context).size.height * 0.85,
          decoration: const BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
          ),
          child: Column(
            children: [
              // Handle
              Container(
                margin: const EdgeInsets.only(top: 12),
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(2),
                ),
              ),

              // Header
              Padding(
                padding: const EdgeInsets.all(20),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Nouveau Template", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                    IconButton(
                      onPressed: () => Navigator.pop(context),
                      icon: const Icon(Icons.close),
                    ),
                  ],
                ),
              ),

              const Divider(height: 1),

              // Content
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Name input
                      const Text("Nom du template", style: TextStyle(fontWeight: FontWeight.w600)),
                      const SizedBox(height: 8),
                      TextField(
                        onChanged: (v) => templateName = v,
                        decoration: InputDecoration(
                          hintText: "Ex: Paliers Standard",
                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        ),
                      ),

                      const SizedBox(height: 24),

                      // Tiers
                      const Text("Paliers de réduction", style: TextStyle(fontWeight: FontWeight.w600)),
                      const SizedBox(height: 8),
                      Text(
                        "Définissez des réductions en pourcentage qui s'appliqueront au prix de base de chaque produit",
                        style: TextStyle(color: Colors.grey[600], fontSize: 12),
                      ),
                      const SizedBox(height: 16),

                      ...tiers.asMap().entries.map((entry) {
                        final index = entry.key;
                        final tier = entry.value;

                        return Container(
                          margin: const EdgeInsets.only(bottom: 12),
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey[200]!),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Row(
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text("Min (kg)", style: TextStyle(fontSize: 11, color: Colors.grey)),
                                    const SizedBox(height: 4),
                                    TextField(
                                      controller: TextEditingController(text: tier['min_quantity_kg'].toString()),
                                      keyboardType: TextInputType.number,
                                      decoration: InputDecoration(
                                        isDense: true,
                                        contentPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(4)),
                                      ),
                                      onChanged: (v) {
                                        tiers[index]['min_quantity_kg'] = int.tryParse(v) ?? 0;
                                      },
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text("Max (kg)", style: TextStyle(fontSize: 11, color: Colors.grey)),
                                    const SizedBox(height: 4),
                                    TextField(
                                      controller: TextEditingController(
                                        text: tier['max_quantity_kg']?.toString() ?? '',
                                      ),
                                      keyboardType: TextInputType.number,
                                      decoration: InputDecoration(
                                        isDense: true,
                                        hintText: "∞",
                                        contentPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(4)),
                                      ),
                                      onChanged: (v) {
                                        tiers[index]['max_quantity_kg'] = v.isEmpty ? null : int.tryParse(v);
                                      },
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text("Réduction (%)", style: TextStyle(fontSize: 11, color: Colors.grey)),
                                    const SizedBox(height: 4),
                                    TextField(
                                      controller: TextEditingController(
                                        text: tier['discount_percent'].toString(),
                                      ),
                                      keyboardType: TextInputType.number,
                                      decoration: InputDecoration(
                                        isDense: true,
                                        contentPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(4)),
                                      ),
                                      onChanged: (v) {
                                        tiers[index]['discount_percent'] = int.tryParse(v) ?? 0;
                                      },
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(width: 8),
                              IconButton(
                                onPressed: tiers.length > 1
                                    ? () {
                                        setSheetState(() {
                                          tiers.removeAt(index);
                                        });
                                      }
                                    : null,
                                icon: Icon(Icons.delete_outline, color: tiers.length > 1 ? Colors.red : Colors.grey),
                                iconSize: 20,
                              ),
                            ],
                          ),
                        );
                      }),

                      // Add tier button
                      if (tiers.length < 5)
                        OutlinedButton.icon(
                          onPressed: () {
                            final last = tiers.last;
                            setSheetState(() {
                              tiers.add({
                                'min_quantity_kg': (last['max_quantity_kg'] ?? 500) + 1,
                                'max_quantity_kg': null,
                                'discount_percent': (last['discount_percent'] ?? 0) + 5,
                              });
                            });
                          },
                          icon: const Icon(Icons.add, size: 18),
                          label: const Text("Ajouter un palier"),
                          style: OutlinedButton.styleFrom(
                            foregroundColor: const Color(0xFF1B5E20),
                          ),
                        ),
                    ],
                  ),
                ),
              ),

              // Footer
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: Colors.white,
                  boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 10, offset: const Offset(0, -5))],
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: OutlinedButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text("Annuler"),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: ElevatedButton(
                        onPressed: () async {
                          if (templateName.trim().isEmpty) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text("Veuillez entrer un nom")),
                            );
                            return;
                          }

                          try {
                            await widget.apiClient.createPriceTemplate(null, { // Defaults to currentProducerId
                              'name': templateName,
                              'is_default': _templates.isEmpty,
                              'tiers': tiers,
                            });

                            if (mounted) {
                              Navigator.pop(context);
                              _loadData();
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text("Template créé avec succès!")),
                              );
                            }
                          } catch (e) {
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text("Erreur: $e")),
                              );
                            }
                          }
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF1B5E20),
                          foregroundColor: Colors.white,
                        ),
                        child: const Text("Créer"),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// Price Tier Editor Widget for a selected product
class _PriceTierEditorWidget extends StatefulWidget {
  final dynamic product;
  final Map<String, dynamic>? pricing;
  final List<dynamic> templates;
  final ApiClient apiClient;
  final VoidCallback onSaved;

  const _PriceTierEditorWidget({
    required this.product,
    required this.pricing,
    required this.templates,
    required this.apiClient,
    required this.onSaved,
  });

  @override
  State<_PriceTierEditorWidget> createState() => _PriceTierEditorWidgetState();
}

class _PriceTierEditorWidgetState extends State<_PriceTierEditorWidget> {
  late String _selectedMode;
  int? _selectedTemplateId;
  List<Map<String, dynamic>> _tiers = [];
  bool _isSaving = false;

  @override
  void initState() {
    super.initState();
    _initializeFromPricing();
  }

  @override
  void didUpdateWidget(covariant _PriceTierEditorWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.product['id'] != widget.product['id']) {
      _initializeFromPricing();
    }
  }

  void _initializeFromPricing() {
    final pricing = widget.pricing;
    _selectedMode = pricing?['pricing_mode'] ?? 'SINGLE';
    _selectedTemplateId = pricing?['template_id'];

    if (pricing?['tiers'] != null && (pricing!['tiers'] as List).isNotEmpty) {
      _tiers = (pricing['tiers'] as List).map((t) => {
        'min_quantity_kg': t['min_quantity_kg'],
        'max_quantity_kg': t['max_quantity_kg'],
        'price_per_kg': (t['price_per_kg'] as num).toDouble(),
      }).toList();
    } else {
      final basePrice = (widget.product['price_fob'] as num).toDouble();
      _tiers = [
        {'min_quantity_kg': 1, 'max_quantity_kg': 49, 'price_per_kg': basePrice},
        {'min_quantity_kg': 50, 'max_quantity_kg': 199, 'price_per_kg': basePrice * 0.95},
        {'min_quantity_kg': 200, 'max_quantity_kg': null, 'price_per_kg': basePrice * 0.90},
      ];
    }
  }

  Future<void> _save() async {
    setState(() => _isSaving = true);

    try {
      final productId = widget.product['id'] as int;

      if (_selectedMode == 'TIERED') {
        await widget.apiClient.setProductPriceTiers(productId, _tiers);
      } else {
        await widget.apiClient.updateProductPricingMode(
          productId,
          _selectedMode,
          templateId: _selectedMode == 'TEMPLATE' ? _selectedTemplateId : null,
        );
      }

      widget.onSaved();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Tarifs sauvegardés!")),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Erreur: $e")),
        );
      }
    } finally {
      setState(() => _isSaving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final basePrice = (widget.product['price_fob'] as num).toDouble();

    return Container(
      color: Colors.grey[50],
      child: Column(
        children: [
          // Product Header
          Container(
            color: Colors.white,
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: const Color(0xFF1B5E20).withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.inventory_2, color: Color(0xFF1B5E20)),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        widget.product['name'] ?? 'Produit',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      ),
                      Text(
                        "Prix de base: \$${basePrice.toStringAsFixed(2)}/kg",
                        style: TextStyle(color: Colors.grey[600], fontSize: 13),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          const Divider(height: 1),

          // Mode Selection
          Container(
            color: Colors.white,
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("Mode de tarification", style: TextStyle(fontWeight: FontWeight.w600)),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 8,
                  children: [
                    _buildModeChip('SINGLE', 'Prix unique'),
                    _buildModeChip('TIERED', 'Paliers personnalisés'),
                    if (widget.templates.isNotEmpty)
                      _buildModeChip('TEMPLATE', 'Utiliser template'),
                  ],
                ),
              ],
            ),
          ),

          const Divider(height: 1),

          // Content based on mode
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: _buildModeContent(basePrice),
            ),
          ),

          // Save Button
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 10, offset: const Offset(0, -5))],
            ),
            child: SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isSaving ? null : _save,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1B5E20),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                ),
                child: _isSaving
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text("Sauvegarder les tarifs", style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildModeChip(String mode, String label) {
    final isSelected = _selectedMode == mode;
    return ChoiceChip(
      label: Text(label),
      selected: isSelected,
      selectedColor: const Color(0xFF1B5E20).withValues(alpha: 0.2),
      labelStyle: TextStyle(
        color: isSelected ? const Color(0xFF1B5E20) : Colors.grey[700],
        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
      ),
      onSelected: (selected) {
        if (selected) {
          setState(() => _selectedMode = mode);
        }
      },
    );
  }

  Widget _buildModeContent(double basePrice) {
    switch (_selectedMode) {
      case 'SINGLE':
        return _buildSingleModeContent(basePrice);
      case 'TIERED':
        return _buildTieredModeContent(basePrice);
      case 'TEMPLATE':
        return _buildTemplateModeContent(basePrice);
      default:
        return const SizedBox.shrink();
    }
  }

  Widget _buildSingleModeContent(double basePrice) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        children: [
          const Icon(Icons.price_check, size: 48, color: Colors.grey),
          const SizedBox(height: 12),
          Text(
            "\$${basePrice.toStringAsFixed(2)}/kg",
            style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20)),
          ),
          const SizedBox(height: 8),
          Text(
            "Prix unique quelle que soit la quantité",
            style: TextStyle(color: Colors.grey[600]),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildTieredModeContent(double basePrice) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Tiers Table Header
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.grey[100],
            borderRadius: const BorderRadius.vertical(top: Radius.circular(8)),
          ),
          child: const Row(
            children: [
              Expanded(flex: 2, child: Text("Quantité", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
              Expanded(flex: 2, child: Text("Prix/kg", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
              Expanded(flex: 1, child: Text("Réduction", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
              SizedBox(width: 40),
            ],
          ),
        ),

        // Tiers
        Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: const BorderRadius.vertical(bottom: Radius.circular(8)),
            border: Border.all(color: Colors.grey[200]!),
          ),
          child: Column(
            children: [
              ..._tiers.asMap().entries.map((entry) {
                final index = entry.key;
                final tier = entry.value;
                final pricePerKg = (tier['price_per_kg'] as num).toDouble();
                final discount = ((basePrice - pricePerKg) / basePrice * 100).clamp(0, 100);

                return Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    border: Border(bottom: BorderSide(color: Colors.grey[200]!)),
                  ),
                  child: Row(
                    children: [
                      // Quantity Range
                      Expanded(
                        flex: 2,
                        child: Row(
                          children: [
                            SizedBox(
                              width: 50,
                              child: TextField(
                                controller: TextEditingController(text: tier['min_quantity_kg'].toString()),
                                keyboardType: TextInputType.number,
                                decoration: const InputDecoration(
                                  isDense: true,
                                  contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 13),
                                onChanged: (v) {
                                  setState(() {
                                    _tiers[index]['min_quantity_kg'] = int.tryParse(v) ?? 1;
                                  });
                                },
                              ),
                            ),
                            const Text(" - ", style: TextStyle(fontSize: 12)),
                            SizedBox(
                              width: 50,
                              child: TextField(
                                controller: TextEditingController(
                                  text: tier['max_quantity_kg']?.toString() ?? '',
                                ),
                                keyboardType: TextInputType.number,
                                decoration: const InputDecoration(
                                  isDense: true,
                                  hintText: "∞",
                                  contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 13),
                                onChanged: (v) {
                                  setState(() {
                                    _tiers[index]['max_quantity_kg'] = v.isEmpty ? null : int.tryParse(v);
                                  });
                                },
                              ),
                            ),
                          ],
                        ),
                      ),

                      // Price
                      Expanded(
                        flex: 2,
                        child: TextField(
                          controller: TextEditingController(text: pricePerKg.toStringAsFixed(2)),
                          keyboardType: const TextInputType.numberWithOptions(decimal: true),
                          decoration: const InputDecoration(
                            isDense: true,
                            prefixText: "\$ ",
                            contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 6),
                            border: OutlineInputBorder(),
                          ),
                          style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold),
                          onChanged: (v) {
                            setState(() {
                              _tiers[index]['price_per_kg'] = double.tryParse(v) ?? basePrice;
                            });
                          },
                        ),
                      ),

                      // Discount Display
                      Expanded(
                        flex: 1,
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: discount > 0 ? Colors.green[50] : Colors.grey[100],
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            discount > 0 ? "-${discount.toStringAsFixed(1)}%" : "Base",
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                              color: discount > 0 ? Colors.green : Colors.grey,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ),

                      // Delete button
                      SizedBox(
                        width: 40,
                        child: IconButton(
                          onPressed: _tiers.length > 1
                              ? () {
                                  setState(() {
                                    _tiers.removeAt(index);
                                  });
                                }
                              : null,
                          icon: Icon(
                            Icons.delete_outline,
                            size: 18,
                            color: _tiers.length > 1 ? Colors.red : Colors.grey,
                          ),
                        ),
                      ),
                    ],
                  ),
                );
              }),
            ],
          ),
        ),

        const SizedBox(height: 12),

        // Add tier button
        if (_tiers.length < 5)
          OutlinedButton.icon(
            onPressed: () {
              final last = _tiers.last;
              setState(() {
                _tiers.add({
                  'min_quantity_kg': (last['max_quantity_kg'] ?? 500) + 1,
                  'max_quantity_kg': null,
                  'price_per_kg': (last['price_per_kg'] as num).toDouble() * 0.95,
                });
              });
            },
            icon: const Icon(Icons.add, size: 18),
            label: const Text("Ajouter un palier"),
            style: OutlinedButton.styleFrom(
              foregroundColor: const Color(0xFF1B5E20),
            ),
          ),
      ],
    );
  }

  Widget _buildTemplateModeContent(double basePrice) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text("Sélectionner un template", style: TextStyle(fontWeight: FontWeight.w600)),
        const SizedBox(height: 12),

        ...widget.templates.map((template) {
          final isSelected = _selectedTemplateId == template['id'];
          final tiers = template['tiers'] as List<dynamic>? ?? [];

          return Container(
            margin: const EdgeInsets.only(bottom: 12),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isSelected ? const Color(0xFF1B5E20) : Colors.grey[200]!,
                width: isSelected ? 2 : 1,
              ),
            ),
            child: InkWell(
              onTap: () {
                setState(() => _selectedTemplateId = template['id']);
              },
              borderRadius: BorderRadius.circular(12),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Radio<int>(
                          value: template['id'],
                          groupValue: _selectedTemplateId,
                          onChanged: (v) {
                            setState(() => _selectedTemplateId = v);
                          },
                          activeColor: const Color(0xFF1B5E20),
                        ),
                        Text(
                          template['name'] ?? 'Template',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        if (template['is_default'] == true) ...[
                          const SizedBox(width: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: Colors.blue[100],
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: const Text("Défaut", style: TextStyle(fontSize: 10, color: Colors.blue, fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ],
                    ),
                    const SizedBox(height: 8),

                    // Preview prices
                    ...tiers.map((tier) {
                      final discount = (tier['discount_percent'] as num?)?.toDouble() ?? 0;
                      final price = basePrice * (1 - discount / 100);
                      final minQty = (tier['min_quantity_kg'] as num?)?.toInt() ?? 0;
                      final maxQty = tier['max_quantity_kg'];

                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 2),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              maxQty == null ? "$minQty+ kg" : "$minQty-${(maxQty as num).toInt()} kg",
                              style: TextStyle(fontSize: 13, color: Colors.grey[600]),
                            ),
                            Row(
                              children: [
                                Text(
                                  "\$${price.toStringAsFixed(2)}/kg",
                                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                                ),
                                if (discount > 0) ...[
                                  const SizedBox(width: 8),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
                                    decoration: BoxDecoration(
                                      color: Colors.green[50],
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(
                                      "-${discount.toStringAsFixed(0)}%",
                                      style: const TextStyle(fontSize: 11, color: Colors.green, fontWeight: FontWeight.bold),
                                    ),
                                  ),
                                ],
                              ],
                            ),
                          ],
                        ),
                      );
                    }),
                  ],
                ),
              ),
            ),
          );
        }),

        if (widget.templates.isEmpty)
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: Colors.grey[100],
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Center(
              child: Text(
                "Aucun template disponible.\nCréez-en un dans l'onglet 'Mes Templates'.",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey),
              ),
            ),
          ),
      ],
    );
  }
}
