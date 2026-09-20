"""
alien.py - Alien hierarchy and AlienFleet coordinator for Space Invaders.
Handles formation marching, progressive hardware-style speedup, boundary bounce/drop,
and column-based tactical bomb dropping.
"""

from turtle import Turtle, Shape
import random
import time
from laser import AlienBomb
from sound_effects import play_march_sound

# Vector contours for iconic 1978 arcade sprites
SQUID_SHAPE_POINTS = (
    (-6, 12), (6, 12), (10, 6), (6, -4), (10, -10),
    (6, -10), (2, -4), (-2, -4), (-6, -10), (-10, -10),
    (-6, -4), (-10, 6)
)

CRAB_SHAPE_POINTS = (
    (-12, 10), (-6, 10), (-4, 4), (4, 4), (6, 10), (12, 10),
    (10, 0), (14, -6), (10, -10), (6, -4), (-6, -4),
    (-10, -10), (-14, -6), (-10, 0)
)

OCTOPUS_SHAPE_POINTS = (
    (-8, 10), (8, 10), (12, 4), (12, -4), (8, -10),
    (4, -4), (0, -10), (-4, -4), (-8, -10), (-12, -4), (-12, 4)
)

ALIEN_RANKS = {
    3: {"name": "squid", "points": 30, "color": "#D800FF", "points_shape": SQUID_SHAPE_POINTS},
    2: {"name": "crab", "points": 20, "color": "#00FFFF", "points_shape": CRAB_SHAPE_POINTS},
    1: {"name": "octopus", "points": 10, "color": "#FFFF00", "points_shape": OCTOPUS_SHAPE_POINTS},
}

FLEET_ROWS = 4
FLEET_COLS = 6
X_SPACING = 55
Y_SPACING = 45
LEFT_BOUND = -350
RIGHT_BOUND = 350
FLEET_DROP_Y = 22
PLAYER_DEFENSE_LINE_Y = -245


def register_alien_shapes(screen):
    """Registers compound shapes for the three alien castes onto the turtle Screen."""
    for rank, data in ALIEN_RANKS.items():
        try:
            custom_shape = Shape("compound")
            custom_shape.addcomponent(data["points_shape"], data["color"], data["color"])
            screen.register_shape(data["name"], custom_shape)
        except Exception:
            pass


class Alien(Turtle):
    def __init__(self, rank: int, x: float, y: float):
        super().__init__()
        self.rank = rank
        self.config = ALIEN_RANKS[rank]
        self.points = self.config["points"]
        
        try:
            self.shape(self.config["name"])
        except Exception:
            self.shape("circle")
            
        self.color(self.config["color"])
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.is_alive = True

    def destroy(self):
        """Hides and retires alien from active play."""
        self.is_alive = False
        self.hideturtle()
        self.goto(2000, 2000)


class AlienFleet:
    def __init__(self, screen, wave: int = 1):
        self.screen = screen
        self.wave = wave
        self.aliens: list[Alien] = []
        self.dx = 14  # Horizontal step size
        self.march_counter = 0
        self.last_march_time = time.time()
        self.last_bomb_time = time.time()
        
        # Difficulty scaling
        self.base_step_interval = max(0.28, 0.65 - (wave - 1) * 0.06)
        self.bomb_interval = max(1.1, 2.2 - (wave - 1) * 0.15)
        
        self._spawn_fleet()

    def _spawn_fleet(self):
        """Constructs the 4x6 alien invader matrix."""
        start_x = -((FLEET_COLS - 1) * X_SPACING) / 2
        start_y = 120 + min(40, (self.wave - 1) * 10)  # Starts slightly lower on higher waves

        # Row 3 (top): Squid (Rank 3)
        # Row 2: Crab (Rank 2)
        # Row 1: Crab (Rank 2)
        # Row 0 (bottom): Octopus (Rank 1)
        row_ranks = [1, 2, 2, 3]

        for row_idx, rank in enumerate(row_ranks):
            for col_idx in range(FLEET_COLS):
                x = start_x + (col_idx * X_SPACING)
                y = start_y + (row_idx * Y_SPACING)
                alien = Alien(rank=rank, x=x, y=y)
                self.aliens.append(alien)

    @property
    def alive_aliens(self) -> list[Alien]:
        return [a for a in self.aliens if a.is_alive]

    @property
    def total_initial(self) -> int:
        return FLEET_ROWS * FLEET_COLS

    def get_current_step_interval(self) -> float:
        """Dynamically accelerates march as fleet numbers dwindle."""
        alive_count = len(self.alive_aliens)
        if alive_count == 0:
            return self.base_step_interval
        # Scale between base_step_interval and 0.08s for the last remaining alien
        ratio = alive_count / self.total_initial
        return max(0.08, self.base_step_interval * (ratio ** 0.85))

    def update(self) -> list[AlienBomb]:
        """
        Advances fleet position and periodically drops bombs.
        Returns a list of newly spawned AlienBomb instances.
        """
        new_bombs = []
        now = time.time()
        
        # 1. Fleet March Timing
        if now - self.last_march_time >= self.get_current_step_interval():
            self.last_march_time = now
            self._march_step()

        # 2. Bomb Dropping Timing
        if now - self.last_bomb_time >= self.bomb_interval:
            self.last_bomb_time = now
            bomb = self._drop_bomb()
            if bomb:
                new_bombs.append(bomb)

        return new_bombs

    def _march_step(self):
        """Executes one step in the synchronized fleet march."""
        alive = self.alive_aliens
        if not alive:
            return

        # Check if boundary would be crossed on the next step
        drop_and_reverse = False
        for alien in alive:
            next_x = alien.xcor() + self.dx
            if next_x > RIGHT_BOUND or next_x < LEFT_BOUND:
                drop_and_reverse = True
                break

        if drop_and_reverse:
            self.dx = -self.dx
            for alien in alive:
                alien.sety(alien.ycor() - FLEET_DROP_Y)
        else:
            for alien in alive:
                alien.setx(alien.xcor() + self.dx)

        # Heartbeat cadence audio
        play_march_sound(self.march_counter)
        self.march_counter += 1

    def _drop_bomb(self) -> AlienBomb | None:
        """Picks a random bottom-most alien from active columns to fire downward."""
        alive = self.alive_aliens
        if not alive:
            return None

        # Group aliens by rounded x coordinate to identify lowest member of each column
        columns: dict[float, Alien] = {}
        for alien in alive:
            # Round x to collapse small variations
            col_key = round(alien.xcor() / 10.0) * 10.0
            if col_key not in columns or alien.ycor() < columns[col_key].ycor():
                columns[col_key] = alien

        bottom_aliens = list(columns.values())
        if not bottom_aliens:
            return None

        shooter = random.choice(bottom_aliens)
        bomb_speed = 10 + min(6, self.wave * 1.2)
        return AlienBomb(x=shooter.xcor(), y=shooter.ycor() - 14, speed=bomb_speed)

    def has_breached(self) -> bool:
        """Returns True if any alien has penetrated to or below player baseline."""
        for alien in self.alive_aliens:
            if alien.ycor() <= PLAYER_DEFENSE_LINE_Y:
                return True
        return False

    def is_cleared(self) -> bool:
        """Returns True if all aliens in the fleet have been defeated."""
        return len(self.alive_aliens) == 0

    def clear(self):
        """Cleanly removes all remaining aliens when restarting or resetting."""
        for alien in self.aliens:
            alien.destroy()
        self.aliens.clear()
