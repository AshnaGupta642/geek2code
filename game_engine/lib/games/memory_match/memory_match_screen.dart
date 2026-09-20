import 'dart:async';

import 'package:flutter/material.dart';

import '../../engine/game_adapter.dart';
import '../../engine/game_engine.dart';
import '../../engine/result_manager.dart';
import '../../models/game_result.dart';
import '../../services/adaptive_difficulty.dart';
import '../../services/game_api_service.dart';
import '../../services/performance_tracker.dart';
import 'memory_match_game.dart';

class MemoryMatchScreen extends StatefulWidget {
  final int difficulty;
  final String? authToken;

  const MemoryMatchScreen({super.key, this.difficulty = 1, this.authToken});

  @override
  State<MemoryMatchScreen> createState() => _MemoryMatchScreenState();
}

class _MemoryMatchScreenState extends State<MemoryMatchScreen> {
  late MemoryMatchGame game;

  // Engine layer
  final GameEngine gameEngine = GameEngine();
  final ResultManager resultManager = ResultManager();
  late GameAdapter gameAdapter;

  // Performance and adaptive difficulty
  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty = AdaptiveDifficulty();
  final GameApiService gameApiService = GameApiService();

  // Backend session
  String? backendSessionId;

  int currentDifficulty = 1;
  int nextDifficulty = 1;

  bool isProcessing = false;

  // Hint
  Timer? _hintTimer;
  final Set<int> _hintCards = {};

  @override
  void initState() {
    super.initState();

    currentDifficulty = widget.difficulty;

    game = MemoryMatchGame(difficulty: currentDifficulty);

    // Start game through the central engine.
    gameEngine.startGame(game);

    // Adapter connects this game with the result system.
    gameAdapter = GameAdapter(
      gameId: game.gameId,
      difficulty: currentDifficulty,
    );

    tracker.startGame();

    // Start backend session.
    _startBackendSession();
  }

  // ------------------------------------------------------------
  // BACKEND SESSION
  // ------------------------------------------------------------

  Future<void> _startBackendSession() async {
    final session = await gameApiService.startGame(
      gameId: game.gameId,
      authToken: widget.authToken,
    );

    if (session != null) {
      backendSessionId = session['session_id'] as String?;

      debugPrint('Backend game session started: $backendSessionId');

      debugPrint('Backend difficulty: ${session['difficulty']}');
    } else {
      debugPrint('Backend game session could not be started.');
    }
  }

  // ------------------------------------------------------------
  // HINT
  // ------------------------------------------------------------

  void _useHint() {
    if (game.isGameComplete || isProcessing) {
      return;
    }

    if (_hintCards.isNotEmpty) {
      return;
    }

    int? firstIndex;
    int? secondIndex;

    // Find an unmatched pair.
    for (int i = 0; i < game.cards.length; i++) {
      if (game.cards[i].isMatched) {
        continue;
      }

      for (int j = i + 1; j < game.cards.length; j++) {
        if (game.cards[j].isMatched) {
          continue;
        }

        if (game.cards[i].image == game.cards[j].image) {
          firstIndex = i;
          secondIndex = j;
          break;
        }
      }

      if (firstIndex != null) {
        break;
      }
    }

    if (firstIndex == null || secondIndex == null) {
      return;
    }

    tracker.useHint();

    _hintCards
      ..clear()
      ..add(firstIndex)
      ..add(secondIndex);

    setState(() {
      game.cards[firstIndex!].isFlipped = true;
      game.cards[secondIndex!].isFlipped = true;
    });

    _hintTimer?.cancel();

    _hintTimer = Timer(const Duration(milliseconds: 1200), () {
      if (!mounted) return;

      for (final index in _hintCards) {
        if (!game.cards[index].isMatched) {
          game.cards[index].isFlipped = false;
        }
      }

      _hintCards.clear();

      setState(() {});
    });
  }

  // ------------------------------------------------------------
  // CARD TAP
  // ------------------------------------------------------------

  void _onCardTapped(int index) {
    if (game.isGameComplete || isProcessing) {
      return;
    }

    _hintCards.remove(index);

    if (game.firstCardIndex == null) {
      tracker.startResponseTimer();
    }

    final bool flipped = game.flipCard(index);

    if (!flipped) {
      return;
    }

    // Second card selected.
    if (game.secondCardIndex != null) {
      final firstIndex = game.firstCardIndex!;
      final secondIndex = game.secondCardIndex!;

      final firstCard = game.cards[firstIndex];
      final secondCard = game.cards[secondIndex];

      final bool isCorrect = firstCard.image == secondCard.image;

      tracker.recordAttempt(correct: isCorrect);

      isProcessing = true;
    }

    setState(() {});

    if (game.secondCardIndex != null) {
      Future.delayed(const Duration(milliseconds: 900), () {
        if (!mounted) return;

        game.hideMismatchedCards();

        isProcessing = false;

        setState(() {});

        // Check completion after pair processing.
        if (game.isGameComplete) {
          _showGameCompletedDialog();
        }
      });
    }
  }

  // ------------------------------------------------------------
  // RESULT
  // ------------------------------------------------------------

  void _showGameCompletedDialog() {
    if (!mounted) return;

    final int playedDifficulty = currentDifficulty;

    // Create result through GameAdapter.
    final GameResult result = gameAdapter.createResult(
      tracker: tracker,
      patientId: 'patient_001',
      sessionId: backendSessionId ?? '',
      completionRate: 1.0,
    );

    // Store result centrally.
    resultManager.addResult(result);

    // Submit result to backend.
    gameApiService.submitResult(result, authToken: widget.authToken).then((
      success,
    ) {
      if (success) {
        debugPrint('Game result submitted successfully.');
      } else {
        debugPrint('Failed to submit game result.');
      }
    });

    // Calculate next difficulty.
    nextDifficulty = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: playedDifficulty,
      accuracy: tracker.accuracy,
      averageResponseTime: tracker.averageResponseTime,
    );

    debugPrint('Game Result: ${result.toJson()}');
    debugPrint('Total games recorded: ${resultManager.totalGames}');

    // Game has finished.
    gameEngine.endGame();

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          title: const Text(
            'Great job! 🎉',
            style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
          ),
          content: Text(
            'You completed the game!\n\n'
            'Score: ${game.score}\n'
            'Attempts: ${game.attempts}\n'
            'Accuracy: '
            '${(tracker.accuracy * 100).toStringAsFixed(0)}%\n'
            'Hints used: ${tracker.hintsUsed}\n\n'
            'Next round difficulty: '
            '${adaptiveDifficulty.getDifficultyLabel(nextDifficulty)}',
            style: const TextStyle(fontSize: 22),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);

                _hintTimer?.cancel();
                _hintCards.clear();

                setState(() {
                  currentDifficulty = nextDifficulty;

                  game = MemoryMatchGame(difficulty: currentDifficulty);

                  // Start the new game through GameEngine.
                  gameEngine.startGame(game);

                  // Create adapter for the new difficulty.
                  gameAdapter = GameAdapter(
                    gameId: game.gameId,
                    difficulty: currentDifficulty,
                  );

                  tracker.startGame();

                  // Start a new backend session.
                  backendSessionId = null;
                  _startBackendSession();

                  isProcessing = false;
                });
              },
              child: const Text('Play Again', style: TextStyle(fontSize: 20)),
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    _hintTimer?.cancel();

    // Make sure the engine does not keep
    // a reference to the screen's game.
    gameEngine.endGame();

    super.dispose();
  }

  // ------------------------------------------------------------
  // UI
  // ------------------------------------------------------------

  // ------------------------------------------------------------
  // UI
  // ------------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF7F1E3),
      appBar: AppBar(
        backgroundColor: const Color(0xFFF7F1E3),
        elevation: 0,
        toolbarHeight: 68,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new, size: 22),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          'Memory Match',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Color(0xFF202B28),
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final width = constraints.maxWidth;
            final height = constraints.maxHeight;

            final horizontalPadding = width < 500 ? 20.0 : 28.0;

            return SingleChildScrollView(
              padding: EdgeInsets.fromLTRB(
                horizontalPadding,
                12,
                horizontalPadding,
                24,
              ),
              child: ConstrainedBox(
                constraints: BoxConstraints(minHeight: height - 36),
                child: Column(
                  children: [
                    _buildGameHeader(),

                    const SizedBox(height: 18),

                    _buildHintButton(),

                    const SizedBox(height: 20),

                    _buildGameBoard(width),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  Widget _buildGameHeader() {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFFE6F0E8),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            'Difficulty: '
            '${adaptiveDifficulty.getDifficultyLabel(currentDifficulty)}',
            style: const TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.w600,
              color: Color(0xFF205A46),
            ),
          ),
        ),

        const SizedBox(height: 18),

        const Text(
          'Find the matching pairs',
          style: TextStyle(
            fontSize: 27,
            fontWeight: FontWeight.bold,
            color: Color(0xFF202B28),
          ),
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: 8),

        Text(
          'Remember where each picture is',
          style: TextStyle(fontSize: 17, color: Colors.grey.shade700),
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: 12),

        Container(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(18),
          ),
          child: Text(
            'Score: ${game.score}',
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Color(0xFF202B28),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildHintButton() {
    return SizedBox(
      width: 150,
      height: 52,
      child: ElevatedButton.icon(
        onPressed: (_hintCards.isNotEmpty || isProcessing) ? null : _useHint,
        icon: const Icon(Icons.lightbulb_outline, size: 23),
        label: const Text(
          'Hint',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFFF9D58A),
          foregroundColor: const Color(0xFF202B28),
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
          ),
        ),
      ),
    );
  }

  Widget _buildGameBoard(double screenWidth) {
    final int columns = game.cards.length <= 4 ? 2 : 3;

    final double spacing = 12;

    final double availableWidth = screenWidth - 40 - ((columns - 1) * spacing);

    final double cardSize = (availableWidth / columns).clamp(75.0, 120.0);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.06),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Wrap(
        alignment: WrapAlignment.center,
        spacing: spacing,
        runSpacing: spacing,
        children: List.generate(game.cards.length, (index) {
          return SizedBox(
            width: cardSize,
            height: cardSize,
            child: _buildCard(index),
          );
        }),
      ),
    );
  }

  Widget _buildCard(int index) {
    final card = game.cards[index];

    final bool showContent = card.isFlipped || card.isMatched;

    return GestureDetector(
      onTap: () => _onCardTapped(index),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: card.isMatched
              ? const Color(0xFFCDE8D5)
              : card.isFlipped
              ? Colors.white
              : const Color(0xFFF9D58A),
          border: Border.all(
            color: card.isMatched
                ? const Color(0xFF4F8A68)
                : const Color(0xFFE4B85F),
            width: 2.5,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.08),
              blurRadius: 5,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Center(
          child: AnimatedSwitcher(
            duration: const Duration(milliseconds: 180),
            child: Text(
              showContent ? card.image : '❓',
              key: ValueKey('${index}_${showContent}_${card.image}'),
              style: const TextStyle(fontSize: 42),
            ),
          ),
        ),
      ),
    );
  }
}
