# 1-Hour Crossy Road Challenge

A **3D Crossy Road clone** in Python using **Panda3D**, with procedural lanes, hazards, scoring, and UI.

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

## Features

- **3D world**: Low-poly tiles, trees, rocks, cars, logs, trains.
- **Grid movement**: One tile per hop with smooth ease-in/out animation and slight squash on land.
- **Camera**: Isometric/trailing camera that follows the player with smoothing and a short death shake.
- **Lanes**: Procedural endless lanes (grass, road, river, train) generated ahead and culled behind.
- **Hazards**: Cars and trains kill on contact; water drowns unless you stand on a moving log (logs carry you).
- **Doom**: If you don’t move forward for too long, you’re eliminated.
- **Scoring**: Score increases for each new forward row; best score is saved to `best_score.json`.
- **UI**: Start screen, in-game HUD (score, best, FPS), game over screen with restart.
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
    ui.py              # Start / HUD / Game over text
    save.py            # Best score load/save
  world/
    world_gen.py       # Procedural lane generation
    lane.py            # Lane types (grass, road, river, train)
    tiles.py           # Box geometry for tiles
    obstacles.py      # Trees, rocks
  entities/
    player.py          # Grid movement, hop, ride-on-log
    vehicle.py        # Road cars
    log.py            # River logs
    train.py          # Train with warning
  utils/
    math3d.py         # Grid ↔ world
    easing.py         # Hop and squash easing
```

## Audio (optional)

Place OGG files in a `sounds/` folder next to `crossy3d/`:

- `hop.ogg` – hop
- `death.ogg` – death
- `splash.ogg` – drown
- `train_horn.ogg` – train warning
- `score.ogg` – new row / score
- `doom.ogg` – doom timer

The game runs without these; missing files are skipped.

## Platform

Tested on macOS; should run on Windows and Linux with Panda3D installed.
