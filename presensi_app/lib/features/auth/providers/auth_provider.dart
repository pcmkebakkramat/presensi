import 'dart:convert';
import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../data/user_model.dart';
import '../../../core/network/api_service.dart';

final authProvider = AsyncNotifierProvider<AuthNotifier, UserModel?>(() {
  return AuthNotifier();
});

class AuthNotifier extends AsyncNotifier<UserModel?> {
  @override
  FutureOr<UserModel?> build() async {
    return _checkSession();
  }

  Future<UserModel?> _checkSession() async {
    final prefs = await SharedPreferences.getInstance();
    final userStr = prefs.getString('PCM_USER');
    if (userStr != null) {
      return UserModel.fromJson(jsonDecode(userStr));
    }
    return null;
  }

  Future<void> login(String username, String password) async {
    state = const AsyncValue.loading();
    try {
      final res = await ApiService.post({
        'action': 'login',
        'data': {
          'username': username,
          'password': password,
        }
      });

      if (res['status'] == 'success') {
        final user = UserModel.fromJson(res);
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('PCM_USER', jsonEncode(user.toJson()));
        state = AsyncValue.data(user);
      } else {
        state = const AsyncValue.data(null);
        throw Exception(res['message'] ?? 'Login failed');
      }
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      rethrow;
    }
  }
  
  Future<void> register(Map<String, dynamic> data) async {
    state = const AsyncValue.loading();
    try {
      final res = await ApiService.post({
        'action': 'register',
        'data': data,
      });

      if (res['status'] == 'success') {
        state = const AsyncValue.data(null);
      } else {
        state = const AsyncValue.data(null);
        throw Exception(res['message'] ?? 'Register failed');
      }
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      rethrow;
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('PCM_USER');
    state = const AsyncValue.data(null);
  }
}
