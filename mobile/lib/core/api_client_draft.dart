
// This is a PSEUDO-CODE example to guide the mobile developer.
// File: lib/core/api_client.dart

/*
import 'package:dio/dio.dart';

class ApiClient {
  final Dio dio;
  
  // Use 10.0.2.2 for Android Emulator to access localhost
  // Use http://localhost:8000 for iOS Simulator
  ApiClient({required String baseUrl}) : dio = Dio(BaseOptions(baseUrl: baseUrl));

  Future<dynamic> login(String phone) async {
    return await dio.post('/auth/login', data: {'phone_number': phone});
  }

  Future<dynamic> uploadProduct(String name, double price, String imageUrl) async {
    return await dio.post('/products/upload', data: {
      'name': name,
      'price_fob': price,
      'image_url': imageUrl
    });
  }
}
*/
