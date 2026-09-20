import 'package:flutter/material.dart';

import '../../engine/game_adapter.dart';
import '../../engine/game_engine.dart';
import '../../engine/result_manager.dart';
import '../../models/game_result.dart';
import '../../services/adaptive_difficulty.dart';
import '../../services/game_api_service.dart';
import '../../services/performance_tracker.dart';
import 'pattern_recognition_game.dart';

class PatternRecognitionScreen extends StatefulWidget {
  final int difficulty;

  const PatternRecognitionScreen({super.key, this.difficulty = 1});

  @override
  State<PatternRecognitionScreen> createState() =>
      _PatternRecognitionScreenState();
}

class _PatternRecognitionScreenState extends State<PatternRecognitionScreen> {
  late PatternRecognitionGame game;

  final GameEngine gameEngine = GameEngine();
  final ResultManager resultManager = ResultManager();
  final GameApiService gameApiService = GameApiService();
  late GameAdapter gameAdapter;

  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty = AdaptiveDifficulty();

  int currentDifficulty = 1;
  int nextDifficulty = 1;

  @override
  void initState() {
    super.initState();

    currentDifficulty = widget.difficulty;

    game = PatternRecognitionGame(difficulty: currentDifficulty);

    gameEngine.startGame(game);

    gameAdapter = GameAdapter(
      gameId: game.gameId,
      difficulty: currentDifficulty,
    );

    tracker.startGame();
    tracker.startResponseTimer();
  }

  // ------------------------------------------------------------
  // ANSWER
  // ------------------------------------------------------------

  void _selectAnswer(String answer) {
    if (game.isComplete) {
      return;
    }

    game.selectAnswer(answer);

    tracker.recordAttempt(correct: game.isCorrect);

    setState(() {});

    if (game.isComplete) {
      Future.delayed(const Duration(milliseconds: 400), () {
        if (!mounted) return;
        _showGameCompletedDialog();
      });
    }
  }

  // ------------------------------------------------------------
  // RESULT
  // ------------------------------------------------------------

  void _showGameCompletedDialog() {
    if (!mounted) return;

    final int playedDifficulty = currentDifficulty;

    final GameResult result = gameAdapter.createResult(
      tracker: tracker,
      patientId: 'patient_001',
      sessionId: DateTime.now().millisecondsSinceEpoch.toString(),
      completionRate: 1.0,
    );
    gameApiService.submitResult(result).then((success) {
      if (success) {
        debugPrint('Pattern Recognition result submitted successfully.');
      } else {
        debugPrint('Failed to submit Pattern Recognition result.');
      }
    });

    resultManager.addResult(result);

    nextDifficulty = adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: playedDifficulty,
      accuracy: tracker.accuracy,
      averageResponseTime: tracker.averageResponseTime,
    );

    debugPrint('Game Result: ${result.toJson()}');

    debugPrint(
      'Total games recorded: '
      '${resultManager.totalGames}',
    );

    gameEngine.endGame();

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return AlertDialog(
          title: Text(
            game.isCorrect ? 'Excellent! 🎉' : 'Good try! 👍',
            style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
          ),
          content: Text(
            'Pattern completed!\n\n'
            'Answer: '
            '${game.isCorrect ? 'Correct' : 'Incorrect'}\n'
            'Accuracy: '
            '${(tracker.accuracy * 100).toStringAsFixed(0)}%\n'
            'Response time: '
            '${tracker.averageResponseTime.toStringAsFixed(1)} sec\n\n'
            'Next difficulty: '
            '${adaptiveDifficulty.getDifficultyLabel(nextDifficulty)}',
            style: const TextStyle(fontSize: 21),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);

                setState(() {
                  currentDifficulty = nextDifficulty;

                  game = PatternRecognitionGame(difficulty: currentDifficulty);

                  gameEngine.startGame(game);

                  gameAdapter = GameAdapter(
                    gameId: game.gameId,
                    difficulty: currentDifficulty,
                  );

                  tracker.startGame();
                  tracker.startResponseTimer();
                });
              },
              child: const Text('Next Round', style: TextStyle(fontSize: 20)),
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    gameEngine.endGame();
    super.dispose();
  }

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
          'Pattern Recognition',
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

                    const SizedBox(height: 24),

                    _buildPattern(width),

                    const SizedBox(height: 28),

                    const Text(
                      'Choose the correct symbol',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF202B28),
                      ),
                      textAlign: TextAlign.center,
                    ),

                    const SizedBox(height: 16),

                    _buildOptions(width),
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
          'What comes next?',
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
            color: Color(0xFF202B28),
          ),
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: 8),

        const Text(
          'Look carefully and find the missing symbol',
          style: TextStyle(fontSize: 17, color: Color(0xFF5F625F)),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildPattern(double screenWidth) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 24),
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
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ...game.pattern.map(
              (symbol) => _buildPatternSymbol(symbol, screenWidth),
            ),

            _buildPatternSymbol('?', screenWidth, isQuestion: true),
          ],
        ),
      ),
    );
  }

  Widget _buildPatternSymbol(
    String symbol,
    double screenWidth, {
    bool isQuestion = false,
  }) {
    final double size = screenWidth < 400 ? 58 : 68;

    return Container(
      width: size,
      height: size,
      margin: const EdgeInsets.symmetric(horizontal: 5),
      decoration: BoxDecoration(
        color: isQuestion ? const Color(0xFFE6F0E8) : const Color(0xFFF9D58A),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isQuestion ? const Color(0xFF4F8A68) : const Color(0xFFE4B85F),
          width: 2,
        ),
      ),
      child: Center(
        child: Text(
          symbol,
          style: TextStyle(
            fontSize: isQuestion ? 36 : 34,
            fontWeight: isQuestion ? FontWeight.bold : FontWeight.normal,
          ),
        ),
      ),
    );
  }

  Widget _buildOptions(double screenWidth) {
    final double spacing = 12;

    final double buttonWidth = (screenWidth - 40 - spacing) / 2;

    return Wrap(
      alignment: WrapAlignment.center,
      spacing: spacing,
      runSpacing: spacing,
      children: game.options.map((option) {
        return SizedBox(
          width: buttonWidth.clamp(130.0, 210.0),
          height: 100,
          child: ElevatedButton(
            onPressed: game.isComplete ? null : () => _selectAnswer(option),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFF9D58A),
              foregroundColor: const Color(0xFF202B28),
              elevation: 0,
              padding: EdgeInsets.zero,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
            ),
            child: Text(option, style: const TextStyle(fontSize: 44)),
          ),
        );
      }).toList(),
    );
  }
}
