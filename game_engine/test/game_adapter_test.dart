import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/engine/game_adapter.dart';
import 'package:game_engine/services/performance_tracker.dart';

void main() {
  test('GameAdapter creates a game result', () {
    final tracker = PerformanceTracker();

    tracker.startGame();

    tracker.startResponseTimer();

    tracker.recordAttempt(correct: true);

    final adapter = GameAdapter(gameId: 'memory_match', difficulty: 1);

    final result = adapter.createResult(
      tracker: tracker,
      patientId: 'patient_001',
      sessionId: 'session_001',
      completionRate: 1.0,
    );

    expect(result.gameId, 'memory_match');
    expect(result.difficulty, 1);
    expect(result.score, 1);
    expect(result.accuracy, 1);
    expect(result.completionRate, 1.0);
  });
}
