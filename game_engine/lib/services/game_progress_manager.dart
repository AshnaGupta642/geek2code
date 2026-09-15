import 'adaptive_difficulty.dart';

class GameProgressManager {
  final AdaptiveDifficulty _adaptiveDifficulty = AdaptiveDifficulty();

  final Map<String, int> _difficultyByGame = {};

  int getDifficulty(String gameId) {
    return _difficultyByGame[gameId] ?? 1;
  }

  int updateDifficulty({
    required String gameId,
    required double accuracy,
    required double averageResponseTime,
  }) {
    final currentDifficulty = getDifficulty(gameId);

    final nextDifficulty = _adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: currentDifficulty,
      accuracy: accuracy,
      averageResponseTime: averageResponseTime,
    );

    _difficultyByGame[gameId] = nextDifficulty;

    return nextDifficulty;
  }

  void resetGameProgress(String gameId) {
    _difficultyByGame[gameId] = 1;
  }

  void resetAllProgress() {
    _difficultyByGame.clear();
  }
}