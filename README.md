# 👾 Space Invaders — Day 95 Python Portfolio Project

A high-performance, arcade-authentic recreation of Tomohiro Nishikado's iconic 1978 arcade blockbuster **Space Invaders** (Taito / Midway), built in pure **Python** with Object-Oriented Architecture using the **`turtle`** graphics engine.

---

## 🎮 Game Overview & Mechanics

The player pilots an earth defense laser cannon along the bottom baseline to repel an invading armada of descending extraterrestrial invaders. As the alien fleet descends row by row, defensive bunkers erode under crossfire, the invaders' marching pace accelerates dramatically, and a high-value Mystery UFO periodically streaks across the upper atmosphere.

### 🌟 Key Features
- **Authentic 1978 Arcade Visuals & Custom Shapes**:
  - Distinct vector polygon contours for all three alien castes (Squid, Crab, Octopus), the Player Laser Cannon, and the Mystery Flying Saucer.
  - Classic retro color scheme (Magenta, Cyan, Yellow, Emerald Green, Crimson Red).
- **Synchronized Fleet March & Progressive Hardware Acceleration**:
  - The 24-alien armada marches in unison horizontally, drops down one tier upon reaching screen boundaries, and reverses heading.
  - As invaders are destroyed, the step interval dynamically accelerates from 0.65s down to a frantic 0.08s, recreating the classic hardware-load phenomenon that gave the original game its legendary tension.
- **Destructible Defensive Bunkers**:
  - 4 arch-shaped defensive fortifications positioned between the player and invaders.
  - Composed of discrete, destructible block segments that absorb and erode under incoming player lasers and alien bombs.
  - Descending aliens physically crush through and obliterate any remaining bunker segments.
- **Tactical Alien Counter-Attack**:
  - Column-aware bomb dropping: Only the lowest active alien in each column releases bombs, preventing internal collisions.
- **Mystery UFO (Flying Saucer)**:
  - Randomly crosses the top stratosphere with an audio warning chime.
  - Hitting the saucer awards classic mystery bonus points (`50`, `100`, `150`, or `300` pts).
- **Asynchronous Audio Synthesizer**:
  - Non-blocking background thread audio synthesis (`winsound.Beep`) producing authentic 4-tone heartbeat march cadence, laser beam blasts, explosion crunches, and UFO alarms.
  - Safe zero-lag cross-platform fallback.
- **Scoreboard HUD & Persistence**:
  - Real-time `SCORE`, `HI-SCORE` (persisted to `highscore.txt`), `WAVE` tracking, and visual ship icons for remaining lives.
- **Dual Controls & Quality of Life**:
  - Arrow keys (`←` / `→`) or WASD (`A` / `D`) with continuous keypress holding for silky 60 FPS motion.
  - Spacebar fire with weapon cooldown.
  - Pause / Resume (`P`).
  - Instant restart (`Space` or `R`) upon Game Over.

---

## 🕹️ Controls

| Action | Primary Key | Secondary Key |
| :--- | :--- | :--- |
| **Move Cannon Left** | `Left Arrow (←)` | `A` |
| **Move Cannon Right** | `Right Arrow (→)` | `D` |
| **Fire Laser Cannon** | `Spacebar` | — |
| **Pause / Resume** | `P` | — |
| **Start / Restart Game** | `Spacebar` | `R` |

---

## 📂 Project Architecture (OOP)

The codebase strictly follows clean Object-Oriented Programming (OOP) and Separation of Concerns:

```
Space_Invaders_Game_day95/
├── main.py              # Central game loop, 60 FPS update cycle, input dispatch & collision router
├── player.py            # Player spaceship turret, boundary clamping, weapon cooldown & continuous input
├── laser.py             # PlayerLaser and AlienBomb projectile classes with vector trajectory physics
├── alien.py             # Alien hierarchy and AlienFleet coordinator (march rhythm, boundary bounce, bombing)
├── bunker.py            # BunkerBlock and BunkerManager (4 destructible arch shield matrices)
├── ufo.py               # Mystery UFO saucer (intermittent stratosphere traverse & bonus points)
├── scoreboard.py        # Retro HUD, visual life icons, banner overlays & high score persistence
├── sound_effects.py     # Non-blocking async audio synthesis (winsound) with silent fallback
├── test_game_logic.py   # Headless automated unit & integration test suite
├── highscore.txt        # Local persistent high-score record
├── requirements.txt     # Locked project dependencies (Python 3.14 standard library)
└── README.md            # Architecture documentation & assignment reflection journal
```

---

## 🚀 How to Run

No external third-party packages required. Run directly with Python 3.10+:

```bash
# Run the game
py main.py
# or
python main.py

# Run the automated logic test suite
py test_game_logic.py
```

---

## 📝 Assignment Reflection Time (Journal)

> *Answers for the Day 95 Portfolio Project Submission:*

### 1. How did you approach the project?
I approached this project by decomposing the complex arcade state machine into discrete, modular components using strict Object-Oriented Programming (OOP), expanding significantly beyond previous 2D projects:
1. **Screen & Custom Vector Contours:** Instead of standard geometric primitives, I designed custom coordinate arrays for the 1978 arcade sprites (Squid, Crab, Octopus, Laser Cannon, and Mystery UFO) and registered them via Turtle's `Shape("compound")` API.
2. **Synchronized Fleet March Mechanics:** I treated the alien formation not as isolated wanderers, but as a single coordinated `AlienFleet` collective. A centralized march timer checks edge collisions for the entire active formation before applying directional reversal and vertical drops in unison.
3. **Hardware Acceleration Simulation:** I formulated a dynamic timing decay function ($T_{step} = T_{base} \cdot (\frac{N_{alive}}{N_{total}})^{0.85}$) to emulate the iconic 1978 Intel 8080 CPU hardware effect where fewer sprites on screen reduced processing overhead and accelerated the alien march.
4. **Destructible Defense Grids:** Rather than treating bunkers as solid walls, I built a `BunkerManager` managing 4 modular $5 \times 4$ block matrices. Projectiles trigger micro-erosion on impact, and descending aliens trample through them.
5. **Separation of Concerns:** Isolated input handling, vector physics, audio dispatch, and HUD updates into dedicated modules, tying them together within a deterministic 60 FPS master loop in `main.py`.

### 2. What was hard, what was easy?
* **What was easy:**
  - Setting up the basic `Player` paddle mechanics and boundary clamping logic, which came naturally from prior experience with Day 22 (Pong) and Day 87 (Breakout).
  - Creating the HUD, score counter, and banner overlays with Turtle text rendering.
* **What was hard:**
  - **Synchronous Edge Detection & Fleet Descent:** Ensuring that when an outer alien touches the screen edge, the *entire* fleet drops down exactly once and reverses heading without individual aliens desynchronizing or stuttering. This was solved by evaluating boundary lookahead across all living aliens before executing the group step.
  - **Non-blocking Audio Synchronization:** Classic Space Invaders relies heavily on audio feedback (the 4-tone march, beam shoots, explosions). In Python Turtle, standard synchronous audio calls like `winsound.Beep` block execution and freeze the animation loop. Moving all sound generation into background daemon threads completely eliminated frame drops.
  - **Column-Aware Alien Bombing:** Preventing alien bombs from spawning behind friendly invaders. I implemented a coordinate grouping algorithm that maps living aliens by horizontal column and selects strictly from the bottom-most vanguard.

### 3. How might you improve for the next project?
- **Sprite Animation Frames:** Add two alternating animation frames for each alien rank (arms up vs. arms down) on each march step, identical to the original arcade cabinet.
- **Progressive Weapon Upgrades:** Introduce temporary power-ups dropped by the Mystery UFO (e.g., twin-lasers, plasma shields, or speed boosts).
- **Dedicated Game Engine Transition:** For larger scale arcade titles with hundreds of simultaneous particles and explosions, transitioning from `turtle` to `pygame-ce` or `arcade` would provide hardware-accelerated sprite batching and higher rendering efficiency.

### 4. What was your biggest learning from today?
My biggest insight was understanding how early hardware limitations can inadvertently create iconic game design. The accelerating alien march in the original 1978 game wasn't an intentional feature at first—it occurred because the Intel 8080 processor had fewer pixels to redraw as aliens were killed. Recreating this dynamic acceleration through mathematical step scaling showed how technical constraints directly shape player psychology and emotional tension.

### 5. What would you do differently if you were to tackle this project again?
If building this from scratch again, I would implement a unified 2D spatial grid (Spatial Hashing or Quadtree) for collision queries. While pairwise distance checking between active projectiles, 24 aliens, and 64 bunker blocks is lightning-fast in this configuration, a spatial hash partition would generalize effortlessly to bullet-hell games with hundreds of simultaneous projectiles without any $O(N \cdot M)$ overhead.
