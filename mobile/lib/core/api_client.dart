import 'package:dio/dio.dart';

class ApiClient {
  // Setup: 
  // For iOS Simulator: http://localhost:8000/api/v1
  // For Android Emulator: http://10.0.2.2:8000/api/v1
  // For Real Device (USB): http://<YOUR_IP>:8000/api/v1
  // PROD (Render):
  static const String baseUrl = 'https://teravoo-backend.onrender.com/api/v1'; 
  
  // LOCAL DEV (uncomment for local development):
  // static const String baseUrl = 'http://localhost:8000/api/v1';
  
  final Dio _dio = Dio(BaseOptions(
    baseUrl: baseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  ));

  // MVP State Management: Static to share across instances
  static int? currentProducerId;

  Future<bool> requestOtp(String phone) async {
    try {
      final response = await _dio.post('/auth/login', data: {'phone_number': phone});
      return response.statusCode == 200;
    } catch (e) {
      print("API Error (requestOtp): $e");
      return false;
    }
  }

  Future<Map<String, dynamic>> verifyOtp(String phone, String otp) async {
      try {
        final response = await _dio.post('/auth/verify', data: {'phone_number': phone, 'otp': otp});
        return response.data;
      } catch (e) {
        print("API Error (verifyOtp): $e");
        rethrow;
      }
  }

  Future<Map<String, dynamic>> uploadProduct({
    required String name, 
    required double price, 
    required String imagePath,
    required double moisture,
    required double vanillin,
    String? producerId,
    String? grade,
  }) async {
    
    // String fileName = imagePath.split('/').last; // unused for MVP JSON upload

    final response = await _dio.post('/products/upload', data: {
        "name": name,
        "price_fob": price,
        "image_url": "https://placehold.co/600x400?text=Uploaded+From+Mobile",
        "moisture_content": moisture,
        "vanillin_content": vanillin,
        "producer_id": producerId != null ? int.tryParse(producerId) : null,
        "grade": grade ?? "A"
    });
    return response.data;
  }

  Future<List<dynamic>> getProducts() async {
    try {
      final response = await _dio.get('/products/');
      return response.data as List<dynamic>;
    } catch (e) {
      print("API Error (getProducts): $e");
      return [];
    }
  }

  Future<void> deleteProduct(int id) async {
    try {
      await _dio.delete('/products/$id');
    } catch (e) {
      print("API Error (deleteProduct): $e");
      rethrow;
    }
  }
  Future<List<dynamic>> getProducers() async {
    try {
      final response = await _dio.get('/producers/');
      return response.data;
    } catch (e) {
      print("API Error (getProducers): $e");
      return [];
    }
  }

  Future<Map<String, dynamic>?> createProducer(String name, String region, String district) async {
      try {
          final response = await _dio.post('/producers/', data: {
              "name": name,
              "location_region": region,
              "location_district": district,
              "bio": "Onboarded via Mobile App",
              "badges": ["NEW"]
          });
          return response.data;
      } catch (e) {
          print("API Error (createProducer): $e");
          return null;
      }
  }

  // Sales Dashboard
  Future<List<dynamic>> getMySales() async {
    try {
      final response = await _dio.get('/producers/me/sales');
      return response.data;
    } catch (e) {
       print("API Error (getMySales): $e");
       return [];
    }
  }

  // Sales Actions
  Future<void> acceptOrder(int orderId) async {
    try {
      await _dio.post('/orders/$orderId/accept');
    } catch (e) {
      print("API Error (acceptOrder): $e");
      rethrow;
    }
  }

  Future<void> rejectOrder(int orderId) async {
    try {
      await _dio.post('/orders/$orderId/reject');
    } catch (e) {
      print("API Error (rejectOrder): $e");
      rethrow;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // PRICING TIERS API
  // ═══════════════════════════════════════════════════════════

  /// Get pricing tiers for a product
  Future<Map<String, dynamic>?> getProductPriceTiers(int productId) async {
    try {
      final response = await _dio.get('/pricing/products/$productId/price-tiers');
      return response.data;
    } catch (e) {
      print("API Error (getProductPriceTiers): $e");
      return null;
    }
  }

  /// Calculate price for a given quantity
  Future<Map<String, dynamic>?> calculatePrice(int productId, double quantityKg) async {
    try {
      final response = await _dio.get('/pricing/products/$productId/calculate-price',
        queryParameters: {'quantity_kg': quantityKg}
      );
      return response.data;
    } catch (e) {
      print("API Error (calculatePrice): $e");
      return null;
    }
  }

  /// Set price tiers for a product (Producer side)
  Future<List<dynamic>?> setProductPriceTiers(int productId, List<Map<String, dynamic>> tiers) async {
    try {
      final response = await _dio.post('/pricing/products/$productId/price-tiers',
        data: {'tiers': tiers}
      );
      return response.data;
    } catch (e) {
      print("API Error (setProductPriceTiers): $e");
      return null;
    }
  }

  /// Get producer's price templates, defaults to current producer
  Future<List<dynamic>> getProducerTemplates(int? producerId) async {
    final id = producerId ?? currentProducerId;
    if (id == null) return [];
    
    try {
      final response = await _dio.get('/pricing/producers/$id/price-templates');
      return response.data;
    } catch (e) {
      print("API Error (getProducerTemplates): $e");
      return [];
    }
  }

  /// Create a new price template
  Future<Map<String, dynamic>?> createPriceTemplate(int? producerId, Map<String, dynamic> template) async {
    final id = producerId ?? currentProducerId;
    if (id == null) return null;

    try {
      final response = await _dio.post('/pricing/producers/$id/price-templates',
        data: template
      );
      return response.data;
    } catch (e) {
      print("API Error (createPriceTemplate): $e");
      return null;
    }
  }

  /// Update pricing mode for a product
  Future<Map<String, dynamic>?> updateProductPricingMode(int productId, String mode, {int? templateId}) async {
    try {
      final response = await _dio.put('/pricing/products/$productId/pricing-mode',
        data: {
          'mode': mode,
          if (templateId != null) 'template_id': templateId
        }
      );
      return response.data;
    } catch (e) {
      print("API Error (updateProductPricingMode): $e");
      return null;
    }
  }

  // Update Product Details
  Future<Map<String, dynamic>?> updateProduct(int id, Map<String, dynamic> data) async {
    try {
      final response = await _dio.put('/products/$id', data: data);
      return response.data;
    } catch (e) {
      print("API Error (updateProduct): $e");
      return null;
    }
  }
}
