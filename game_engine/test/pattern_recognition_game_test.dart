import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/games/pattern_recognition/pattern_recognition_game.dart';

void main() {
  group('Pattern Recognition Game', () {
    test('Easy difficulty creates pattern of 3', () {
      final game = PatternRecognitionGame(difficulty: 1);

      expect(game.pattern.length, 3);
    });

    test('Medium difficulty creates pattern of 4', () {
      final game = PatternRecognitionGame(difficulty: 2);

      expect(game.pattern.length, 4);
    });

    test('Hard difficulty creates pattern of 5', () {
      final game = PatternRecognitionGame(difficulty: 3);

      expect(game.pattern.length, 5);
    });

    test('Correct answer is detected', () {
      final game = PatternRecognitionGame(difficulty: 1);

      game.selectAnswer(game.correctAnswer);

      expect(game.isComplete, true);
      expect(game.isCorrect, true);
    });

    test('Incorrect answer is detected', () {
      final game = PatternRecognitionGame(difficulty: 1);

      final wrongAnswer = game.options.firstWhere(
        (option) => option != game.correctAnswer,
      );

      game.selectAnswer(wrongAnswer);

      expect(game.isComplete, true);
      expect(game.isCorrect, false);
    });

    test('Reset starts a new game', () {
      final game = PatternRecognitionGame(difficulty: 1);

      game.selectAnswer(game.correctAnswer);
      game.reset();

      expect(game.isComplete, false);
      expect(game.isCorrect, false);
    });
  });
}
