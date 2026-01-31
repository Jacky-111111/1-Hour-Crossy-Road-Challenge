# 1-Hour Crossy Road Challenge

A **3D Crossy Road clone** in Python using **Panda3D**, with a **SpongeBob SquarePants** theme, procedural lanes, hazards, scoring, and UI.

## Requirements

- Python 3.8+
- Panda3D

## Install

```bash
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python crossy3d/main.py
```

Or from inside `crossy3d/`:

```bash
cd crossy3d && python main.py
```

## Controls

All controls are shown on screen as a reminder (start screen, in-game HUD, game over).

| Key | Action |
|-----|--------|
| **W / ↑ / Space** | Hop forward |
| **S / ↓** | Hop backward |
| **A / ←** | Hop left |
| **D / →** | Hop right |
| **Enter** | Start game / confirm |
| **R** | Restart (on game over) |
| **F1** | Toggle debug collision boxes |
| **Esc** | Quit |

**Restart:** You can press **R** or click the **Restart** button on the game over screen.

## Features

- **SpongeBob theme**: Start screen title “SpongeBob Crossy Road” and “Bikini Bottom 3D”; player is a SpongeBob-style character (yellow body, eyes, brown shorts). World includes Krusty Krab, Pineapple House, Squidward’s house, coral, palm trees, shells, jellyfish; boats and rafts; Bikini Bottom sky/ocean colors.
- **3D world**: Low-poly tiles, themed obstacles, boats, rafts, Bikini Bottom bus (train).
- **Grid movement**: One tile per hop with smooth ease-in/out animation and slight squash on land.
- **Camera**: Isometric/trailing camera, zoomed in to fill the view; smooth follow and death shake.
- **Lanes**: Procedural endless lanes (grass/sand, road, river, train) generated ahead and culled behind. Rivers can repeat (2–3 water lanes in a row) so water feels continuous.
- **Hazards**: Boats and bus kill on contact. **Water rule (Crossy Road):** You can only step onto water if a log/raft is under that tile; stepping into empty water is blocked. If you’re in water without a log, you drown after a short delay. Logs carry you.
- **Doom**: If you don’t move forward for too long, you’re eliminated.
- **Scoring**: Score increases for each new forward row; best score is saved to `best_score.json`.
- **UI**: Start screen (SpongeBob title + controls), in-game HUD (score, best, FPS, controls reminder), game over screen with **Restart** button and full controls reminder.
- **Audio**: Optional sound effects (hop, death, splash, train horn, score) if files are present in `sounds/`.

## Project layout

```
crossy3d/
  main.py              # Entry point
  settings.py          # Constants and tuning
  game/
    game_app.py        # Panda3D app, loop, state, collision
    state.py           # GameState enum
    input.py           # Input buffer and key mapping
    camera.py          # Smooth follow + death shake
    audio.py           # Sound effects (optional)
    ui.py              # Start / HUD / Game over + Restart button + controls
    save.py            # Best score load/save
  world/
    world_gen.py       # Procedural lane generation
    lane.py            # Lane types (grass, road, river, train)
    tiles.py           # Box geometry for tiles
    obstacles.py       # Bikini Bottom props (coral, palm, shell, jellyfish, buildings)
  entities/
    player.py          # SpongeBob-style character, grid movement, hop, ride-on-log
    vehicle.py         # Boat-style vehicles
    log.py             # River rafts
    train.py           # Bikini Bottom bus
  utils/
    math3d.py         # Grid ↔ world
    easing.py         # Hop and squash easing
```

## Audio (optional)

Place OGG files in a `sounds/` folder next to `crossy3d/`:

- `hop.ogg` – hop
- `death.ogg` – death
- `splash.ogg` – drown
- `train_horn.ogg` – bus/train warning
- `score.ogg` – new row / score
- `doom.ogg` – doom timer

The game runs without these; missing files are skipped.

## Platform

Tested on macOS; should run on Windows and Linux with Panda3D installed.
