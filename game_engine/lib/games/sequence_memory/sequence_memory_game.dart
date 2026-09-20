import 'dart:math';

import '../../engine/cognitive_game.dart';

class SequenceMemoryGame implements CognitiveGame {
  @override
  final int difficulty;

  @override
  String get gameId => 'sequence_memory';

  late List<String> sequence;
  List<String> userSequence = [];

  bool _isComplete = false;
  bool isCorrect = false;

  @override
  bool get isComplete => _isComplete;

  @override
  int get score => isCorrect ? 1 : 0;

  @override
  int get attempts => _isComplete ? 1 : 0;

  @override
  int get mistakes => _isComplete && !isCorrect ? 1 : 0;

  SequenceMemoryGame({required this.difficulty}) {
    _initializeGame();
  }

  int get sequenceLength {
    switch (difficulty) {
      case 1:
        return 3;
      case 2:
        return 4;
      case 3:
        return 5;
      default:
        throw ArgumentError('Difficulty must be between 1 and 3');
    }
  }

  void _initializeGame() {
    final objects = ['🍎', '🥛', '🍌', '🥣', '☕', '🌸', '🚗', '🐶'];

    objects.shuffle(Random());

    sequence = objects.take(sequenceLength).toList();
  }

  void addAnswer(String item) {
    if (_isComplete) {
      return;
    }

    userSequence.add(item);

    if (userSequence.length == sequence.length) {
      _checkAnswer();
    }
  }

  void _checkAnswer() {
    _isComplete = true;
    isCorrect = true;

    for (int i = 0; i < sequence.length; i++) {
      if (sequence[i] != userSequence[i]) {
        isCorrect = false;
        break;
      }
    }
  }

  @override
  void reset() {
    userSequence = [];
    _isComplete = false;
    isCorrect = false;

    _initializeGame();
  }
}
