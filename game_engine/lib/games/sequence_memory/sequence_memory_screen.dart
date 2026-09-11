import 'dart:async';

import 'package:flutter/material.dart';

import '../../services/adaptive_difficulty.dart';
import '../../services/performance_tracker.dart';
import 'sequence_memory_game.dart';

class SequenceMemoryScreen extends StatefulWidget {
  final int difficulty;

  const SequenceMemoryScreen({
    super.key,
    this.difficulty = 1,
  });

  @override
  State<SequenceMemoryScreen> createState() =>
      _SequenceMemoryScreenState();
}

class _SequenceMemoryScreenState
    extends State<SequenceMemoryScreen> {
  late SequenceMemoryGame game;

  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty =
      AdaptiveDifficulty();

  int currentDifficulty = 1;
  int nextDifficulty = 1;

  bool showingSequence = true;
  Timer? sequenceTimer;

  @override
  void initState() {
    super.initState();

    currentDifficulty = widget.difficulty;

    game = SequenceMemoryGame(
      difficulty: currentDifficulty,
    );

    tracker.startGame();

    _showSequence();
  }

  void _showSequence() {
    setState(() {
      showingSequence = true;
    });

    sequenceTimer = Timer(
      const Duration(seconds: 3),
      () {
        if (!mounted) return;

        setState(() {
          showingSequence = false;
        });

        tracker.startResponseTimer();
      },
    );
  }

  void _selectItem(String item) {
    if (showingSequence || game.isComplete) {
      return;
    }

    game.addAnswer(item);

    if (game.isComplete) {
      tracker.recordAttempt(
        correct: game.isCorrect,
      );

      setState(() {});

      Future.delayed(
        const Duration(milliseconds: 500),
        () {
          if (!mounted) return;
          _showGameCompletedDialog();
        },
      );

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

    final accuracy =
        (tracker.accuracy * 100).toStringAsFixed(0);

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          title: const Text(
            'Great job! 🎉',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          content: Text(
            'You completed the sequence!\n\n'
            'Score: ${game.score}\n'
            'Accuracy: $accuracy%\n\n'
            'Next round difficulty: '
            '${adaptiveDifficulty.getDifficultyLabel(nextDifficulty)}',
            style: const TextStyle(
              fontSize: 22,
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);

                setState(() {
                  currentDifficulty = nextDifficulty;

                  game = SequenceMemoryGame(
                    difficulty: currentDifficulty,
                  );

                  tracker.startGame();

                  showingSequence = true;

                  _showSequence();
                });
              },
              child: const Text(
                'Play Again',
                style: TextStyle(
                  fontSize: 20,
                ),
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
      appBar: AppBar(
        title: const Text(
          'Sequence Memory',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              const SizedBox(height: 20),

              Text(
                showingSequence
                    ? 'Remember this sequence'
                    : 'Repeat the sequence',
                style: const TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 30),

              if (showingSequence)
                _buildSequenceDisplay()
              else
                _buildUserSequence(),

              const Spacer(),

              if (!showingSequence)
                _buildOptions(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSequenceDisplay() {
    return Wrap(
      alignment: WrapAlignment.center,
      spacing: 20,
      runSpacing: 20,
      children: game.sequence.map((item) {
        return Container(
          width: 90,
          height: 90,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              width: 3,
            ),
          ),
          child: Center(
            child: Text(
              item,
              style: const TextStyle(
                fontSize: 45,
              ),
            ),
          ),
        );
      }).toList(),
    );
  }

  Widget _buildUserSequence() {
    return Column(
      children: [
        const Text(
          'Your sequence:',
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 15),
        Wrap(
          alignment: WrapAlignment.center,
          spacing: 12,
          children: game.userSequence.map((item) {
            return Text(
              item,
              style: const TextStyle(
                fontSize: 40,
              ),
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildOptions() {
    final options = [
      '🍎',
      '🥛',
      '🍌',
      '🥣',
      '☕',
      '🌸',
      '🚗',
      '🐶',
    ];

    return Wrap(
      alignment: WrapAlignment.center,
      spacing: 12,
      runSpacing: 12,
      children: options.map((item) {
        return SizedBox(
          width: 80,
          height: 70,
          child: ElevatedButton(
            onPressed: () => _selectItem(item),
            child: Text(
              item,
              style: const TextStyle(
                fontSize: 32,
              ),
            ),
          ),
        );
      }).toList(),
    );
  }
}