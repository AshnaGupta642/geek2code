import 'dart:async';

import 'package:flutter/material.dart';

import '../../services/adaptive_difficulty.dart';
import '../../services/game_api_service.dart';
import '../../services/performance_tracker.dart';
import 'sequence_memory_game.dart';

class SequenceMemoryScreen extends StatefulWidget {
  final int difficulty;

  const SequenceMemoryScreen({super.key, this.difficulty = 1});

  @override
  State<SequenceMemoryScreen> createState() => _SequenceMemoryScreenState();
}

class _SequenceMemoryScreenState extends State<SequenceMemoryScreen> {
  late SequenceMemoryGame game;

  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty = AdaptiveDifficulty();
  final GameApiService gameApiService = GameApiService();

  int currentDifficulty = 1;
  int nextDifficulty = 1;

  bool showingSequence = true;
  Timer? sequenceTimer;

  @override
  void initState() {
    super.initState();

    currentDifficulty = widget.difficulty;

    game = SequenceMemoryGame(difficulty: currentDifficulty);

    tracker.startGame();

    _showSequence();
  }

  void _showSequence() {
    sequenceTimer?.cancel();

    setState(() {
      showingSequence = true;
    });

    sequenceTimer = Timer(const Duration(seconds: 3), () {
      if (!mounted) return;

      setState(() {
        showingSequence = false;
      });

      tracker.startResponseTimer();
    });
  }

  void _selectItem(String item) {
    if (showingSequence || game.isComplete) {
      return;
    }

    game.addAnswer(item);

    if (game.isComplete) {
      tracker.recordAttempt(correct: game.isCorrect);

      setState(() {});

      Future.delayed(const Duration(milliseconds: 500), () {
        if (!mounted) return;
        _showGameCompletedDialog();
      });

      return;
    }

    setState(() {});
  }

  void _showGameCompletedDialog() {
    final int playedDifficulty = currentDifficulty;

    final next = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: playedDifficulty,
      accuracy: tracker.accuracy,
      averageResponseTime: tracker.averageResponseTime,
    );

    nextDifficulty = next;

    final accuracy = (tracker.accuracy * 100).toStringAsFixed(0);

    final result = tracker.createResult(
      patientId: 'patient_001',
      gameId: game.gameId,
      sessionId: DateTime.now().millisecondsSinceEpoch.toString(),
      difficulty: playedDifficulty,
      completionRate: 1.0,
    );

    gameApiService.submitResult(result).then((success) {
      if (success) {
        debugPrint('Sequence Memory result submitted successfully.');
      } else {
        debugPrint('Failed to submit Sequence Memory result.');
      }
    });

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
          ),
          title: const Text(
            'Great job! 🎉',
            style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
          ),
          content: Text(
            'You completed the sequence!\n\n'
            'Score: ${game.score}\n'
            'Accuracy: $accuracy%\n\n'
            'Next round difficulty: '
            '${adaptiveDifficulty.getDifficultyLabel(nextDifficulty)}',
            style: const TextStyle(fontSize: 20, height: 1.4),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);

                setState(() {
                  currentDifficulty = nextDifficulty;

                  game = SequenceMemoryGame(difficulty: currentDifficulty);

                  tracker.startGame();

                  showingSequence = true;

                  _showSequence();
                });
              },
              child: const Text(
                'Play Again',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    sequenceTimer?.cancel();
    super.dispose();
  }

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
          'Sequence Memory',
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

                    const SizedBox(height: 26),

                    if (showingSequence)
                      _buildSequenceDisplay(width)
                    else
                      _buildUserSequence(),

                    const SizedBox(height: 28),

                    if (!showingSequence) _buildOptions(width),
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

        const SizedBox(height: 20),

        Text(
          showingSequence ? 'Remember this sequence' : 'Repeat the sequence',
          style: const TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: Color(0xFF202B28),
          ),
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: 8),

        Text(
          showingSequence
              ? 'Watch carefully 👀'
              : 'Tap the items in the correct order',
          style: const TextStyle(fontSize: 18, color: Color(0xFF5F625F)),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildSequenceDisplay(double screenWidth) {
    final double cardSize = screenWidth >= 500 ? 92 : 82;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 22),
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
        spacing: 14,
        runSpacing: 14,
        children: game.sequence.map((item) {
          return Container(
            width: cardSize,
            height: cardSize,
            decoration: BoxDecoration(
              color: const Color(0xFFF9D58A),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: const Color(0xFFE4B85F), width: 2),
            ),
            child: Center(
              child: Text(item, style: const TextStyle(fontSize: 42)),
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildUserSequence() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
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
      child: Column(
        children: [
          const Text(
            'Your sequence',
            style: TextStyle(
              fontSize: 21,
              fontWeight: FontWeight.bold,
              color: Color(0xFF202B28),
            ),
          ),

          const SizedBox(height: 16),

          if (game.userSequence.isEmpty)
            const Text(
              'Choose the first item below',
              style: TextStyle(fontSize: 17, color: Color(0xFF777777)),
            )
          else
            Wrap(
              alignment: WrapAlignment.center,
              spacing: 12,
              runSpacing: 8,
              children: game.userSequence.map((item) {
                return Container(
                  width: 58,
                  height: 58,
                  decoration: BoxDecoration(
                    color: const Color(0xFFE6F0E8),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Center(
                    child: Text(item, style: const TextStyle(fontSize: 32)),
                  ),
                );
              }).toList(),
            ),
        ],
      ),
    );
  }

  Widget _buildOptions(double screenWidth) {
    final options = ['🍎', '🥛', '🍌', '🥣', '☕', '🌸', '🚗', '🐶'];

    final double spacing = 12;

    final double buttonWidth = (screenWidth - 40 - (spacing * 3)) / 4;

    return Column(
      children: [
        const Text(
          'Choose the next item',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Color(0xFF202B28),
          ),
        ),

        const SizedBox(height: 16),

        Wrap(
          alignment: WrapAlignment.center,
          spacing: spacing,
          runSpacing: spacing,
          children: options.map((item) {
            return SizedBox(
              width: buttonWidth.clamp(68.0, 105.0),
              height: 68,
              child: ElevatedButton(
                onPressed: () => _selectItem(item),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFF9D58A),
                  foregroundColor: const Color(0xFF202B28),
                  elevation: 0,
                  padding: EdgeInsets.zero,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(18),
                  ),
                ),
                child: Text(item, style: const TextStyle(fontSize: 31)),
              ),
            );
          }).toList(),
        ),
      ],
    );
  }
}
