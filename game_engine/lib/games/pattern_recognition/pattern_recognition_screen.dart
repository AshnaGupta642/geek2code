import 'package:flutter/material.dart';

import '../../engine/game_adapter.dart';
import '../../engine/game_engine.dart';
import '../../engine/result_manager.dart';
import '../../models/game_result.dart';
import '../../services/adaptive_difficulty.dart';
import '../../services/performance_tracker.dart';
import 'pattern_recognition_game.dart';

class PatternRecognitionScreen extends StatefulWidget {
  final int difficulty;

  const PatternRecognitionScreen({
    super.key,
    this.difficulty = 1,
  });

  @override
  State<PatternRecognitionScreen> createState() =>
      _PatternRecognitionScreenState();
}

class _PatternRecognitionScreenState
    extends State<PatternRecognitionScreen> {
  late PatternRecognitionGame game;

  final GameEngine gameEngine = GameEngine();
  final ResultManager resultManager = ResultManager();

  late GameAdapter gameAdapter;

  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty =
      AdaptiveDifficulty();

  int currentDifficulty = 1;
  int nextDifficulty = 1;

  @override
  void initState() {
    super.initState();

    currentDifficulty = widget.difficulty;

    game = PatternRecognitionGame(
      difficulty: currentDifficulty,
    );

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

    tracker.recordAttempt(
      correct: game.isCorrect,
    );

    setState(() {});

    if (game.isComplete) {
      Future.delayed(
        const Duration(milliseconds: 400),
        () {
          if (!mounted) return;
          _showGameCompletedDialog();
        },
      );
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
      sessionId:
          DateTime.now().millisecondsSinceEpoch.toString(),
      completionRate: 1.0,
    );

    resultManager.addResult(result);

    nextDifficulty =
        adaptiveDifficulty.calculateNextDifficulty(
      currentDifficulty: playedDifficulty,
      accuracy: tracker.accuracy,
      averageResponseTime:
          tracker.averageResponseTime,
    );

    debugPrint(
      'Game Result: ${result.toJson()}',
    );

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
            game.isCorrect
                ? 'Excellent! 🎉'
                : 'Good try! 👍',
            style: const TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
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
            '${adaptiveDifficulty.getDifficultyLabel(
              nextDifficulty,
            )}',
            style: const TextStyle(
              fontSize: 21,
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);

                setState(() {
                  currentDifficulty = nextDifficulty;

                  game = PatternRecognitionGame(
                    difficulty: currentDifficulty,
                  );

                  gameEngine.startGame(game);

                  gameAdapter = GameAdapter(
                    gameId: game.gameId,
                    difficulty: currentDifficulty,
                  );

                  tracker.startGame();
                  tracker.startResponseTimer();
                });
              },
              child: const Text(
                'Next Round',
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
    gameEngine.endGame();
    super.dispose();
  }

  // ------------------------------------------------------------
  // UI
  // ------------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Pattern Recognition',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 18),

            Text(
              'Difficulty: '
              '${adaptiveDifficulty.getDifficultyLabel(
                currentDifficulty,
              )}',
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w600,
              ),
            ),

            const SizedBox(height: 14),

            const Text(
              'What comes next?',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 25),

            // Pattern
            Container(
              margin: const EdgeInsets.symmetric(
                horizontal: 20,
              ),
              padding: const EdgeInsets.symmetric(
                vertical: 25,
                horizontal: 15,
              ),
              decoration: BoxDecoration(
                borderRadius:
                    BorderRadius.circular(20),
                color: Colors.blue.shade50,
                border: Border.all(
                  color: Colors.blue.shade700,
                  width: 3,
                ),
              ),
              child: Row(
                mainAxisAlignment:
                    MainAxisAlignment.center,
                children: [
                  ...game.pattern.map(
                    (symbol) => Padding(
                      padding:
                          const EdgeInsets.symmetric(
                        horizontal: 8,
                      ),
                      child: Text(
                        symbol,
                        style: const TextStyle(
                          fontSize: 48,
                        ),
                      ),
                    ),
                  ),
                  const Padding(
                    padding: EdgeInsets.symmetric(
                      horizontal: 8,
                    ),
                    child: Text(
                      '?',
                      style: TextStyle(
                        fontSize: 48,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 35),

            const Text(
              'Choose the correct symbol',
              style: TextStyle(
                fontSize: 21,
                fontWeight: FontWeight.w600,
              ),
            ),

            const SizedBox(height: 20),

            Expanded(
              child: GridView.builder(
                padding: const EdgeInsets.all(25),
                itemCount: game.options.length,
                gridDelegate:
                    const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 18,
                  mainAxisSpacing: 18,
                ),
                itemBuilder: (context, index) {
                  final option = game.options[index];

                  return ElevatedButton(
                    onPressed: game.isComplete
                        ? null
                        : () => _selectAnswer(option),
                    style: ElevatedButton.styleFrom(
                      shape: RoundedRectangleBorder(
                        borderRadius:
                            BorderRadius.circular(20),
                      ),
                    ),
                    child: Text(
                      option,
                      style: const TextStyle(
                        fontSize: 50,
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}