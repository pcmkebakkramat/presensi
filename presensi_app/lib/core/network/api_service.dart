import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "https://script.google.com/macros/s/AKfycbwAvmq-LQZdHDrlegLOVXo-IZsgx47aGdhDOQhN3Dlf3l79JFVNxiGdrdlpNRw7DkX0Aw/exec";

  static Future<Map<String, dynamic>> post(Map<String, dynamic> body) async {
    try {
      // For Google Apps Script, following redirects is required and handled automatically by the http package
      final response = await http.post(
        Uri.parse(baseUrl),
        headers: {"Content-Type": "text/plain"},
        body: jsonEncode(body),
      );
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception("Failed with status code: ${response.statusCode}");
      }
    } catch (e) {
      throw Exception("Network error: $e");
    }
  }
}
