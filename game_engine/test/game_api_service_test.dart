import 'package:flutter_test/flutter_test.dart';

import 'package:game_engine/models/game_result.dart';
import 'package:game_engine/services/game_api_service.dart';

void main() {
  group('GameApiService', () {
    test('creates correct backend payload from GameResult', () {
      final startedAt = DateTime(2026, 9, 12, 10, 0, 0);
      final completedAt = DateTime(2026, 9, 12, 10, 0, 15);

      final result = GameResult(
        patientId: 'patient_001',
        gameId: 'memory_match',
        sessionId: 'test_session_001',
        difficulty: 2,
        score: 8,
        accuracy: 0.8,
        averageResponseTime: 2.5,
        attempts: 10,
        mistakes: 2,
        hintsUsed: 1,
        completionRate: 1.0,
        startedAt: startedAt,
        completedAt: completedAt,
      );

      final payload = result.toBackendJson(
        patientId: GameApiService.defaultPatientId,
      );

      expect(payload['patient_id'], 1);
      expect(payload['session_id'], 'test_session_001');
      expect(payload['game_id'], 'memory_match');
      expect(payload['score'], 8);
      expect(payload['accuracy'], 80);
      expect(payload['mistakes'], 2);
      expect(payload['duration_seconds'], 15);
      expect(payload['attempts'], 10);
      expect(payload['hints_used'], 1);
      expect(payload['response_time'], 2.5);
      expect(payload['difficulty'], 'medium');
      expect(
        payload['completed_at'],
        completedAt.toIso8601String(),
      );
    });
  });
}