import 'dart:async';

import 'package:flutter/material.dart';

import '../../engine/game_adapter.dart';
import '../../engine/game_engine.dart';
import '../../engine/result_manager.dart';
import '../../models/game_result.dart';
import '../../services/adaptive_difficulty.dart';
import '../../services/game_api_service.dart';
import '../../services/performance_tracker.dart';
import '../../services/sound_service.dart';
import 'sound_memory_game.dart';

class SoundMemoryScreen extends StatefulWidget {
  final int difficulty;

  const SoundMemoryScreen({super.key, this.difficulty = 1});

  @override
  State<SoundMemoryScreen> createState() => _SoundMemoryScreenState();
}

class _SoundMemoryScreenState extends State<SoundMemoryScreen> {
  late SoundMemoryGame game;

  final GameEngine gameEngine = GameEngine();
  final ResultManager resultManager = ResultManager();
  final GameApiService gameApiService = GameApiService();
  late GameAdapter gameAdapter;

  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty = AdaptiveDifficulty();

  final SoundService soundService = SoundService();

  int currentDifficulty = 1;
  int nextDifficulty = 1;

  bool gameStarted = false;
  bool playingSequence = false;
  int? currentlyPlaying;

  @override
  void initState() {
    super.initState();

    currentDifficulty = widget.difficulty;

    game = SoundMemoryGame(difficulty: currentDifficulty);

    gameEngine.startGame(game);

    gameAdapter = GameAdapter(
      gameId: game.gameId,
      difficulty: currentDifficulty,
    );

    tracker.startGame();
  }

  // ------------------------------------------------------------
  // START GAME
  // ------------------------------------------------------------

  Future<void> _startGame() async {
    if (gameStarted || playingSequence) {
      return;
    }

    setState(() {
      gameStarted = true;
      playingSequence = true;
    });

    await _playSequence();

    if (!mounted) return;

    setState(() {
      playingSequence = false;
    });

    tracker.startResponseTimer();
  }

  // ------------------------------------------------------------
  // PLAY SOUND SEQUENCE
  // ------------------------------------------------------------

  Future<void> _playSequence() async {
    for (final soundId in game.sequence) {
      if (!mounted) return;

      setState(() {
        currentlyPlaying = soundId;
      });

      await soundService.playSound(soundId);

      await Future.delayed(const Duration(milliseconds: 800));

      if (!mounted) return;

      setState(() {
        currentlyPlaying = null;
      });

      await Future.delayed(const Duration(milliseconds: 300));
    }
  }

  // ------------------------------------------------------------
  // SOUND SELECTION
  // ------------------------------------------------------------

  void _selectSound(int soundId) {
    if (!gameStarted || playingSequence || game.isComplete) {
      return;
    }

    soundService.playSound(soundId);

    game.addAnswer(soundId);

    setState(() {});

    if (game.isComplete) {
      tracker.recordAttempt(correct: game.isCorrect);

      _showGameCompletedDialog();
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
        debugPrint('Sound Memory result submitted successfully.');
      } else {
        debugPrint('Failed to submit Sound Memory result.');
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
            'Sound sequence completed!\n\n'
            'Result: '
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

                  game = SoundMemoryGame(difficulty: currentDifficulty);

                  gameEngine.startGame(game);

                  gameAdapter = GameAdapter(
                    gameId: game.gameId,
                    difficulty: currentDifficulty,
                  );

                  tracker.startGame();

                  gameStarted = false;
                  playingSequence = false;
                  currentlyPlaying = null;
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
    soundService.dispose();
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
          'Sound Memory',
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

                    _buildStartArea(),

                    const SizedBox(height: 22),

                    _buildSoundBoard(width),

                    if (gameStarted && !playingSequence) ...[
                      const SizedBox(height: 20),
                      _buildProgress(),
                    ],
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

        Text(
          playingSequence
              ? 'Listen carefully! 🔊'
              : gameStarted
              ? 'Repeat the sounds'
              : 'Remember the sound sequence',
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 27,
            fontWeight: FontWeight.bold,
            color: Color(0xFF202B28),
          ),
        ),

        const SizedBox(height: 8),

        Text(
          playingSequence
              ? 'Listen to each sound carefully'
              : gameStarted
              ? 'Tap the sounds in the same order'
              : 'Press start when you are ready',
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 17, color: Color(0xFF5F625F)),
        ),
      ],
    );
  }

  Widget _buildStartArea() {
    if (playingSequence) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 22),
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
            const SizedBox(
              width: 38,
              height: 38,
              child: CircularProgressIndicator(strokeWidth: 4),
            ),
            const SizedBox(height: 14),
            Text(
              currentlyPlaying == null ? 'Get ready...' : 'Playing sound...',
              style: const TextStyle(
                fontSize: 19,
                fontWeight: FontWeight.w600,
                color: Color(0xFF202B28),
              ),
            ),
          ],
        ),
      );
    }

    if (!gameStarted) {
      return SizedBox(
        width: double.infinity,
        height: 64,
        child: ElevatedButton.icon(
          onPressed: _startGame,
          icon: const Icon(Icons.play_arrow, size: 30),
          label: const Text(
            'Start Game',
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

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
      ),
      child: const Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.hearing, size: 25, color: Color(0xFF205A46)),
          SizedBox(width: 10),
          Text(
            'Your turn',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Color(0xFF202B28),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSoundBoard(double screenWidth) {
    const icons = [
      Icons.music_note,
      Icons.notifications,
      Icons.directions_car,
      Icons.pets,
      Icons.nature,
    ];

    const labels = ['Music', 'Bell', 'Car', 'Dog', 'Nature'];

    const double spacing = 12;

    final double buttonWidth = (screenWidth - 40 - spacing) / 2;

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
        children: List.generate(5, (index) {
          return SizedBox(
            width: buttonWidth.clamp(130.0, 210.0),
            height: 108,
            child: _buildSoundButton(index, icons[index], labels[index]),
          );
        }),
      ),
    );
  }

  Widget _buildSoundButton(int soundId, IconData icon, String label) {
    final bool isPlaying = currentlyPlaying == soundId;

    return GestureDetector(
      onTap: () => _selectSound(soundId),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(20),
          color: isPlaying ? const Color(0xFFCDE8D5) : const Color(0xFFF9D58A),
          border: Border.all(
            color: isPlaying
                ? const Color(0xFF4F8A68)
                : const Color(0xFFE4B85F),
            width: 2.5,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.07),
              blurRadius: 5,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 42, color: const Color(0xFF205A46)),
            const SizedBox(height: 8),
            Text(
              label,
              style: const TextStyle(
                fontSize: 19,
                fontWeight: FontWeight.bold,
                color: Color(0xFF202B28),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProgress() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        color: const Color(0xFFE6F0E8),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        'Selected: '
        '${game.userSequence.length}/'
        '${game.sequence.length}',
        style: const TextStyle(
          fontSize: 19,
          fontWeight: FontWeight.bold,
          color: Color(0xFF205A46),
        ),
      ),
    );
  }
}
