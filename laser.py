"""
laser.py - Laser projectiles and alien bomb classes for Space Invaders.
Handles projectile physics, bounding box collision checks, and boundary recycling.
"""

from turtle import Turtle

PLAYER_LASER_SPEED = 22
ALIEN_BOMB_SPEED = 11
TOP_BOUND = 325
BOTTOM_BOUND = -325


class PlayerLaser(Turtle):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.8, stretch_len=0.18)
        self.color("#00FF66")  # Neon laser green
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.is_active = True

    def move(self):
        """Advance laser upward."""
        if not self.is_active:
            return
        self.sety(self.ycor() + PLAYER_LASER_SPEED)
        if self.ycor() > TOP_BOUND:
            self.destroy()

    def destroy(self):
        """Deactivates and removes laser from display."""
        self.is_active = False
        self.hideturtle()
        self.goto(1000, 1000)  # Move far off-screen


class AlienBomb(Turtle):
    def __init__(self, x: float, y: float, speed: float = ALIEN_BOMB_SPEED):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.7, stretch_len=0.18)
        self.color("#FF3366")  # Hot alien pink/red
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.speed_val = speed
        self.is_active = True

    def move(self):
        """Advance bomb downward towards player defense."""
        if not self.is_active:
            return
        self.sety(self.ycor() - self.speed_val)
        if self.ycor() < BOTTOM_BOUND:
            self.destroy()

    def destroy(self):
        """Deactivates and removes bomb from display."""
        self.is_active = False
        self.hideturtle()
        self.goto(1000, 1000)
