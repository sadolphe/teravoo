import 'package:flutter/material.dart';
import 'dart:io';
import '../core/api_client.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  bool _isAnalyzing = false;
  File? _capturedImage;
  final ApiClient _apiClient = ApiClient();
  final TextEditingController _priceController = TextEditingController();
  final TextEditingController _moistureController = TextEditingController();
  final TextEditingController _vanillinController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();

  // Producer State
  List<dynamic> _producers = [];
  String? _selectedProducerId;
  
  @override
  void initState() {
    super.initState();
    _loadProducers();
  }

  Future<void> _loadProducers() async {
      final producers = await _apiClient.getProducers();
      if (mounted) {
          setState(() {
              _producers = producers;
              if (_producers.isNotEmpty) {
                  _selectedProducerId = _producers.first['id'].toString();
              }
          });
      }
  }

  @override
  void dispose() {
    _priceController.dispose();
    _moistureController.dispose();
    _vanillinController.dispose();
    super.dispose();
  }
  
  // Analysis Result
  Map<String, dynamic>? _analysisResult;

  void _captureImage() async {
     setState(() => _isAnalyzing = true);
     
     // Simulate AI Processing time
     await Future.delayed(const Duration(seconds: 2));
     
     setState(() {
         _isAnalyzing = false;
         _capturedImage = File('mock_path'); 
         _analysisResult = {
             "grade": "A",
             "moisture": "35",
             "vanillin": "1.8",
             "recommended_price": 250.0
         };
         _priceController.text = "250.0";
         _moistureController.text = "35.0";
         _vanillinController.text = "1.8";
         _nameController.text = "Vanille Scan #${DateTime.now().minute}";
     });
  }

  Future<void> _createNewProducer() async {
      final nameController = TextEditingController();
      final regionController = TextEditingController();
      final districtController = TextEditingController();
      
      return showDialog(context: context, builder: (ctx) => AlertDialog(
          title: const Text("New Producer"),
          content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                  TextField(controller: nameController, decoration: const InputDecoration(labelText: "Full Name")),
                  TextField(controller: regionController, decoration: const InputDecoration(labelText: "Region")),
                  TextField(controller: districtController, decoration: const InputDecoration(labelText: "Village/District")),
              ],
          ),
          actions: [
              TextButton(onPressed: () => Navigator.pop(ctx), child: const Text("Cancel")),
              ElevatedButton(
                  onPressed: () async {
                      Navigator.pop(ctx);
                      final newProducer = await _apiClient.createProducer(
                          nameController.text, 
                          regionController.text, 
                          districtController.text
                      );
                      if (newProducer != null) {
                          _loadProducers(); // Refresh list
                          ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Producer Created!")));
                      }
                  }, 
                  child: const Text("Create")
              )
          ],
      ));
  }

  void _publishProduct() async {
      if (_analysisResult == null) return;
      
      try {
          final double finalPrice = double.tryParse(_priceController.text) ?? 250.0;
          final double finalMoisture = double.tryParse(_moistureController.text) ?? 35.0;
          final double finalVanillin = double.tryParse(_vanillinController.text) ?? 1.8;

          await _apiClient.uploadProduct(
              name: _nameController.text, 
              price: finalPrice, 
              imagePath: "mock_image.jpg",
              moisture: finalMoisture,
              vanillin: finalVanillin,
              producerId: _selectedProducerId
          );
          if (mounted) {
              Navigator.pop(context, true); 
          }
      } catch (e) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
      }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF000000),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        iconTheme: const IconThemeData(color: Colors.white),
        elevation: 0,
      ),
      body: Column(
        children: [
          Expanded(
            child: Container(
                width: double.infinity,
                decoration: BoxDecoration(
                    color: Colors.grey[900],
                    borderRadius: BorderRadius.circular(20),
                ),
                margin: const EdgeInsets.all(16),
                child: _capturedImage == null 
                ? Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                        Icon(Icons.camera_alt, size: 64, color: Colors.white.withOpacity(0.5)),
                        const SizedBox(height: 16),
                        const Text("Align Vanilla Beans", style: TextStyle(color: Colors.white))
                    ],
                )
                : Stack(
                    fit: StackFit.expand,
                    children: [
                        Image.network(
                            "https://placehold.co/400x600/1a1a1a/e5e5e5?text=Scanned+Vanilla", 
                            fit: BoxFit.cover
                        ),
                        if (_analysisResult != null)
                        Container(
                            decoration: BoxDecoration(
                                gradient: LinearGradient(
                                    begin: Alignment.topCenter,
                                    end: Alignment.bottomCenter,
                                    colors: [Colors.transparent, Colors.black.withOpacity(0.9)]
                                )
                            ),
                            padding: const EdgeInsets.all(24),
                            child: SingleChildScrollView(
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.end,
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                    // PRODUCER SELECTION
                                    Container(
                                        padding: const EdgeInsets.all(12),
                                        margin: const EdgeInsets.only(bottom: 16),
                                        decoration: BoxDecoration(
                                            color: Colors.white.withOpacity(0.1),
                                            borderRadius: BorderRadius.circular(12),
                                            border: Border.all(color: Colors.white24)
                                        ),
                                        child: Column(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                                const Text("SOURCING FROM:", style: TextStyle(color: Colors.white54, fontSize: 10, fontWeight: FontWeight.bold)),
                                                const SizedBox(height: 8),
                                                Row(
                                                    children: [
                                                        const Icon(Icons.person, color: Colors.white, size: 20),
                                                        const SizedBox(width: 8),
                                                        Expanded(
                                                            child: DropdownButton<String>(
                                                                value: _selectedProducerId,
                                                                dropdownColor: Colors.grey[900],
                                                                isDense: true,
                                                                underline: const SizedBox(),
                                                                isExpanded: true,
                                                                hint: const Text("Select Producer", style: TextStyle(color: Colors.white)),
                                                                items: _producers.map<DropdownMenuItem<String>>((p) {
                                                                    return DropdownMenuItem<String>(
                                                                        value: p['id'].toString(),
                                                                        child: Text(p['name'], style: const TextStyle(color: Colors.white)),
                                                                    );
                                                                }).toList(), 
                                                                onChanged: (val) => setState(() => _selectedProducerId = val),
                                                            ),
                                                        ),
                                                        IconButton(
                                                            icon: const Icon(Icons.add_circle, color: Color(0xFFD4AF37)),
                                                            onPressed: _createNewProducer,
                                                        )
                                                    ],
                                                )
                                            ],
                                        ),
                                    ),

                                    // NEW: Batch Name Field
                                    Container(
                                      margin: const EdgeInsets.only(bottom: 16),
                                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: Colors.white.withOpacity(0.1),
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                      child: TextField(
                                        controller: _nameController,
                                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                                        decoration: const InputDecoration(
                                          border: InputBorder.none,
                                          labelText: "Batch Name",
                                          labelStyle: TextStyle(color: Colors.white54),
                                          icon: Icon(Icons.edit, color: Colors.white54),
                                        ),
                                      ),
                                    ),

                                    Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                        decoration: BoxDecoration(color: Colors.green, borderRadius: BorderRadius.circular(20)),
                                        child: Text("Grade ${_analysisResult!['grade']}", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))
                                    ),
// ... (rest)

                                    const SizedBox(height: 16),
                                    
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                      children: [
                                        Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            const Text("Moisture %", style: TextStyle(color: Colors.white70, fontSize: 12)),
                                            SizedBox(
                                              width: 80,
                                              child: TextField(
                                                controller: _moistureController,
                                                style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                                                keyboardType: TextInputType.number,
                                                decoration: const InputDecoration(border: InputBorder.none),
                                              ),
                                            ),
                                          ],
                                        ),
                                        Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            const Text("Vanillin %", style: TextStyle(color: Colors.white70, fontSize: 12)),
                                            SizedBox(
                                              width: 80,
                                              child: TextField(
                                                controller: _vanillinController,
                                                style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                                                keyboardType: TextInputType.number,
                                                decoration: const InputDecoration(border: InputBorder.none),
                                              ),
                                            ),
                                          ],
                                        ),
                                        const Icon(Icons.edit, color: Colors.white24, size: 16)
                                      ],
                                    ),

                                    const SizedBox(height: 16),
                                    const Divider(color: Colors.white24),
                                    Row(
                                      children: [
                                        const Text("\$ ", style: TextStyle(color: Color(0xFFD4AF37), fontSize: 24, fontWeight: FontWeight.bold)),
                                        SizedBox(
                                          width: 100,
                                          child: TextField(
                                            controller: _priceController,
                                            style: const TextStyle(color: Color(0xFFD4AF37), fontSize: 24, fontWeight: FontWeight.bold),
                                            keyboardType: TextInputType.number,
                                            decoration: const InputDecoration(
                                              border: InputBorder.none,
                                              isDense: true,
                                            ),
                                          ),
                                        ),
                                        const Text("/ kg", style: TextStyle(color: Color(0xFFD4AF37), fontSize: 24, fontWeight: FontWeight.bold)),
                                      ],
                                    ),
                                    const Text("Recommended Price based on Quality", style: TextStyle(color: Colors.white54, fontSize: 12)),
                                ],
                              ),
                            ),
                        )
                    ],
                )
            ),
          ),
          
          Padding(
            padding: const EdgeInsets.all(24.0),
            child: _capturedImage == null 
            ? IconButton(
                onPressed: _isAnalyzing ? null : _captureImage,
                iconSize: 72,
                icon: _isAnalyzing 
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Icon(Icons.circle, color: Colors.white),
            )
            : SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                    onPressed: _publishProduct,
                    style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFD4AF37),
                        foregroundColor: Colors.black,
                        padding: const EdgeInsets.symmetric(vertical: 16)
                    ),
                    child: const Text("Publish to Marketplace", style: TextStyle(fontWeight: FontWeight.bold)),
                ),
            ),
          )
        ],
      ),
    );
  }
}
