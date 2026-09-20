import 'package:flutter/material.dart';

import '../../engine/game_adapter.dart';
import '../../engine/game_engine.dart';
import '../../engine/result_manager.dart';
import '../../models/game_result.dart';
import '../../services/adaptive_difficulty.dart';
import '../../services/game_api_service.dart';
import '../../services/performance_tracker.dart';
import 'puzzle_game.dart';

class PuzzleScreen extends StatefulWidget {
  final int difficulty;

  const PuzzleScreen({super.key, this.difficulty = 1});

  @override
  State<PuzzleScreen> createState() => _PuzzleScreenState();
}

class _PuzzleScreenState extends State<PuzzleScreen> {
  late PuzzleGame game;

  final GameEngine gameEngine = GameEngine();
  final ResultManager resultManager = ResultManager();

  late GameAdapter gameAdapter;

  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty = AdaptiveDifficulty();
  final GameApiService gameApiService = GameApiService();

  int currentDifficulty = 1;
  int nextDifficulty = 1;

  @override
  void initState() {
    super.initState();

    currentDifficulty = widget.difficulty;

    game = PuzzleGame(difficulty: currentDifficulty);

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

    tracker.recordAttempt(correct: game.isCorrect);

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
      sessionId: DateTime.now().millisecondsSinceEpoch.toString(),
      completionRate: game.isCorrect ? 1.0 : 0.0,
    );
    gameApiService.submitResult(result).then((success) {
      if (success) {
        debugPrint('Puzzle result submitted successfully.');
      } else {
        debugPrint('Failed to submit Puzzle result.');
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
            style: const TextStyle(fontSize: 21),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);

                setState(() {
                  currentDifficulty = nextDifficulty;

                  game = PuzzleGame(difficulty: currentDifficulty);

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
          'Puzzle',
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

                    const SizedBox(height: 22),

                    _buildPuzzleBoard(width),

                    const SizedBox(height: 24),

                    _buildCheckButton(),
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
          'Arrange the pieces in order',
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 27,
            fontWeight: FontWeight.bold,
            color: Color(0xFF202B28),
          ),
        ),

        const SizedBox(height: 8),

        Text(
          '${game.pieceCount} pieces',
          style: const TextStyle(fontSize: 18, color: Color(0xFF5F625F)),
        ),

        const SizedBox(height: 6),

        const Text(
          'Tap a piece to move it',
          style: TextStyle(fontSize: 16, color: Color(0xFF777777)),
        ),
      ],
    );
  }

  Widget _buildPuzzleBoard(double screenWidth) {
    final int columns = game.pieceCount <= 4 ? 2 : 3;

    const double spacing = 14;

    final double availableWidth = screenWidth - 40 - ((columns - 1) * spacing);

    final double pieceSize = (availableWidth / columns).clamp(90.0, 145.0);

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
        children: List.generate(game.pieces.length, (index) {
          return SizedBox(
            width: pieceSize,
            height: pieceSize,
            child: _buildPiece(index),
          );
        }),
      ),
    );
  }

  Widget _buildCheckButton() {
    return SizedBox(
      width: double.infinity,
      height: 62,
      child: ElevatedButton.icon(
        onPressed: game.isComplete ? null : _checkPuzzle,
        icon: const Icon(Icons.check_circle_outline, size: 27),
        label: const Text(
          'Check Puzzle',
          style: TextStyle(fontSize: 21, fontWeight: FontWeight.bold),
        ),
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF205A46),
          foregroundColor: Colors.white,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
          ),
        ),
      ),
    );
  }

  Widget _buildPiece(int index) {
    final piece = game.pieces[index];

    return GestureDetector(
      onTap: () => _movePiece(index),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: const Color(0xFFF9D58A),
          border: Border.all(color: const Color(0xFFE4B85F), width: 2.5),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.08),
              blurRadius: 5,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.extension, size: 38, color: Color(0xFF205A46)),
            const SizedBox(height: 8),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: Text(
                piece,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF202B28),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
