import 'package:audioplayers/audioplayers.dart';

class SoundService {
  final AudioPlayer _player = AudioPlayer();

  Future<void> playSound(int soundId) async {
    const sounds = [
      'sounds/music.wav',
      'sounds/bell.wav',
      'sounds/car.wav',
      'sounds/dog.wav',
      'sounds/nature.wav',
    ];

    if (soundId < 0 || soundId >= sounds.length) return;

    await _player.stop();
    await _player.play(
      AssetSource(sounds[soundId]),
    );
  }

  Future<void> dispose() async {
    await _player.dispose();
  }
}