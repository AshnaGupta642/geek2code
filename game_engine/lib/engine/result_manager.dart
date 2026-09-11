import '../models/game_result.dart';

class ResultManager {
  final List<GameResult> results = [];

  void addResult(GameResult result) {
    results.add(result);
  }

  List<GameResult> getResults() {
    return List.unmodifiable(results);
  }

  GameResult? getLatestResult() {
    if (results.isEmpty) {
      return null;
    }

    return results.last;
  }

  void clearResults() {
    results.clear();
  }

  int get totalGames {
    return results.length;
  }

  double get averageAccuracy {
    if (results.isEmpty) {
      return 0;
    }

    final total = results.fold<double>(
      0,
      (sum, result) => sum + result.accuracy,
    );

    return total / results.length;
  }
}