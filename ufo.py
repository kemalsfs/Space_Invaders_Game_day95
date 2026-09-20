"""
ufo.py - Mystery Flying Saucer (Bonus Target) for Space Invaders.
Crosses the upper screen at irregular intervals and awards random mystery points.
"""

from turtle import Turtle, Shape
import random
import time
from sound_effects import play_ufo_sound

UFO_SHAPE_POINTS = (
    (-18, 0), (-12, 6), (-4, 6), (-2, 10), (2, 10), (4, 6),
    (12, 6), (18, 0), (10, -5), (-10, -5)
)

UFO_Y = 280
UFO_SPEED = 4.5
POSSIBLE_POINTS = [50, 100, 150, 300]


class MysteryUFO(Turtle):
    def __init__(self):
        super().__init__()
        self._register_ufo_shape()
        self.shape("ufo_saucer")
        self.color("#FF1744")  # Vivid crimson red
        self.penup()
        self.speed(0)
        self.hideturtle()
        
        self.is_active = False
        self.direction = 1  # 1: left-to-right, -1: right-to-left
        self.next_spawn_time = time.time() + random.uniform(18.0, 32.0)
        self.last_audio_time = 0.0

    def _register_ufo_shape(self):
        try:
            custom_shape = Shape("compound")
            custom_shape.addcomponent(UFO_SHAPE_POINTS, "#FF1744", "#FFFFFF")
            self.screen.register_shape("ufo_saucer", custom_shape)
        except Exception:
            self.shape("circle")
            self.shapesize(stretch_wid=0.8, stretch_len=1.8)

    def update(self) -> int | None:
        """
        Updates UFO state. Spawns if timer has elapsed and traverses across screen.
        """
        now = time.time()
        
        if not self.is_active:
            if now >= self.next_spawn_time:
                self._spawn()
            return None

        # Movement when active
        self.setx(self.xcor() + (self.direction * UFO_SPEED))
        
        # Intermittent audio pulse
        if now - self.last_audio_time > 0.4:
            self.last_audio_time = now
            play_ufo_sound()

        # Check exit screen
        if (self.direction == 1 and self.xcor() > 410) or (self.direction == -1 and self.xcor() < -410):
            self.despawn()

        return None

    def _spawn(self):
        """Initializes a new flyby across the top of the canvas."""
        self.is_active = True
        self.direction = random.choice([1, -1])
        start_x = -400 if self.direction == 1 else 400
        self.goto(start_x, UFO_Y)
        self.showturtle()

    def hit(self) -> int:
        """Called when struck by player laser. Returns awarded bonus points."""
        points = random.choice(POSSIBLE_POINTS)
        self.despawn()
        return points

    def despawn(self):
        """Despawns saucer and resets timer for next appearance."""
        self.is_active = False
        self.hideturtle()
        self.goto(4000, 4000)
        self.next_spawn_time = time.time() + random.uniform(22.0, 40.0)

    def reset(self):
        """Resets UFO state completely."""
        self.despawn()
        self.next_spawn_time = time.time() + random.uniform(18.0, 30.0)
