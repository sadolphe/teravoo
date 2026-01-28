import 'package:flutter/material.dart';
import 'package:mobile/core/api_client.dart';

class PriceTierWidget extends StatefulWidget {
  final int productId;
  final double basePriceFob;
  final List<dynamic> tiers;
  final double moqKg;
  final int quantityAvailable;
  final Function(double quantity, double pricePerKg, double total)? onPriceCalculated;

  const PriceTierWidget({
    super.key,
    required this.productId,
    required this.basePriceFob,
    required this.tiers,
    this.moqKg = 1.0,
    this.quantityAvailable = 500,
    this.onPriceCalculated,
  });

  @override
  State<PriceTierWidget> createState() => _PriceTierWidgetState();
}

class _PriceTierWidgetState extends State<PriceTierWidget> {
  final ApiClient _api = ApiClient();
  final TextEditingController _quantityController = TextEditingController();

  double _quantity = 10;
  double _currentPricePerKg = 0;
  double _total = 0;
  double _savingsPercent = 0;
  int _activeTierPosition = 0;
  Map<String, dynamic>? _nextTier;
  bool _isCalculating = false;

  @override
  void initState() {
    super.initState();
    _quantity = widget.moqKg > 1 ? widget.moqKg : 10;
    _quantityController.text = _quantity.toStringAsFixed(0);
    _currentPricePerKg = widget.basePriceFob;
    _total = _quantity * _currentPricePerKg;

    // Initial calculation
    _calculatePrice();
  }

  @override
  void dispose() {
    _quantityController.dispose();
    super.dispose();
  }

  Future<void> _calculatePrice() async {
    if (_quantity < widget.moqKg) return;

    setState(() => _isCalculating = true);

    final result = await _api.calculatePrice(widget.productId, _quantity);

    if (result != null && mounted) {
      setState(() {
        _currentPricePerKg = (result['price_per_kg'] as num).toDouble();
        _total = (result['total'] as num).toDouble();

        if (result['tier_applied'] != null) {
          _activeTierPosition = result['tier_applied']['position'] ?? 0;
        }

        if (result['savings_vs_base'] != null) {
          _savingsPercent = (result['savings_vs_base']['percent'] as num?)?.toDouble() ?? 0;
        } else {
          _savingsPercent = 0;
        }

        _nextTier = result['next_tier'];
        _isCalculating = false;
      });

      widget.onPriceCalculated?.call(_quantity, _currentPricePerKg, _total);
    } else {
      setState(() => _isCalculating = false);
    }
  }

  void _onQuantityChanged(String value) {
    final qty = double.tryParse(value) ?? widget.moqKg;
    setState(() {
      _quantity = qty.clamp(widget.moqKg, widget.quantityAvailable.toDouble());
    });
    _calculatePrice();
  }

  @override
  Widget build(BuildContext context) {
    // If no tiers or single tier, show simple price
    if (widget.tiers.isEmpty || (widget.tiers.length == 1 && (widget.tiers[0]['discount_percent'] ?? 0) == 0)) {
      return _buildSimplePrice();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Title
        Row(
          children: [
            const Text(
              "Tarifs Dégressifs",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.green[100],
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Text(
                "Volume Discount",
                style: TextStyle(fontSize: 10, color: Colors.green, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),

        // Tiers Table
        Container(
          decoration: BoxDecoration(
            border: Border.all(color: Colors.grey.shade200),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Column(
            children: [
              // Header
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: Colors.grey.shade50,
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(12),
                    topRight: Radius.circular(12),
                  ),
                ),
                child: const Row(
                  children: [
                    Expanded(flex: 2, child: Text("Quantité", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
                    Expanded(flex: 2, child: Text("Prix/kg", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
                    Expanded(flex: 1, child: Text("Économie", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12), textAlign: TextAlign.right)),
                  ],
                ),
              ),

              // Tiers
              ...widget.tiers.asMap().entries.map((entry) {
                final tier = entry.value;
                final isActive = (tier['position'] ?? entry.key) == _activeTierPosition;
                final discount = (tier['discount_percent'] as num?)?.toDouble() ?? 0;
                final pricePerKg = (tier['price_per_kg'] as num?)?.toDouble() ?? widget.basePriceFob;
                final minQty = (tier['min_quantity_kg'] as num?)?.toDouble() ?? 0;
                final maxQty = tier['max_quantity_kg'];

                return Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: isActive ? const Color(0xFF1B5E20).withValues(alpha: 0.1) : null,
                    border: Border(
                      left: isActive ? const BorderSide(color: Color(0xFF1B5E20), width: 4) : BorderSide.none,
                      bottom: BorderSide(color: Colors.grey.shade200),
                    ),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        flex: 2,
                        child: Row(
                          children: [
                            Text(
                              maxQty == null ? "${minQty.toInt()}+ kg" : "${minQty.toInt()} - ${(maxQty as num).toInt()} kg",
                              style: TextStyle(
                                fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                                fontSize: 13,
                              ),
                            ),
                            if (isActive) ...[
                              const SizedBox(width: 8),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: const Color(0xFF1B5E20),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: const Text(
                                  "Actif",
                                  style: TextStyle(color: Colors.white, fontSize: 9, fontWeight: FontWeight.bold),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                      Expanded(
                        flex: 2,
                        child: Text(
                          "\$${pricePerKg.toStringAsFixed(2)}",
                          style: TextStyle(
                            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                            color: isActive ? const Color(0xFF1B5E20) : null,
                            fontSize: isActive ? 16 : 13,
                          ),
                        ),
                      ),
                      Expanded(
                        flex: 1,
                        child: Text(
                          discount > 0 ? "-${discount.toStringAsFixed(1)}%" : "Base",
                          style: TextStyle(
                            color: discount > 0 ? Colors.green : Colors.grey,
                            fontWeight: discount > 0 ? FontWeight.bold : FontWeight.normal,
                            fontSize: 12,
                          ),
                          textAlign: TextAlign.right,
                        ),
                      ),
                    ],
                  ),
                );
              }),
            ],
          ),
        ),

        const SizedBox(height: 24),

        // Quantity Input & Calculator
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.grey.shade50,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.grey.shade200),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Quantity Input
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text("Quantité souhaitée", style: TextStyle(fontWeight: FontWeight.w500)),
                  Text("Dispo: ${widget.quantityAvailable} kg", style: TextStyle(fontSize: 12, color: Colors.grey.shade600)),
                ],
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _quantityController,
                      keyboardType: TextInputType.number,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: Colors.white,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: BorderSide(color: Colors.grey.shade300),
                        ),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      ),
                      onChanged: _onQuantityChanged,
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Text("kg", style: TextStyle(fontSize: 16, color: Colors.grey)),
                ],
              ),
              if (widget.moqKg > 1)
                Padding(
                  padding: const EdgeInsets.only(top: 4),
                  child: Text(
                    "Commande minimum: ${widget.moqKg.toInt()} kg",
                    style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                  ),
                ),

              const SizedBox(height: 16),
              const Divider(),
              const SizedBox(height: 12),

              // Calculated Result
              if (_isCalculating)
                const Center(child: CircularProgressIndicator(strokeWidth: 2))
              else ...[
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Prix appliqué", style: TextStyle(color: Colors.grey)),
                    Text(
                      "\$${_currentPricePerKg.toStringAsFixed(2)}/kg",
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF1B5E20)),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Total", style: TextStyle(fontWeight: FontWeight.w500)),
                    Text(
                      "\$${_total.toStringAsFixed(2)}",
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 24, color: Color(0xFF1B5E20)),
                    ),
                  ],
                ),

                // Savings
                if (_savingsPercent > 0) ...[
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.green.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text("Vous économisez", style: TextStyle(color: Colors.green, fontWeight: FontWeight.w500)),
                        Text(
                          "\$${((widget.basePriceFob - _currentPricePerKg) * _quantity).toStringAsFixed(2)} (${_savingsPercent.toStringAsFixed(1)}%)",
                          style: const TextStyle(color: Colors.green, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ],

                // Next Tier Nudge
                if (_nextTier != null) ...[
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("💡 ", style: TextStyle(fontSize: 16)),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                "Plus que ${((_nextTier!['at_quantity_kg'] as num) - _quantity).toInt()} kg pour \$${(_nextTier!['price_per_kg'] as num).toStringAsFixed(2)}/kg",
                                style: const TextStyle(color: Colors.blue, fontWeight: FontWeight.w500, fontSize: 13),
                              ),
                              Text(
                                "Économie supplémentaire: \$${(_nextTier!['extra_savings_total'] as num).toStringAsFixed(2)}",
                                style: TextStyle(color: Colors.blue.shade400, fontSize: 11),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ],
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildSimplePrice() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          crossAxisAlignment: CrossAxisAlignment.baseline,
          textBaseline: TextBaseline.alphabetic,
          children: [
            Text(
              "\$${widget.basePriceFob.toStringAsFixed(2)}",
              style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Color(0xFF1B5E20)),
            ),
            const SizedBox(width: 8),
            const Text("/ kg (FOB)", style: TextStyle(color: Colors.grey)),
          ],
        ),
        const SizedBox(height: 8),
        Text(
          "Prix unique quelle que soit la quantité commandée.",
          style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
        ),
      ],
    );
  }
}
