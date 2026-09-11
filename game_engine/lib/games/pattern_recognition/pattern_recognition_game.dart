import 'dart:math';

import '../../engine/cognitive_game.dart';

class PatternRecognitionGame implements CognitiveGame {
  @override
  final int difficulty;

  @override
  String get gameId => 'pattern_recognition';

  @override
  bool get isComplete => _isComplete;

  @override
  int get score => isCorrect ? 1 : 0;

  @override
  int get attempts => _isComplete ? 1 : 0;

  @override
  int get mistakes => _isComplete && !isCorrect ? 1 : 0;

  late List<String> pattern;
  late String correctAnswer;
  late List<String> options;

  bool isCorrect = false;
  bool _isComplete = false;

  PatternRecognitionGame({
    required this.difficulty,
  }) {
    _initializeGame();
  }

  int get patternLength {
    switch (difficulty) {
      case 1:
        return 3;
      case 2:
        return 4;
      case 3:
        return 5;
      default:
        throw ArgumentError(
          'Difficulty must be between 1 and 3',
        );
    }
  }

  void _initializeGame() {
    final symbols = [
      '🔴',
      '🔵',
      '🟢',
      '🟡',
    ];

    symbols.shuffle(Random());

    final first = symbols[0];
    final second = symbols[1];

    // Example:
    // 🔴 🔵 🔴 ?
    // Correct answer = 🔵
    pattern = List.generate(
      patternLength,
      (index) {
        return index.isEven ? first : second;
      },
    );

    // The next position is patternLength.
    // Even index -> first symbol
    // Odd index  -> second symbol
    correctAnswer =
        patternLength.isEven ? first : second;

    options = List<String>.from(symbols);
    options.shuffle(Random());
  }

  void selectAnswer(String answer) {
    if (_isComplete) {
      return;
    }

    isCorrect = answer == correctAnswer;
    _isComplete = true;
  }

  @override
  void reset() {
    isCorrect = false;
    _isComplete = false;

    _initializeGame();
  }
}