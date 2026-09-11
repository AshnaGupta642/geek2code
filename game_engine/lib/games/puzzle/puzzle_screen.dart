import 'package:flutter/material.dart';

import '../../engine/game_adapter.dart';
import '../../engine/game_engine.dart';
import '../../engine/result_manager.dart';
import '../../models/game_result.dart';
import '../../services/adaptive_difficulty.dart';
import '../../services/performance_tracker.dart';
import 'puzzle_game.dart';

class PuzzleScreen extends StatefulWidget {
  final int difficulty;

  const PuzzleScreen({
    super.key,
    this.difficulty = 1,
  });

  @override
  State<PuzzleScreen> createState() => _PuzzleScreenState();
}

class _PuzzleScreenState extends State<PuzzleScreen> {
  late PuzzleGame game;

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

    game = PuzzleGame(
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
  // MOVE PIECE
  // ------------------------------------------------------------

  void _movePiece(int index) {
    if (game.isComplete) {
      return;
    }

    game.swapPieceLeft(index);

    setState(() {});
  }

  // ------------------------------------------------------------
  // CHECK PUZZLE
  // ------------------------------------------------------------

  void _checkPuzzle() {
    if (game.isComplete) {
      return;
    }

    game.checkPuzzle();

    tracker.recordAttempt(
      correct: game.isCorrect,
    );

    setState(() {});

    _showGameCompletedDialog();
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
      completionRate: game.isCorrect ? 1.0 : 0.0,
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
            game.isCorrect
                ? 'Puzzle completed correctly!\n\n'
                    'Accuracy: '
                    '${(tracker.accuracy * 100).toStringAsFixed(0)}%\n'
                    'Response time: '
                    '${tracker.averageResponseTime.toStringAsFixed(1)} sec\n\n'
                    'Next difficulty: '
                    '${adaptiveDifficulty.getDifficultyLabel(nextDifficulty)}'
                : 'The pieces are not in the correct order.\n\n'
                    'Try again and remember the correct sequence!',
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

                  game = PuzzleGame(
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
          'Puzzle',
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
              '${adaptiveDifficulty.getDifficultyLabel(currentDifficulty)}',
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w600,
              ),
            ),

            const SizedBox(height: 14),

            const Text(
              'Arrange the pieces in order',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 23,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 12),

            Text(
              '${game.pieceCount} pieces',
              style: const TextStyle(
                fontSize: 19,
              ),
            ),

            const SizedBox(height: 25),

            Expanded(
              child: GridView.builder(
                padding: const EdgeInsets.all(25),
                itemCount: game.pieces.length,
                gridDelegate:
                    SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount:
                      game.pieceCount <= 4 ? 2 : 3,
                  crossAxisSpacing: 15,
                  mainAxisSpacing: 15,
                ),
                itemBuilder: (context, index) {
                  return _buildPiece(index);
                },
              ),
            ),

            Padding(
              padding: const EdgeInsets.only(
                left: 25,
                right: 25,
                bottom: 25,
              ),
              child: SizedBox(
                width: double.infinity,
                height: 60,
                child: ElevatedButton.icon(
                  onPressed: game.isComplete
                      ? null
                      : _checkPuzzle,
                  icon: const Icon(
                    Icons.check_circle_outline,
                    size: 28,
                  ),
                  label: const Text(
                    'Check Puzzle',
                    style: TextStyle(
                      fontSize: 21,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPiece(int index) {
    final piece = game.pieces[index];

    return GestureDetector(
      onTap: () => _movePiece(index),
      child: AnimatedContainer(
        duration:
            const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          borderRadius:
              BorderRadius.circular(20),
          color: Colors.blue.shade100,
          border: Border.all(
            color: Colors.blue.shade700,
            width: 3,
          ),
          boxShadow: const [
            BoxShadow(
              blurRadius: 5,
              offset: Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.extension,
              size: 40,
            ),
            const SizedBox(height: 8),
            Text(
              piece,
              style: const TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}