"""
player.py - Player Spaceship Cannon for Space Invaders.
Subclasses turtle.Turtle with custom turret geometry, boundary clamping, and firing cooldowns.
"""

from turtle import Turtle, Shape
import time

CANNON_SHAPE_POINTS = (
    (-18, -6),
    (-18, 2),
    (-14, 2),
    (-14, 8),
    (-3, 8),
    (-3, 16),
    (3, 16),
    (3, 8),
    (14, 8),
    (14, 2),
    (18, 2),
    (18, -6),
)

PLAYER_START_Y = -270
MOVE_SPEED = 18
X_BOUND_MIN = -360
X_BOUND_MAX = 360
FIRE_COOLDOWN = 0.35  # Minimum seconds between shots


class Player(Turtle):
    def __init__(self, shape_name="laser_cannon"):
        super().__init__()
        self.shape_name = shape_name
        self._register_custom_shape()
        self.shape(self.shape_name)
        self.color("#00FF66")  # Vibrant arcade green
        self.penup()
        self.speed(0)
        self.goto(0, PLAYER_START_Y)
        self.setheading(90)
        
        self.last_shot_time = 0.0
        self.is_moving_left = False
        self.is_moving_right = False

    def _register_custom_shape(self):
        """Registers the custom vector polygon for the laser cannon."""
        try:
            custom_shape = Shape("compound")
            custom_shape.addcomponent(CANNON_SHAPE_POINTS, "#00FF66", "#00CC55")
            self.screen.register_shape(self.shape_name, custom_shape)
        except Exception:
            # Fallback to built-in square if compound shape registration fails
            self.shape_name = "square"

    def move_left(self):
        """Move cannon to the left within boundaries."""
        new_x = self.xcor() - MOVE_SPEED
        if new_x >= X_BOUND_MIN:
            self.setx(new_x)
        else:
            self.setx(X_BOUND_MIN)

    def move_right(self):
        """Move cannon to the right within boundaries."""
        new_x = self.xcor() + MOVE_SPEED
        if new_x <= X_BOUND_MAX:
            self.setx(new_x)
        else:
            self.setx(X_BOUND_MAX)

    def update_continuous_movement(self):
        """Updates position based on currently held keys for buttery-smooth 60 FPS controls."""
        if self.is_moving_left and not self.is_moving_right:
            self.move_left()
        elif self.is_moving_right and not self.is_moving_left:
            self.move_right()

    def can_fire(self) -> bool:
        """Checks if firing cooldown has elapsed."""
        current_time = time.time()
        if current_time - self.last_shot_time >= FIRE_COOLDOWN:
            self.last_shot_time = current_time
            return True
        return False

    def reset_position(self):
        """Resets cannon to center baseline after hit."""
        self.goto(0, PLAYER_START_Y)
        self.is_moving_left = False
        self.is_moving_right = False
