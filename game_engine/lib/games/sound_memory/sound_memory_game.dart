import 'dart:math';

import '../../engine/cognitive_game.dart';

class SoundMemoryGame implements CognitiveGame {
  @override
  final int difficulty;

  @override
  String get gameId => 'sound_memory';

  @override
  bool get isComplete => _isComplete;

  @override
  int get score => isCorrect ? 1 : 0;

  @override
  int get attempts => _isComplete ? 1 : 0;

  @override
  int get mistakes => _isComplete && !isCorrect ? 1 : 0;

  late List<int> sequence;

  final List<int> userSequence = [];

  bool _isComplete = false;
  bool isCorrect = false;

  SoundMemoryGame({required this.difficulty}) {
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
    final sounds = [0, 1, 2, 3, 4];

    sounds.shuffle(Random());

    sequence = sounds.take(sequenceLength).toList();
  }

  void addAnswer(int sound) {
    if (_isComplete) {
      return;
    }

    // Prevent extra answers after the required
    // sequence length has been reached.
    if (userSequence.length >= sequence.length) {
      return;
    }

    userSequence.add(sound);

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
    userSequence.clear();

    _isComplete = false;
    isCorrect = false;

    _initializeGame();
  }
}
