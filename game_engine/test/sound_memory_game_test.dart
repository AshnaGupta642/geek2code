import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/games/sound_memory/sound_memory_game.dart';

void main() {
  group('Sound Memory Game', () {
    test('Easy difficulty creates sequence of 3', () {
      final game = SoundMemoryGame(difficulty: 1);

      expect(game.sequence.length, 3);
    });

    test('Medium difficulty creates sequence of 4', () {
      final game = SoundMemoryGame(difficulty: 2);

      expect(game.sequence.length, 4);
    });

    test('Hard difficulty creates sequence of 5', () {
      final game = SoundMemoryGame(difficulty: 3);

      expect(game.sequence.length, 5);
    });

    test('Correct sequence is detected', () {
      final game = SoundMemoryGame(difficulty: 1);

      for (final sound in game.sequence) {
        game.addAnswer(sound);
      }

      expect(game.isComplete, true);
      expect(game.isCorrect, true);
    });

    test('Incorrect sequence is detected', () {
      final game = SoundMemoryGame(difficulty: 1);

      final wrongSequence = List<int>.from(game.sequence.reversed);

      for (final sound in wrongSequence) {
        game.addAnswer(sound);
      }

      expect(game.isComplete, true);
      expect(game.isCorrect, false);
    });

    test('Reset starts a new game', () {
      final game = SoundMemoryGame(difficulty: 1);

      game.addAnswer(game.sequence[0]);
      game.reset();

      expect(game.userSequence, isEmpty);
      expect(game.isComplete, false);
    });
  });
}
