import 'package:dio/dio.dart';

class ApiClient {
  // Setup: 
  // For iOS Simulator: http://localhost:8000/api/v1
  // For Android Emulator: http://10.0.2.2:8000/api/v1
  // For Real Device (USB): http://<YOUR_IP>:8000/api/v1
  static const String baseUrl = 'http://localhost:8000/api/v1'; 
  
  final Dio _dio = Dio(BaseOptions(
    baseUrl: baseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
  ));

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
        throw e;
      }
  }

  Future<Map<String, dynamic>> uploadProduct({
    required String name, 
    required double price, 
    required String imagePath,
    required double moisture,
    required double vanillin,
    String? producerId,
  }) async {
    
    // String fileName = imagePath.split('/').last; // unused for MVP JSON upload

    final response = await _dio.post('/products/upload', data: {
        "name": name,
        "price_fob": price,
        "image_url": "https://placehold.co/600x400?text=Uploaded+From+Mobile",
        "moisture_content": moisture,
        "vanillin_content": vanillin,
        "producer_id": producerId != null ? int.tryParse(producerId) : null
    });
    return response.data;
  }

  Future<List<dynamic>> getProducts() async {
    try {
      final response = await _dio.get('/products/');
      return response.data as List<dynamic>;
    } catch (e) {
      print("API Error (getProducts): $e");
      print("API Error (getProducts): $e");
      return [];
    }
  }

  Future<void> deleteProduct(int id) async {
    try {
      await _dio.delete('/products/$id');
    } catch (e) {
      print("API Error (deleteProduct): $e");
      throw e;
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

}
