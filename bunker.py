"""
bunker.py - Defensive Bunkers and shield segment matrices for Space Invaders.
Constructs 4 classic arch-shaped defensive structures that erode upon absorbing laser or bomb hits.
"""

from turtle import Turtle

BLOCK_SIZE = 12
BUNKER_COLOR = "#00FF7F"  # Classic arcade defense green
BUNKER_Y = -185
BUNKER_X_OFFSETS = [-240, -80, 80, 240]

# 5 columns x 4 rows matrix with center arch opening at the bottom
# 1 = block present, 0 = arch hollow
BUNKER_LAYOUT = [
    [1, 1, 0, 1, 1],  # Row 0 (bottom)
    [1, 1, 0, 1, 1],  # Row 1
    [1, 1, 1, 1, 1],  # Row 2
    [0, 1, 1, 1, 0],  # Row 3 (rounded top)
]


class BunkerBlock(Turtle):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.shape("square")
        # Base turtle square is 20x20. Scale to BLOCK_SIZE (e.g. 12x12 -> 0.6 stretch)
        self.shapesize(stretch_wid=BLOCK_SIZE / 20.0, stretch_len=BLOCK_SIZE / 20.0)
        self.color(BUNKER_COLOR)
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.is_intact = True

    def destroy(self):
        """Erodes and hides block on projectile impact."""
        self.is_intact = False
        self.hideturtle()
        self.goto(3000, 3000)


class BunkerManager:
    def __init__(self):
        self.blocks: list[BunkerBlock] = []
        self._build_bunkers()

    def _build_bunkers(self):
        """Builds all 4 defense installations on the defense perimeter."""
        for cx in BUNKER_X_OFFSETS:
            self._build_single_bunker(center_x=cx, center_y=BUNKER_Y)

    def _build_single_bunker(self, center_x: float, center_y: float):
        """Instantiates the 5x4 block grid for one bunker."""
        cols = len(BUNKER_LAYOUT[0])
        rows = len(BUNKER_LAYOUT)
        
        start_x = center_x - ((cols - 1) * BLOCK_SIZE) / 2
        start_y = center_y - ((rows - 1) * BLOCK_SIZE) / 2

        for r_idx, row in enumerate(BUNKER_LAYOUT):
            for c_idx, val in enumerate(row):
                if val == 1:
                    bx = start_x + (c_idx * BLOCK_SIZE)
                    by = start_y + (r_idx * BLOCK_SIZE)
                    block = BunkerBlock(x=bx, y=by)
                    self.blocks.append(block)

    @property
    def intact_blocks(self) -> list[BunkerBlock]:
        return [b for b in self.blocks if b.is_intact]

    def check_projectile_hit(self, proj_x: float, proj_y: float, hit_radius: float = 14.0) -> BunkerBlock | None:
        """
        Tests if a projectile strikes any intact bunker block.
        Returns the struck BunkerBlock or None.
        """
        for block in self.intact_blocks:
            if abs(block.xcor() - proj_x) < hit_radius and abs(block.ycor() - proj_y) < hit_radius:
                return block
        return None

    def obliterate_at(self, alien_x: float, alien_y: float, radius: float = 24.0):
        """Destroys any blocks an invading alien body collides with."""
        for block in self.intact_blocks:
            if abs(block.xcor() - alien_x) < radius and abs(block.ycor() - alien_y) < radius:
                block.destroy()

    def reset(self):
        """Reconstructs all bunkers for a new game or wave."""
        for block in self.blocks:
            block.destroy()
        self.blocks.clear()
        self._build_bunkers()
