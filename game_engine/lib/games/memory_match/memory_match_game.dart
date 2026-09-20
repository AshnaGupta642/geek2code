import 'dart:math';

import '../../engine/cognitive_game.dart';
import 'memory_card.dart';

class MemoryMatchGame implements CognitiveGame {
  @override
  String get gameId => 'memory_match';

  @override
  final int difficulty;

  late List<MemoryCard> cards;

  @override
  int score = 0;

  @override
  int attempts = 0;

  @override
  int mistakes = 0;

  bool _isGameComplete = false;

  @override
  bool get isComplete => _isGameComplete;

  bool get isGameComplete => _isGameComplete;
  int? firstCardIndex;
  int? secondCardIndex;

  MemoryMatchGame({required this.difficulty}) {
    _initializeGame();
  }

  void _initializeGame() {
    final List<String> symbols;

    switch (difficulty) {
      case 1:
        symbols = ['🐶', '🐱'];
        break;

      case 2:
        symbols = ['🐶', '🐱', '🍎', '🚗'];
        break;

      case 3:
        symbols = ['🐶', '🐱', '🍎', '🚗', '🌸', '🏠'];
        break;

      default:
        throw ArgumentError('Difficulty must be between 1 and 3');
    }

    cards = [];

    for (int i = 0; i < symbols.length; i++) {
      cards.add(MemoryCard(id: '${symbols[i]}_1', image: symbols[i]));

      cards.add(MemoryCard(id: '${symbols[i]}_2', image: symbols[i]));
    }

    cards.shuffle(Random());
  }

  bool flipCard(int index) {
    if (_isGameComplete) {
      return false;
    }

    if (index < 0 || index >= cards.length) {
      return false;
    }

    final card = cards[index];

    if (card.isFlipped || card.isMatched) {
      return false;
    }

    card.isFlipped = true;

    if (firstCardIndex == null) {
      firstCardIndex = index;
      return true;
    }

    secondCardIndex = index;
    attempts++;

    final firstCard = cards[firstCardIndex!];
    final secondCard = cards[secondCardIndex!];

    if (firstCard.image == secondCard.image) {
      firstCard.isMatched = true;
      secondCard.isMatched = true;

      score++;
    } else {
      mistakes++;
    }

    _checkGameComplete();

    return true;
  }

  void hideMismatchedCards() {
    if (firstCardIndex == null || secondCardIndex == null) {
      return;
    }

    final firstCard = cards[firstCardIndex!];
    final secondCard = cards[secondCardIndex!];

    if (!firstCard.isMatched && !secondCard.isMatched) {
      firstCard.isFlipped = false;
      secondCard.isFlipped = false;
    }

    firstCardIndex = null;
    secondCardIndex = null;
  }

  void _checkGameComplete() {
    _isGameComplete = cards.every((card) => card.isMatched);
  }

  @override
  void reset() {
    score = 0;
    attempts = 0;
    mistakes = 0;

    firstCardIndex = null;
    secondCardIndex = null;

    _isGameComplete = false;

    _initializeGame();
  }
}
