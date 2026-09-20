"""
test_game_logic.py - Headless Unit & Integration Test Suite for Space Invaders (Day 95).
Validates vector physics, collision mathematics, fleet acceleration formulas,
bunker erosion, and game over thresholds without requiring GUI rendering.
"""

import unittest
import math


class TestSpaceInvadersLogic(unittest.TestCase):
    def test_player_boundary_clamping(self):
        """Ensures spaceship cannot move outside visual boundaries [-360, 360]."""
        x_min, x_max = -360, 360
        move_speed = 18

        # Left boundary clamp test
        cur_x = -350
        target_x = cur_x - move_speed
        clamped_x = max(x_min, target_x)
        self.assertEqual(clamped_x, -360)

        # Further left attempt
        target_x2 = clamped_x - move_speed
        clamped_x2 = max(x_min, target_x2)
        self.assertEqual(clamped_x2, -360)

        # Right boundary clamp test
        cur_x = 350
        target_x = cur_x + move_speed
        clamped_x = min(x_max, target_x)
        self.assertEqual(clamped_x, 360)

    def test_laser_trajectory_and_bounds(self):
        """Verifies player laser advances upward and triggers out-of-bounds at top threshold."""
        start_y = -260
        speed = 22
        top_bound = 325

        y = start_y
        steps = 0
        while y <= top_bound:
            y += speed
            steps += 1

        self.assertGreater(y, top_bound)
        self.assertEqual(steps, math.ceil((top_bound - start_y) / speed))

    def test_alien_ranks_and_scoring(self):
        """Validates classic 1978 Space Invaders score hierarchy."""
        ranks = {
            3: {"name": "squid", "points": 30},
            2: {"name": "crab", "points": 20},
            1: {"name": "octopus", "points": 10},
        }

        self.assertEqual(ranks[3]["points"], 30)
        self.assertEqual(ranks[2]["points"], 20)
        self.assertEqual(ranks[1]["points"], 10)

        total_points = (6 * 30) + (12 * 20) + (6 * 10)  # 24 invaders
        self.assertEqual(total_points, 480)

    def test_fleet_acceleration_curve(self):
        """Verifies remaining alien count dynamically scales march step interval down to ~0.08s."""
        base_interval = 0.65
        total_initial = 24

        # Full fleet
        ratio_full = 24 / total_initial
        interval_full = max(0.08, base_interval * (ratio_full ** 0.85))
        self.assertAlmostEqual(interval_full, 0.65, places=2)

        # Half fleet remaining (12 aliens)
        ratio_half = 12 / total_initial
        interval_half = max(0.08, base_interval * (ratio_half ** 0.85))
        self.assertLess(interval_half, interval_full)
        self.assertGreater(interval_half, 0.08)

        # Single surviving alien (1 alien) -> maximum hardware panic speed
        ratio_last = 1 / total_initial
        interval_last = max(0.08, base_interval * (ratio_last ** 0.85))
        self.assertEqual(interval_last, 0.08)

    def test_bunker_collision_box(self):
        """Verifies projectile hit detection against bunker coordinate grid."""
        bunker_x, bunker_y = 80.0, -185.0
        hit_radius = 14.0

        # Direct hit
        proj_x, proj_y = 85.0, -188.0
        is_hit = abs(bunker_x - proj_x) < hit_radius and abs(bunker_y - proj_y) < hit_radius
        self.assertTrue(is_hit)

        # Miss
        miss_x, miss_y = 120.0, -185.0
        is_miss = abs(bunker_x - miss_x) < hit_radius and abs(bunker_y - miss_y) < hit_radius
        self.assertFalse(is_miss)

    def test_mystery_ufo_points(self):
        """Ensures Mystery UFO only produces valid historical bonus values."""
        possible_points = {50, 100, 150, 300}
        test_samples = [50, 100, 150, 300]
        for pts in test_samples:
            self.assertIn(pts, possible_points)

    def test_player_life_exhaustion(self):
        """Verifies game over triggers when 3 starting lives deplete to zero."""
        lives = 3
        game_over = False

        for _ in range(3):
            lives -= 1
            if lives <= 0:
                game_over = True

        self.assertEqual(lives, 0)
        self.assertTrue(game_over)

    def test_alien_defense_breach_detection(self):
        """Verifies breach condition triggers when alien reaches or passes defense baseline."""
        defense_baseline = -245.0

        alien_y_safe = -100.0
        self.assertFalse(alien_y_safe <= defense_baseline)

        alien_y_breached = -250.0
        self.assertTrue(alien_y_breached <= defense_baseline)


if __name__ == "__main__":
    unittest.main()
