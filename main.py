"""
main.py - Classic Space Invaders Arcade Game (Day 95 Portfolio Project).
Central game loop, 60 FPS update cycle, input dispatch, collision router, and state engine.
"""

from turtle import Screen
import turtle
import time

from player import Player
from laser import PlayerLaser, AlienBomb
from alien import AlienFleet, register_alien_shapes
from bunker import BunkerManager
from ufo import MysteryUFO
from scoreboard import ScoreBoard
import sound_effects

# Game States
STATE_START = "START"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_WAVE_CLEARED = "WAVE_CLEARED"
STATE_GAME_OVER = "GAME_OVER"


class SpaceInvadersGame:
    def __init__(self):
        # 1. Canvas Setup
        self.screen = Screen()
        self.screen.title("Space Invaders (1978 Arcade) — Day 95 Python Turtle")
        self.screen.bgcolor("#05050A")  # Deep space black/indigo
        self.screen.setup(width=800, height=700)
        self.screen.tracer(0)

        # 2. Register Custom Vector Shapes
        register_alien_shapes(self.screen)

        # 3. Game State & Controllers
        self.state = STATE_START
        self.wave_transition_time = 0.0

        # 4. Instantiate Entities
        self.scoreboard = ScoreBoard()
        self.player = Player()
        self.fleet = AlienFleet(self.screen, wave=1)
        self.bunkers = BunkerManager()
        self.ufo = MysteryUFO()

        self.player_lasers: list[PlayerLaser] = []
        self.alien_bombs: list[AlienBomb] = []

        # 5. Bind Controls
        self._bind_keys()
        self.scoreboard.show_start_screen()

    def _bind_keys(self):
        """Binds dual keyboard schemes (Arrows & WASD) for smooth continuous play."""
        self.screen.listen()

        # Left controls
        self.screen.onkeypress(lambda: self._set_player_moving("left", True), "Left")
        self.screen.onkeyrelease(lambda: self._set_player_moving("left", False), "Left")
        self.screen.onkeypress(lambda: self._set_player_moving("left", True), "a")
        self.screen.onkeyrelease(lambda: self._set_player_moving("left", False), "a")
        self.screen.onkeypress(lambda: self._set_player_moving("left", True), "A")
        self.screen.onkeyrelease(lambda: self._set_player_moving("left", False), "A")

        # Right controls
        self.screen.onkeypress(lambda: self._set_player_moving("right", True), "Right")
        self.screen.onkeyrelease(lambda: self._set_player_moving("right", False), "Right")
        self.screen.onkeypress(lambda: self._set_player_moving("right", True), "d")
        self.screen.onkeyrelease(lambda: self._set_player_moving("right", False), "d")
        self.screen.onkeypress(lambda: self._set_player_moving("right", True), "D")
        self.screen.onkeyrelease(lambda: self._set_player_moving("right", False), "D")

        # Action keys
        self.screen.onkey(self._handle_fire, "space")
        self.screen.onkey(self._toggle_pause, "p")
        self.screen.onkey(self._toggle_pause, "P")
        self.screen.onkey(self._handle_restart, "r")
        self.screen.onkey(self._handle_restart, "R")

    def _set_player_moving(self, direction: str, is_active: bool):
        if self.state != STATE_PLAYING:
            return
        if direction == "left":
            self.player.is_moving_left = is_active
        elif direction == "right":
            self.player.is_moving_right = is_active

    def _handle_fire(self):
        """Dispatches fire command or progresses state on start/game-over screens."""
        if self.state == STATE_START:
            self._start_game()
        elif self.state == STATE_GAME_OVER:
            self._restart_game()
        elif self.state == STATE_PLAYING:
            if self.player.can_fire():
                laser = PlayerLaser(x=self.player.xcor(), y=self.player.ycor() + 14)
                self.player_lasers.append(laser)
                sound_effects.play_laser_sound()

    def _handle_restart(self):
        """Restarts the game when in GAME_OVER state."""
        if self.state == STATE_GAME_OVER:
            self._restart_game()

    def _toggle_pause(self):
        if self.state == STATE_PLAYING:
            self.state = STATE_PAUSED
            self.scoreboard.show_paused()
        elif self.state == STATE_PAUSED:
            self.state = STATE_PLAYING
            self.scoreboard.clear_banner()

    def _start_game(self):
        self.state = STATE_PLAYING
        self.scoreboard.clear_banner()

    def _restart_game(self):
        """Cleans all projectiles and entities for a fresh arcade run."""
        self._clear_projectiles()
        self.fleet.clear()
        self.fleet = AlienFleet(self.screen, wave=1)
        self.bunkers.reset()
        self.ufo.reset()
        self.player.reset_position()
        self.scoreboard.reset_for_new_game()
        self.state = STATE_PLAYING

    def _clear_projectiles(self):
        for laser in self.player_lasers:
            laser.destroy()
        self.player_lasers.clear()
        for bomb in self.alien_bombs:
            bomb.destroy()
        self.alien_bombs.clear()

    def _next_wave(self):
        """Advances to next wave upon clearing the alien fleet."""
        self._clear_projectiles()
        self.scoreboard.next_wave()
        self.fleet = AlienFleet(self.screen, wave=self.scoreboard.wave)
        self.player.reset_position()
        self.state = STATE_PLAYING
        self.scoreboard.clear_banner()

    def run(self):
        """Master 60 FPS game loop."""
        try:
            while True:
                frame_start = time.time()

                if self.state == STATE_PLAYING:
                    self._update_playing()
                elif self.state == STATE_WAVE_CLEARED:
                    if time.time() >= self.wave_transition_time:
                        self._next_wave()

                self.screen.update()

                # Target 60 FPS (~16.6 ms per frame)
                elapsed = time.time() - frame_start
                sleep_time = max(0.001, 0.016 - elapsed)
                time.sleep(sleep_time)
        except (turtle.Terminator, KeyboardInterrupt):
            pass

    def _update_playing(self):
        # 1. Player continuous movement
        self.player.update_continuous_movement()

        # 2. Mystery UFO updates
        self.ufo.update()

        # 3. Alien Fleet marching & bomb drops
        new_bombs = self.fleet.update()
        if new_bombs:
            self.alien_bombs.extend(new_bombs)

        # 4. Player Laser updates & collisions
        for laser in list(self.player_lasers):
            laser.move()
            if not laser.is_active:
                continue

            # Collision: Laser vs Aliens
            hit_alien = False
            for alien in self.fleet.alive_aliens:
                if abs(laser.xcor() - alien.xcor()) < 22 and abs(laser.ycor() - alien.ycor()) < 18:
                    alien.destroy()
                    self.scoreboard.add_score(alien.points)
                    sound_effects.play_alien_hit_sound()
                    laser.destroy()
                    hit_alien = True
                    break
            if hit_alien:
                continue

            # Collision: Laser vs Mystery UFO
            if self.ufo.is_active:
                if abs(laser.xcor() - self.ufo.xcor()) < 26 and abs(laser.ycor() - self.ufo.ycor()) < 18:
                    pts = self.ufo.hit()
                    self.scoreboard.add_score(pts)
                    sound_effects.play_alien_hit_sound()
                    laser.destroy()
                    continue

            # Collision: Laser vs Bunkers
            bunker_hit = self.bunkers.check_projectile_hit(laser.xcor(), laser.ycor())
            if bunker_hit:
                bunker_hit.destroy()
                laser.destroy()
                sound_effects.play_bunker_hit_sound()
                continue

        # 5. Alien Bombs updates & collisions
        for bomb in list(self.alien_bombs):
            bomb.move()
            if not bomb.is_active:
                continue

            # Collision: Bomb vs Bunkers
            bunker_hit = self.bunkers.check_projectile_hit(bomb.xcor(), bomb.ycor())
            if bunker_hit:
                bunker_hit.destroy()
                bomb.destroy()
                sound_effects.play_bunker_hit_sound()
                continue

            # Collision: Bomb vs Player Ship
            if abs(bomb.xcor() - self.player.xcor()) < 22 and abs(bomb.ycor() - self.player.ycor()) < 18:
                bomb.destroy()
                sound_effects.play_player_hit_sound()
                has_lives = self.scoreboard.lose_life()
                if has_lives:
                    self.player.reset_position()
                else:
                    self.state = STATE_GAME_OVER
                    self.scoreboard.show_game_over("MOTHERSHIP DESTROYED — 0 LIVES LEFT")
                continue

        # 6. Alien Body vs Bunkers erosion
        for alien in self.fleet.alive_aliens:
            self.bunkers.obliterate_at(alien.xcor(), alien.ycor())

        # 7. Check Alien Fleet Breach (Touch Defense Baseline)
        if self.fleet.has_breached():
            self.state = STATE_GAME_OVER
            sound_effects.play_player_hit_sound()
            self.scoreboard.show_game_over("ALIENS INVADED EARTH DEFENSE LINE")
            return

        # 8. Check Wave Cleared
        if self.fleet.is_cleared():
            self.state = STATE_WAVE_CLEARED
            self.scoreboard.show_wave_cleared()
            self.wave_transition_time = time.time() + 1.8

        # 9. Clean inactive projectile lists
        self.player_lasers = [las for las in self.player_lasers if las.is_active]
        self.alien_bombs = [b for b in self.alien_bombs if b.is_active]


if __name__ == "__main__":
    game = SpaceInvadersGame()
    game.run()
