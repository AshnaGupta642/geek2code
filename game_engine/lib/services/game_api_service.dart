import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/game_result.dart';

class GameApiService {
  static const String baseUrl = 'http://localhost:8000';

  // Temporary patient ID for Person 2 ↔ Person 5 testing.
  // This does not modify Person 1's code.
  static const int defaultPatientId = 1;

  Future<bool> submitResult(
    GameResult result, {
    int? patientId,
  }) async {
    final url = Uri.parse('$baseUrl/games/result');

    final payload = result.toBackendJson(
      patientId: patientId ?? defaultPatientId,
    );

    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode(payload),
      );

      if (response.statusCode >= 200 &&
          response.statusCode < 300) {
        return true;
      }

      return false;
    } catch (_) {
      return false;
    }
  }
}