import 'dart:math';

import '../../engine/cognitive_game.dart';

class PuzzleGame implements CognitiveGame {
  @override
  final int difficulty;

  @override
  String get gameId => 'puzzle';

  @override
  bool get isComplete => _isComplete;

  @override
  int get score => isCorrect ? 1 : 0;

  @override
  int get attempts => _isComplete ? 1 : 0;

  @override
  int get mistakes => _isComplete && !isCorrect ? 1 : 0;

  late List<String> correctOrder;
  late List<String> pieces;

  bool _isComplete = false;
  bool isCorrect = false;

  PuzzleGame({required this.difficulty}) {
    _initializeGame();
  }

  int get pieceCount {
    switch (difficulty) {
      case 1:
        return 4;
      case 2:
        return 6;
      case 3:
        return 9;
      default:
        throw ArgumentError('Difficulty must be between 1 and 3');
    }
  }

  void _initializeGame() {
    correctOrder = List.generate(pieceCount, (index) => '${index + 1}');

    pieces = List<String>.from(correctOrder);
    pieces.shuffle(Random());

    // Make sure the puzzle starts scrambled.
    while (_isCorrectOrder()) {
      pieces.shuffle(Random());
    }
  }

  bool _isCorrectOrder() {
    for (int i = 0; i < pieces.length; i++) {
      if (pieces[i] != correctOrder[i]) {
        return false;
      }
    }

    return true;
  }

  /// Swaps the selected piece with the piece before it.
  void swapPieceLeft(int index) {
    if (_isComplete) {
      return;
    }

    if (index <= 0 || index >= pieces.length) {
      return;
    }

    final temp = pieces[index];
    pieces[index] = pieces[index - 1];
    pieces[index - 1] = temp;
  }

  void checkPuzzle() {
    if (_isComplete) {
      return;
    }

    _isComplete = true;
    isCorrect = _isCorrectOrder();
  }

  @override
  void reset() {
    _isComplete = false;
    isCorrect = false;

    _initializeGame();
  }
}
