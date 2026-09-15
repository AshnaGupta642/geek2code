abstract class CognitiveGame {
  String get gameId;

  int get difficulty;

  bool get isComplete;

  int get score;

  int get attempts;

  int get mistakes;

  void reset();
}