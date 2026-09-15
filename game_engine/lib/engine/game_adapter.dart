import '../models/game_result.dart';
import '../services/performance_tracker.dart';

class GameAdapter {
  final String gameId;
  final int difficulty;

  GameAdapter({
    required this.gameId,
    required this.difficulty,
  });

  GameResult createResult({
    required PerformanceTracker tracker,
    required String patientId,
    required String sessionId,
    required double completionRate,
  }) {
    return tracker.createResult(
      patientId: patientId,
      gameId: gameId,
      sessionId: sessionId,
      difficulty: difficulty,
      completionRate: completionRate,
    );
  }
}