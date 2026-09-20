import 'package:flutter/material.dart';

import 'memory_match/memory_match_screen.dart';
import 'sequence_memory/sequence_memory_screen.dart';
import 'pattern_recognition/pattern_recognition_screen.dart';
import 'puzzle/puzzle_screen.dart';
import 'sound_memory/sound_memory_screen.dart';

class GameSelectorScreen extends StatelessWidget {
  const GameSelectorScreen({super.key});

  void _openGame(BuildContext context, Widget game) {
    Navigator.push(context, MaterialPageRoute(builder: (_) => game));
  }

  @override
  Widget build(BuildContext context) {
    final games = [
      {
        'title': 'Memory Match',
        'subtitle': 'Match the pairs',
        'icon': Icons.grid_view_rounded,
        'screen': const MemoryMatchScreen(),
      },
      {
        'title': 'Sequence Memory',
        'subtitle': 'Remember the order',
        'icon': Icons.format_list_numbered,
        'screen': const SequenceMemoryScreen(),
      },
      {
        'title': 'Pattern Recognition',
        'subtitle': 'Find the correct pattern',
        'icon': Icons.pattern,
        'screen': const PatternRecognitionScreen(),
      },
      {
        'title': 'Puzzle',
        'subtitle': 'Arrange the pieces',
        'icon': Icons.extension,
        'screen': const PuzzleScreen(),
      },
      {
        'title': 'Sound Memory',
        'subtitle': 'Remember the sounds',
        'icon': Icons.volume_up,
        'screen': const SoundMemoryScreen(),
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Cognitive Games',
          style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const SizedBox(height: 10),

            const Text(
              'Choose a game to play',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.w600),
            ),

            const SizedBox(height: 25),

            ...games.map(
              (game) => Padding(
                padding: const EdgeInsets.only(bottom: 18),
                child: SizedBox(
                  height: 105,
                  child: ElevatedButton(
                    onPressed: () =>
                        _openGame(context, game['screen'] as Widget),
                    style: ElevatedButton.styleFrom(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(20),
                      ),
                    ),
                    child: Row(
                      children: [
                        Icon(game['icon'] as IconData, size: 48),
                        const SizedBox(width: 22),
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                game['title'] as String,
                                style: const TextStyle(
                                  fontSize: 23,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 5),
                              Text(
                                game['subtitle'] as String,
                                style: const TextStyle(fontSize: 17),
                              ),
                            ],
                          ),
                        ),
                        const Icon(Icons.arrow_forward_ios, size: 25),
                      ],
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
}
