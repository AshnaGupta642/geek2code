import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/games/memory_match/memory_match_game.dart';

void main() {
  group('Memory Match Game', () {
    test('Easy difficulty creates 4 cards', () {
      final game = MemoryMatchGame(difficulty: 1);

      expect(game.cards.length, 4);
    });

    test('Medium difficulty creates 8 cards', () {
      final game = MemoryMatchGame(difficulty: 2);

      expect(game.cards.length, 8);
    });

    test('Hard difficulty creates 12 cards', () {
      final game = MemoryMatchGame(difficulty: 3);

      expect(game.cards.length, 12);
    });

    test('Cards start face down', () {
      final game = MemoryMatchGame(difficulty: 1);

      for (final card in game.cards) {
        expect(card.isFlipped, false);
        expect(card.isMatched, false);
      }
    });

    test('Flipping a card works', () {
      final game = MemoryMatchGame(difficulty: 1);

      final result = game.flipCard(0);

      expect(result, true);
      expect(game.cards[0].isFlipped, true);
    });

    test('Cannot flip the same card twice', () {
      final game = MemoryMatchGame(difficulty: 1);

      game.flipCard(0);

      final result = game.flipCard(0);

      expect(result, false);
    });

    test('Two cards count as one attempt', () {
      final game = MemoryMatchGame(difficulty: 1);

      game.flipCard(0);
      game.flipCard(1);

      expect(game.attempts, 1);
    });

    test('Reset starts the game again', () {
      final game = MemoryMatchGame(difficulty: 1);

      game.flipCard(0);
      game.flipCard(1);

      game.reset();

      expect(game.score, 0);
      expect(game.attempts, 0);
      expect(game.mistakes, 0);
      expect(game.isGameComplete, false);
    });
  });
}