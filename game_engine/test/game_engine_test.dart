import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/engine/cognitive_game.dart';
import 'package:game_engine/engine/game_engine.dart';

class FakeGame implements CognitiveGame {
  @override
  String get gameId => 'fake_game';

  @override
  int get difficulty => 1;

  @override
  bool isComplete = false;

  @override
  int score = 0;

  @override
  int attempts = 0;

  @override
  int mistakes = 0;

  @override
  void reset() {
    isComplete = false;
    score = 0;
    attempts = 0;
    mistakes = 0;
  }
}

void main() {
  group('Game Engine', () {
    test('starts a game', () {
      final engine = GameEngine();
      final game = FakeGame();

      engine.startGame(game);

      expect(engine.currentGame, game);
      expect(engine.currentGameId, 'fake_game');
      expect(engine.currentDifficulty, 1);
    });

    test('detects active game', () {
      final engine = GameEngine();
      final game = FakeGame();

      engine.startGame(game);

      expect(engine.isGameActive, true);
    });

    test('detects completed game', () {
      final engine = GameEngine();
      final game = FakeGame();

      engine.startGame(game);

      game.isComplete = true;

      expect(engine.isGameActive, false);
    });

    test('resets current game', () {
      final engine = GameEngine();
      final game = FakeGame();

      game.score = 5;
      game.attempts = 5;
      game.mistakes = 2;

      engine.startGame(game);
      engine.resetGame();

      expect(game.score, 0);
      expect(game.attempts, 0);
      expect(game.mistakes, 0);
    });

    test('ends current game', () {
      final engine = GameEngine();

      engine.startGame(FakeGame());
      engine.endGame();

      expect(engine.currentGame, null);
      expect(engine.isGameActive, false);
    });
  });
}
