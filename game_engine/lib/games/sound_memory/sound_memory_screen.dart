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

  const SoundMemoryScreen({
    super.key,
    this.difficulty = 1,
  });

  @override
  State<SoundMemoryScreen> createState() =>
      _SoundMemoryScreenState();
}

class _SoundMemoryScreenState
    extends State<SoundMemoryScreen> {
  late SoundMemoryGame game;

  final GameEngine gameEngine = GameEngine();
  final ResultManager resultManager = ResultManager();
  final GameApiService gameApiService = GameApiService();
  late GameAdapter gameAdapter;

  final PerformanceTracker tracker = PerformanceTracker();
  final AdaptiveDifficulty adaptiveDifficulty =
      AdaptiveDifficulty();

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

    game = SoundMemoryGame(
      difficulty: currentDifficulty,
    );

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

      await Future.delayed(
        const Duration(milliseconds: 800),
      );

      if (!mounted) return;

      setState(() {
        currentlyPlaying = null;
      });

      await Future.delayed(
        const Duration(milliseconds: 300),
      );
    }
  }

  // ------------------------------------------------------------
  // SOUND SELECTION
  // ------------------------------------------------------------

  void _selectSound(int soundId) {
    if (!gameStarted ||
        playingSequence ||
        game.isComplete) {
      return;
    }

    soundService.playSound(soundId);

    game.addAnswer(soundId);

    setState(() {});

    if (game.isComplete) {
      tracker.recordAttempt(
        correct: game.isCorrect,
      );

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
      sessionId:
          DateTime.now().millisecondsSinceEpoch.toString(),
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
            'Sound sequence completed!\n\n'
            'Result: '
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
                  currentDifficulty =
                      nextDifficulty;

                  game = SoundMemoryGame(
                    difficulty: currentDifficulty,
                  );

                  gameEngine.startGame(game);

                  gameAdapter = GameAdapter(
                    gameId: game.gameId,
                    difficulty:
                        currentDifficulty,
                  );

                  tracker.startGame();

                  gameStarted = false;
                  playingSequence = false;
                  currentlyPlaying = null;
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
      appBar: AppBar(
        title: const Text(
          'Sound Memory',
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

            Text(
              playingSequence
                  ? 'Listen carefully! 🔊'
                  : gameStarted
                      ? 'Repeat the sounds'
                      : 'Remember the sound sequence',
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.w600,
              ),
            ),

            const SizedBox(height: 25),

            if (!gameStarted)
              ElevatedButton.icon(
                onPressed: _startGame,
                icon: const Icon(
                  Icons.play_arrow,
                  size: 28,
                ),
                label: const Padding(
                  padding: EdgeInsets.symmetric(
                    horizontal: 18,
                    vertical: 12,
                  ),
                  child: Text(
                    'Start Game',
                    style: TextStyle(
                      fontSize: 20,
                    ),
                  ),
                ),
              ),

            if (playingSequence)
              const Padding(
                padding: EdgeInsets.all(20),
                child: CircularProgressIndicator(),
              ),

            const SizedBox(height: 20),

            Expanded(
              child: GridView.builder(
                padding: const EdgeInsets.all(20),
                itemCount: 5,
                gridDelegate:
                    const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                ),
                itemBuilder: (context, index) {
                  return _buildSoundButton(index);
                },
              ),
            ),

            if (gameStarted && !playingSequence)
              Padding(
                padding: const EdgeInsets.only(
                  bottom: 20,
                ),
                child: Text(
                  'Selected: '
                  '${game.userSequence.length}/'
                  '${game.sequence.length}',
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildSoundButton(int soundId) {
    const icons = [
      Icons.music_note,
      Icons.notifications,
      Icons.directions_car,
      Icons.pets,
      Icons.nature,
    ];

    const labels = [
      'Music',
      'Bell',
      'Car',
      'Dog',
      'Nature',
    ];

    final bool isPlaying =
        currentlyPlaying == soundId;

    return GestureDetector(
      onTap: () => _selectSound(soundId),
      child: AnimatedContainer(
        duration:
            const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          borderRadius:
              BorderRadius.circular(20),
          color: isPlaying
              ? Colors.green.shade300
              : Colors.blue.shade100,
          border: Border.all(
            color: Colors.blue.shade700,
            width: 3,
          ),
        ),
        child: Column(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            Icon(
              icons[soundId],
              size: 50,
            ),
            const SizedBox(height: 10),
            Text(
              labels[soundId],
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}