import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/games/puzzle/puzzle_game.dart';

void main() {
  group('Puzzle Game', () {
    test('Easy difficulty creates 4 pieces', () {
      final game = PuzzleGame(difficulty: 1);

      expect(game.pieces.length, 4);
    });

    test('Medium difficulty creates 6 pieces', () {
      final game = PuzzleGame(difficulty: 2);

      expect(game.pieces.length, 6);
    });

    test('Hard difficulty creates 9 pieces', () {
      final game = PuzzleGame(difficulty: 3);

      expect(game.pieces.length, 9);
    });

    test('Correct puzzle is detected', () {
      final game = PuzzleGame(difficulty: 1);

      game.pieces = List<String>.from(game.correctOrder);

      game.checkPuzzle();

      expect(game.isComplete, true);
      expect(game.isCorrect, true);
    });

    test('Incorrect puzzle is detected', () {
      final game = PuzzleGame(difficulty: 1);

      game.pieces = ['2', '1', '3', '4'];

      game.checkPuzzle();

      expect(game.isComplete, true);
      expect(game.isCorrect, false);
    });

    test('Reset starts a new puzzle', () {
      final game = PuzzleGame(difficulty: 1);

      game.checkPuzzle();
      game.reset();

      expect(game.isComplete, false);
      expect(game.isCorrect, false);
      expect(game.pieces.length, 4);
    });
  });
}
