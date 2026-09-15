import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/models/game_result.dart';
import 'package:game_engine/services/game_api_service.dart';

void main() {
  group('GameApiService', () {
    test('default patient ID is 2', () {
      expect(GameApiService.defaultPatientId, 2);
    });

    test('backend game ID mapping is correct', () {
      expect(GameApiService.backendGameIds['memory_match'], 'G001');
      expect(GameApiService.backendGameIds['sequence_memory'], 'G002');
      expect(GameApiService.backendGameIds['pattern_recognition'], 'G003');
      expect(GameApiService.backendGameIds['puzzle'], 'G004');
      expect(GameApiService.backendGameIds['sound_memory'], 'G005');
    });

    test('result payload uses default patient ID', () {
      final result = GameResult(
        patientId: 'patient_001',
        gameId: 'memory_match',
        sessionId: 'test_session_001',
        difficulty: 1,
        score: 8,
        accuracy: 0.8,
        averageResponseTime: 2.5,
        attempts: 10,
        mistakes: 2,
        hintsUsed: 1,
        completionRate: 1.0,
        startedAt: DateTime(2026, 1, 1, 10, 0),
        completedAt: DateTime(2026, 1, 1, 10, 1),
      );

      final payload = result.toBackendJson(
        patientId: GameApiService.defaultPatientId,
      );

      expect(payload['patient_id'], 2);
      expect(payload['session_id'], 'test_session_001');
      expect(payload['game_id'], 'memory_match');
      expect(payload['score'], 8);
    });
  });
}
