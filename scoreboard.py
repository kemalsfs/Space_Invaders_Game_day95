"""
scoreboard.py - Arcade HUD, lives tracking, banners, and high-score persistence.
Renders retro pixel fonts, visual player life icons, and state overlay announcements.
"""

from turtle import Turtle
import os

FONT_FAMILY = "Courier"
FONT_RETRO_HUD = (FONT_FAMILY, 14, "bold")
FONT_RETRO_LARGE = (FONT_FAMILY, 24, "bold")
FONT_RETRO_SUB = (FONT_FAMILY, 12, "normal")

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.txt")


class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.high_score = self._load_high_score()
        self.lives = 3
        self.wave = 1

        # Dedicated turtle for top HUD text (Score, High Score, Wave)
        self.hud_pen = Turtle()
        self.hud_pen.hideturtle()
        self.hud_pen.penup()
        self.hud_pen.speed(0)
        self.hud_pen.color("#FFFFFF")

        # Dedicated turtle for bottom status / line
        self.bottom_pen = Turtle()
        self.bottom_pen.hideturtle()
        self.bottom_pen.penup()
        self.bottom_pen.speed(0)
        self.bottom_pen.color("#00FF66")

        # Dedicated turtle for central banners (Game Over, Wave Cleared, Pause)
        self.banner_pen = Turtle()
        self.banner_pen.hideturtle()
        self.banner_pen.penup()
        self.banner_pen.speed(0)
        self.banner_pen.color("#FFFFFF")

        # Life indicator icon turtles
        self.life_icons: list[Turtle] = []

        self.draw_defense_line()
        self.update_hud()
        self.update_lives_display()

    def _load_high_score(self) -> int:
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                    return int(f.read().strip())
            except Exception:
                return 1500
        return 1500

    def _save_high_score(self):
        try:
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    def draw_defense_line(self):
        """Draws the classic arcade green defense threshold line across the bottom."""
        self.bottom_pen.clear()
        self.bottom_pen.color("#00FF66")
        self.bottom_pen.pensize(2)
        self.bottom_pen.goto(-380, -288)
        self.bottom_pen.pendown()
        self.bottom_pen.goto(380, -288)
        self.bottom_pen.penup()

    def update_hud(self):
        """Redraws top status: Score, High Score, and Wave level."""
        self.hud_pen.clear()
        self.hud_pen.goto(-360, 310)
        self.hud_pen.write(f"SCORE: {self.score:05d}", align="left", font=FONT_RETRO_HUD)

        self.hud_pen.goto(0, 310)
        self.hud_pen.write(f"HI-SCORE: {self.high_score:05d}", align="center", font=FONT_RETRO_HUD)

        self.hud_pen.goto(360, 310)
        self.hud_pen.write(f"WAVE: {self.wave:02d}", align="right", font=FONT_RETRO_HUD)

    def update_lives_display(self):
        """Draws remaining lives as mini cannon ships in the bottom left."""
        for icon in self.life_icons:
            icon.hideturtle()
        self.life_icons.clear()

        self.bottom_pen.goto(-360, -315)
        self.bottom_pen.color("#FFFFFF")
        self.bottom_pen.write("LIVES:", align="left", font=FONT_RETRO_HUD)

        # Draw mini icons for each remaining life
        for i in range(max(0, self.lives)):
            icon = Turtle()
            icon.hideturtle()
            icon.penup()
            icon.speed(0)
            icon.shape("square")
            icon.shapesize(stretch_wid=0.5, stretch_len=0.8)
            icon.color("#00FF66")
            icon.goto(-280 + (i * 26), -307)
            icon.showturtle()
            self.life_icons.append(icon)

    def add_score(self, pts: int):
        """Increments player score and checks for new all-time high score."""
        self.score += pts
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()
        self.update_hud()

    def lose_life(self) -> bool:
        """Decrements life counter. Returns True if lives remain, False if Game Over."""
        self.lives -= 1
        self.update_lives_display()
        return self.lives > 0

    def next_wave(self):
        """Advances to subsequent wave and awards wave-clear bonus."""
        self.wave += 1
        self.add_score(200)
        self.update_hud()

    def show_start_screen(self):
        """Displays arcade title and scoring reference card."""
        self.banner_pen.clear()
        self.banner_pen.goto(0, 110)
        self.banner_pen.color("#00FF66")
        self.banner_pen.write("SPACE INVADERS", align="center", font=FONT_RETRO_LARGE)

        self.banner_pen.goto(0, 50)
        self.banner_pen.color("#FFFFFF")
        table_text = (
            "* SCORE ADVANCE TABLE *\n\n"
            "= ?  MYSTERY UFO\n"
            "= 30 POINTS (SQUID)\n"
            "= 20 POINTS (CRAB)\n"
            "= 10 POINTS (OCTOPUS)"
        )
        self.banner_pen.write(table_text, align="center", font=FONT_RETRO_HUD)

        self.banner_pen.goto(0, -90)
        self.banner_pen.color("#FFFF00")
        self.banner_pen.write("[ PRESS SPACE TO DEFEND EARTH ]", align="center", font=FONT_RETRO_HUD)

        self.banner_pen.goto(0, -125)
        self.banner_pen.color("#AAAAAA")
        self.banner_pen.write("CONTROLS:  [<- / A] LEFT   [-> / D] RIGHT   [SPACE] FIRE   [P] PAUSE", align="center", font=FONT_RETRO_SUB)

    def show_paused(self):
        """Displays pause banner."""
        self.banner_pen.clear()
        self.banner_pen.goto(0, 30)
        self.banner_pen.color("#FFFF00")
        self.banner_pen.write("GAME PAUSED", align="center", font=FONT_RETRO_LARGE)
        self.banner_pen.goto(0, -10)
        self.banner_pen.color("#FFFFFF")
        self.banner_pen.write("Press P to resume", align="center", font=FONT_RETRO_HUD)

    def clear_banner(self):
        """Clears overlay messages."""
        self.banner_pen.clear()

    def show_game_over(self, reason: str = "ALIENS INVADED"):
        """Displays terminal game-over card with final score."""
        self.banner_pen.clear()
        self.banner_pen.goto(0, 40)
        self.banner_pen.color("#FF1744")
        self.banner_pen.write("GAME OVER", align="center", font=FONT_RETRO_LARGE)

        self.banner_pen.goto(0, 0)
        self.banner_pen.color("#FFAA00")
        self.banner_pen.write(reason, align="center", font=FONT_RETRO_HUD)

        self.banner_pen.goto(0, -35)
        self.banner_pen.color("#FFFFFF")
        self.banner_pen.write(f"FINAL SCORE: {self.score:05d}   |   WAVE REACHED: {self.wave}", align="center", font=FONT_RETRO_HUD)

        self.banner_pen.goto(0, -80)
        self.banner_pen.color("#00FF66")
        self.banner_pen.write("[ PRESS SPACE OR R TO RESTART ]", align="center", font=FONT_RETRO_HUD)

    def show_wave_cleared(self):
        """Displays interim victory banner before next wave."""
        self.banner_pen.clear()
        self.banner_pen.goto(0, 20)
        self.banner_pen.color("#00FF66")
        self.banner_pen.write(f"WAVE {self.wave} CLEARED!", align="center", font=FONT_RETRO_LARGE)
        self.banner_pen.goto(0, -20)
        self.banner_pen.color("#FFFFFF")
        self.banner_pen.write("+200 BONUS POINTS   *   NEXT FLEET ARRIVING...", align="center", font=FONT_RETRO_HUD)

    def reset_for_new_game(self):
        """Resets all metrics for a fresh start."""
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.clear_banner()
        self.update_hud()
        self.update_lives_display()
