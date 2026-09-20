import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/services/adaptive_difficulty.dart';

void main() {
  final adaptiveDifficulty = AdaptiveDifficulty();

  test('increases difficulty for excellent performance', () {
    final result = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: 1,
      accuracy: 0.90,
      averageResponseTime: 4,
    );

    expect(result, 2);
  });

  test('decreases difficulty for poor accuracy', () {
    final result = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: 2,
      accuracy: 0.40,
      averageResponseTime: 6,
    );

    expect(result, 1);
  });

  test('decreases difficulty for slow response', () {
    final result = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: 2,
      accuracy: 0.70,
      averageResponseTime: 12,
    );

    expect(result, 1);
  });

  test('keeps difficulty at 1', () {
    final result = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: 1,
      accuracy: 0.20,
      averageResponseTime: 15,
    );

    expect(result, 1);
  });

  test('keeps difficulty at 3', () {
    final result = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: 3,
      accuracy: 0.95,
      averageResponseTime: 3,
    );

    expect(result, 3);
  });

  test('keeps difficulty unchanged for average performance', () {
    final result = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: 2,
      accuracy: 0.70,
      averageResponseTime: 7,
    );

    expect(result, 2);
  });

  test('returns correct difficulty labels', () {
    expect(adaptiveDifficulty.getDifficultyLabel(1), 'Easy');
    expect(adaptiveDifficulty.getDifficultyLabel(2), 'Medium');
    expect(adaptiveDifficulty.getDifficultyLabel(3), 'Hard');
  });
}
