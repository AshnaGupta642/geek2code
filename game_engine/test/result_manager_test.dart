import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/engine/result_manager.dart';
import 'package:game_engine/models/game_result.dart';

void main() {
  group('ResultManager', () {
    GameResult createTestResult(double accuracy) {
      final now = DateTime.now();

      return GameResult(
        patientId: 'patient_001',
        gameId: 'memory_match',
        sessionId: 'session_001',
        difficulty: 1,
        score: 3,
        accuracy: accuracy,
        averageResponseTime: 4,
        attempts: 4,
        mistakes: 1,
        hintsUsed: 0,
        completionRate: 1.0,
        startedAt: now,
        completedAt: now,
      );
    }

    test('starts with no results', () {
      final manager = ResultManager();

      expect(manager.totalGames, 0);
      expect(manager.getResults(), isEmpty);
    });

    test('adds a result', () {
      final manager = ResultManager();

      manager.addResult(createTestResult(0.75));

      expect(manager.totalGames, 1);
    });

    test('returns latest result', () {
      final manager = ResultManager();

      manager.addResult(createTestResult(0.75));

      final result = manager.getLatestResult();

      expect(result, isNotNull);
      expect(result!.accuracy, 0.75);
    });

    test('calculates average accuracy', () {
      final manager = ResultManager();

      manager.addResult(createTestResult(0.80));

      manager.addResult(createTestResult(0.60));

      expect(manager.averageAccuracy, 0.70);
    });

    test('clears all results', () {
      final manager = ResultManager();

      manager.addResult(createTestResult(0.90));

      manager.clearResults();

      expect(manager.totalGames, 0);
      expect(manager.getResults(), isEmpty);
    });
  });
}
