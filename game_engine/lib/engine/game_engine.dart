import 'cognitive_game.dart';

class GameEngine {
  CognitiveGame? currentGame;

  void startGame(CognitiveGame game) {
    currentGame = game;
  }

  void resetGame() {
    currentGame?.reset();
  }

  bool get isGameActive {
    return currentGame != null &&
        !currentGame!.isComplete;
  }

  String? get currentGameId {
    return currentGame?.gameId;
  }

  int? get currentDifficulty {
    return currentGame?.difficulty;
  }

  void endGame() {
    currentGame = null;
  }
}