class AdaptiveDifficulty {
  int calculateNextDifficulty({
    required int currentDifficulty,
    required double accuracy,
    required double averageResponseTime,
  }) {
    int nextDifficulty = currentDifficulty;

    // Excellent performance → increase difficulty
    if (accuracy >= 0.85 && averageResponseTime <= 5) {
      nextDifficulty++;
    }

    // Poor performance → decrease difficulty
    else if (accuracy < 0.50 || averageResponseTime > 10) {
      nextDifficulty--;
    }

    // Keep difficulty between 1 and 3
    if (nextDifficulty < 1) {
      nextDifficulty = 1;
    }

    if (nextDifficulty > 3) {
      nextDifficulty = 3;
    }

    return nextDifficulty;
  }

  String getDifficultyLabel(int difficulty) {
    switch (difficulty) {
      case 1:
        return 'Easy';
      case 2:
        return 'Medium';
      case 3:
        return 'Hard';
      default:
        return 'Unknown';
    }
  }
}