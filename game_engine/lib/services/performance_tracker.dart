import '../models/game_result.dart';

class PerformanceTracker {
  int attempts = 0;
  int mistakes = 0;
  int score = 0;
  int hintsUsed = 0;

  DateTime? _startTime;
  DateTime? _responseStartTime;

  double totalResponseTime = 0;
  int responseCount = 0;

  void startGame() {
    _startTime = DateTime.now();
    _responseStartTime = null;

    attempts = 0;
    mistakes = 0;
    score = 0;
    hintsUsed = 0;

    totalResponseTime = 0;
    responseCount = 0;
  }

  void startResponseTimer() {
    _responseStartTime = DateTime.now();
  }

  void recordAttempt({
    required bool correct,
  }) {
    attempts++;

    if (correct) {
      score++;
    } else {
      mistakes++;
    }

    if (_responseStartTime != null) {
      final responseTime =
          DateTime.now().difference(_responseStartTime!).inMilliseconds /
              1000;

      totalResponseTime += responseTime;
      responseCount++;
    }

    _responseStartTime = null;
  }

  void useHint() {
    hintsUsed++;
  }

  double get accuracy {
    if (attempts == 0) {
      return 0;
    }

    return score / attempts;
  }

  double get averageResponseTime {
    if (responseCount == 0) {
      return 0;
    }

    return totalResponseTime / responseCount;
  }

  double completionRate({
    required int completedItems,
    required int totalItems,
  }) {
    if (totalItems == 0) {
      return 0;
    }

    return completedItems / totalItems;
  }

  double get gameDuration {
    if (_startTime == null) {
      return 0;
    }

    return DateTime.now().difference(_startTime!).inMilliseconds / 1000;
  }

  GameResult createResult({
    required String patientId,
    required String gameId,
    required String sessionId,
    required int difficulty,
    required double completionRate,
  }) {
    return GameResult(
      patientId: patientId,
      gameId: gameId,
      sessionId: sessionId,
      difficulty: difficulty,
      score: score,
      accuracy: accuracy,
      averageResponseTime: averageResponseTime,
      attempts: attempts,
      mistakes: mistakes,
      hintsUsed: hintsUsed,
      completionRate: completionRate,
      startedAt: _startTime ?? DateTime.now(),
      completedAt: DateTime.now(),
    );
  }

  void reset() {
    startGame();
  }
}