import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/services/game_progress_manager.dart';

void main() {
  group('GameProgressManager', () {
    test('starts every game at difficulty 1', () {
      final manager = GameProgressManager();

      expect(manager.getDifficulty('memory_match'), 1);
      expect(manager.getDifficulty('sequence_memory'), 1);
    });

    test('increases difficulty after good performance', () {
      final manager = GameProgressManager();

      final nextDifficulty = manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.90,
        averageResponseTime: 4,
      );

      expect(nextDifficulty, 2);
      expect(manager.getDifficulty('memory_match'), 2);
    });

    test('decreases difficulty after poor performance', () {
      final manager = GameProgressManager();

      manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.90,
        averageResponseTime: 4,
      );

      final nextDifficulty = manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.40,
        averageResponseTime: 12,
      );

      expect(nextDifficulty, 1);
    });

    test('keeps different games independent', () {
      final manager = GameProgressManager();

      manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.90,
        averageResponseTime: 4,
      );

      expect(manager.getDifficulty('memory_match'), 2);
      expect(manager.getDifficulty('puzzle'), 1);
    });

    test('does not go above difficulty 3', () {
      final manager = GameProgressManager();

      manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.95,
        averageResponseTime: 3,
      );

      manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.95,
        averageResponseTime: 3,
      );

      manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.95,
        averageResponseTime: 3,
      );

      expect(manager.getDifficulty('memory_match'), 3);
    });

    test('can reset a game to difficulty 1', () {
      final manager = GameProgressManager();

      manager.updateDifficulty(
        gameId: 'memory_match',
        accuracy: 0.95,
        averageResponseTime: 3,
      );

      manager.resetGameProgress('memory_match');

      expect(manager.getDifficulty('memory_match'), 1);
    });
  });
}