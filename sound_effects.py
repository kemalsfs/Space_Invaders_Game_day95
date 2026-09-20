"""
sound_effects.py - Asynchronous non-blocking audio synthesizer for Space Invaders.
Uses Windows winsound in background daemon threads with safe cross-platform fallback.
"""

import threading
import sys

_SOUND_ENABLED = True

def _play_beep(frequency: int, duration_ms: int):
    """Internal helper to beep without blocking the main game loop."""
    if not _SOUND_ENABLED:
        return
    try:
        if sys.platform == "win32":
            import winsound
            winsound.Beep(frequency, duration_ms)
    except Exception:
        pass


def play_laser_sound():
    """High-pitched beam sound when player fires."""
    t = threading.Thread(target=_play_beep, args=(880, 35), daemon=True)
    t.start()


def play_alien_hit_sound():
    """Crisp impact sound when an alien is destroyed."""
    t = threading.Thread(target=_play_beep, args=(320, 60), daemon=True)
    t.start()


def play_player_hit_sound():
    """Low rumble sound when player loses a life."""
    def _rumble():
        for freq in (220, 160, 110):
            _play_beep(freq, 70)
    t = threading.Thread(target=_rumble, daemon=True)
    t.start()


def play_ufo_sound():
    """Mystery UFO sound alert."""
    t = threading.Thread(target=_play_beep, args=(1200, 50), daemon=True)
    t.start()


def play_bunker_hit_sound():
    """Dull thud when a bunker segment absorbs fire."""
    t = threading.Thread(target=_play_beep, args=(180, 30), daemon=True)
    t.start()


def play_march_sound(note_index: int):
    """
    Classic 4-tone descending march sound (0 to 3).
    Recreates the iconic heartbeat cadence of Space Invaders.
    """
    frequencies = [140, 125, 110, 98]
    freq = frequencies[note_index % len(frequencies)]
    t = threading.Thread(target=_play_beep, args=(freq, 30), daemon=True)
    t.start()
