class DifficultyEngine {
  /// Calculates the new difficulty based on the patient's performance in the last game.
  ///
  /// The performance metric is calculated as:
  /// (Accuracy * 0.5 + (1 - Normalized Response Time) * 0.3) / (Hints Used + Mistakes + 1)
  ///
  /// The formula dynamically increases or decreases the difficulty level.
  static String calculateNextDifficulty({
    required double accuracy, // 0.0 to 1.0
    required double responseTimeSeconds,
    required int hintsUsed,
    required int mistakes,
    required String currentDifficulty, // 'easy', 'medium', 'hard'
  }) {
    // Normalize response time (assume 30s is a baseline max for a turn)
    double normalizedTime = (responseTimeSeconds / 30.0).clamp(0.0, 1.0);

    double performanceMetric =
        ((accuracy * 0.5) + ((1.0 - normalizedTime) * 0.3)) /
        (hintsUsed + mistakes + 1);

    if (performanceMetric >= 0.4) {
      // Patient performed very well, increase difficulty if possible
      if (currentDifficulty == 'easy') return 'medium';
      if (currentDifficulty == 'medium') return 'hard';
      return 'hard'; // Max difficulty
    } else if (performanceMetric < 0.15) {
      // Patient struggled, decrease difficulty
      if (currentDifficulty == 'hard') return 'medium';
      if (currentDifficulty == 'medium') return 'easy';
      return 'easy'; // Min difficulty
    }

    // Keep current difficulty if performance is average
    return currentDifficulty;
  }
}
