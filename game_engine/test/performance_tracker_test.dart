import 'package:flutter_test/flutter_test.dart';
import 'package:game_engine/services/performance_tracker.dart';

void main() {
  group('PerformanceTracker', () {
    test('starts with zero values', () {
      final tracker = PerformanceTracker();

      expect(tracker.attempts, 0);
      expect(tracker.mistakes, 0);
      expect(tracker.score, 0);
      expect(tracker.hintsUsed, 0);
      expect(tracker.accuracy, 0);
    });

    test('records a correct attempt', () {
      final tracker = PerformanceTracker();

      tracker.startGame();
      tracker.startResponseTimer();
      tracker.recordAttempt(correct: true);

      expect(tracker.attempts, 1);
      expect(tracker.score, 1);
      expect(tracker.mistakes, 0);
      expect(tracker.accuracy, 1);
    });

    test('records an incorrect attempt', () {
      final tracker = PerformanceTracker();

      tracker.startGame();
      tracker.startResponseTimer();
      tracker.recordAttempt(correct: false);

      expect(tracker.attempts, 1);
      expect(tracker.score, 0);
      expect(tracker.mistakes, 1);
      expect(tracker.accuracy, 0);
    });

    test('calculates accuracy correctly', () {
      final tracker = PerformanceTracker();

      tracker.startGame();

      tracker.recordAttempt(correct: true);
      tracker.recordAttempt(correct: true);
      tracker.recordAttempt(correct: false);
      tracker.recordAttempt(correct: false);

      expect(tracker.accuracy, 0.5);
    });

    test('tracks hints', () {
      final tracker = PerformanceTracker();

      tracker.startGame();

      tracker.useHint();
      tracker.useHint();

      expect(tracker.hintsUsed, 2);
    });

    test('calculates completion rate', () {
      final tracker = PerformanceTracker();

      expect(tracker.completionRate(completedItems: 3, totalItems: 4), 0.75);
    });

    test('reset clears performance data', () {
      final tracker = PerformanceTracker();

      tracker.startGame();
      tracker.recordAttempt(correct: true);
      tracker.useHint();

      tracker.reset();

      expect(tracker.attempts, 0);
      expect(tracker.score, 0);
      expect(tracker.mistakes, 0);
      expect(tracker.hintsUsed, 0);
    });
  });
}
