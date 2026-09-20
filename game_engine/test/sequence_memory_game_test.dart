import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/games/sequence_memory/sequence_memory_game.dart';

void main() {
  group('Sequence Memory Game', () {
    test('Easy difficulty creates sequence of 3', () {
      final game = SequenceMemoryGame(difficulty: 1);

      expect(game.sequence.length, 3);
    });

    test('Medium difficulty creates sequence of 4', () {
      final game = SequenceMemoryGame(difficulty: 2);

      expect(game.sequence.length, 4);
    });

    test('Hard difficulty creates sequence of 5', () {
      final game = SequenceMemoryGame(difficulty: 3);

      expect(game.sequence.length, 5);
    });

    test('Correct sequence is detected', () {
      final game = SequenceMemoryGame(difficulty: 1);

      for (final item in game.sequence) {
        game.addAnswer(item);
      }

      expect(game.isComplete, true);
      expect(game.isCorrect, true);
    });

    test('Incorrect sequence is detected', () {
      final game = SequenceMemoryGame(difficulty: 1);

      final wrongSequence = List<String>.from(game.sequence.reversed);

      for (final item in wrongSequence) {
        game.addAnswer(item);
      }

      expect(game.isComplete, true);
      expect(game.isCorrect, false);
    });

    test('Reset starts a new game', () {
      final game = SequenceMemoryGame(difficulty: 1);

      game.addAnswer(game.sequence[0]);
      game.reset();

      expect(game.userSequence, isEmpty);
      expect(game.isComplete, false);
    });
  });
}
