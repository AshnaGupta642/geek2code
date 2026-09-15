import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/game_result.dart';

class GameApiService {
  static const String baseUrl = 'http://localhost:8000/api';
  static const int defaultPatientId = 2;

  static const Map<String, String> backendGameIds = {
    'memory_match': 'G001',
    'sequence_memory': 'G002',
    'pattern_recognition': 'G003',
    'puzzle': 'G004',
    'sound_memory': 'G005',
  };

  Future<Map<String, dynamic>?> startGame({
    required String gameId,
    String? authToken,
  }) async {
    final url = Uri.parse('$baseUrl/games/start');

    final headers = <String, String>{'Content-Type': 'application/json'};

    if (authToken != null && authToken.isNotEmpty) {
      headers['Authorization'] = 'Bearer $authToken';
    }

    try {
      final response = await http.post(
        url,
        headers: headers,
        body: jsonEncode({'game_id': backendGameIds[gameId] ?? gameId}),
      );

      if (response.statusCode >= 200 && response.statusCode < 300) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      }

      print('START GAME API ERROR: ${response.statusCode}');
      print('START GAME API BODY: ${response.body}');
      return null;
    } catch (e) {
      print('START GAME EXCEPTION: $e');
      return null;
    }
  }

  Future<bool> submitResult(
    GameResult result, {
    int patientId = 2,
    String? authToken,
  }) async {
    final url = Uri.parse('$baseUrl/games/result');

    final payload = result.toBackendJson(patientId: patientId);

    final headers = <String, String>{'Content-Type': 'application/json'};

    if (authToken != null && authToken.isNotEmpty) {
      headers['Authorization'] = 'Bearer $authToken';
    }

    try {
      final response = await http.post(
        url,
        headers: headers,
        body: jsonEncode(payload),
      );

      if (response.statusCode >= 200 && response.statusCode < 300) {
        print('RESULT SUBMITTED: ${response.body}');
        return true;
      }

      print('RESULT API ERROR: ${response.statusCode}');
      print('RESULT API BODY: ${response.body}');
      return false;
    } catch (e) {
      print('RESULT API EXCEPTION: $e');
      return false;
    }
  }
}
