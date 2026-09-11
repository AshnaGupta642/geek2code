class MemoryCard {
  final String id;
  final String image;
  bool isFlipped;
  bool isMatched;

  MemoryCard({
    required this.id,
    required this.image,
    this.isFlipped = false,
    this.isMatched = false,
  });
}
