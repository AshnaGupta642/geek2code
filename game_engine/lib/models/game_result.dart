class GameResult {
  final String patientId;
  final String gameId;
  final String sessionId;
  final int difficulty;
  final int score;
  final double accuracy;
  final double averageResponseTime;
  final int attempts;
  final int mistakes;
  final int hintsUsed;
  final double completionRate;
  final DateTime startedAt;
  final DateTime completedAt;

  GameResult({
    required this.patientId,
    required this.gameId,
    required this.sessionId,
    required this.difficulty,
    required this.score,
    required this.accuracy,
    required this.averageResponseTime,
    required this.attempts,
    required this.mistakes,
    required this.hintsUsed,
    required this.completionRate,
    required this.startedAt,
    required this.completedAt,
  });

  Map<String, dynamic> toJson() {
    return {
      'patient_id': patientId,
      'game_id': gameId,
      'session_id': sessionId,
      'difficulty': difficulty,
      'score': score,
      'accuracy': accuracy,
      'response_time_avg': averageResponseTime,
      'attempts': attempts,
      'mistakes': mistakes,
      'hints_used': hintsUsed,
      'completion_rate': completionRate,
      'started_at': startedAt.toIso8601String(),
      'completed_at': completedAt.toIso8601String(),
    };
  }

  factory GameResult.fromJson(Map<String, dynamic> json) {
    return GameResult(
      patientId: json['patient_id'],
      gameId: json['game_id'],
      sessionId: json['session_id'],
      difficulty: json['difficulty'],
      score: json['score'],
      accuracy: json['accuracy'],
      averageResponseTime: json['response_time_avg'],
      attempts: json['attempts'],
      mistakes: json['mistakes'],
      hintsUsed: json['hints_used'],
      completionRate: json['completion_rate'],
      startedAt: DateTime.parse(json['started_at']),
      completedAt: DateTime.parse(json['completed_at']),
    );
  }

  Map<String, dynamic> toBackendJson({required int patientId}) {
    return {
      'patient_id': patientId,
      'session_id': sessionId,
      'game_id': gameId,
      'score': score,
      'accuracy': accuracy * 100,
      'mistakes': mistakes,
      'duration_seconds': completedAt.difference(startedAt).inSeconds,
      'attempts': attempts,
      'hints_used': hintsUsed,
      'response_time': averageResponseTime,
      'difficulty': _difficultyToString(difficulty),
      'completed_at': completedAt.toIso8601String(),
    };
  }

  String _difficultyToString(int difficulty) {
    switch (difficulty) {
      case 1:
        return 'easy';
      case 2:
        return 'medium';
      case 3:
        return 'hard';
      default:
        return 'easy';
    }
  }
}
