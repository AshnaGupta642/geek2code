import 'package:flutter/material.dart';

import 'games/game_selector_screen.dart';

void main() {
  runApp(const GameEngineApp());
}

class GameEngineApp extends StatelessWidget {
  const GameEngineApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Cognitive Games',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
      home: const GameSelectorScreen(),
    );
  }
}
