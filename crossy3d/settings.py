"""
Crossy Road 3D - Global settings and constants.
"""

# Display
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Crossy Road 3D"
FULLSCREEN = False
VSYNC = True

# Grid / World
TILE_SIZE = 1.0
LANE_DEPTH = 1.0  # depth of each lane along forward axis (Z)
LANE_WIDTH = 5    # number of tiles per lane (X axis)
WORLD_FORWARD_AXIS = "z"  # positive Z = forward
FORWARD_SIGN = 1

# Player
PLAYER_HOP_DURATION = 0.25  # seconds per hop
PLAYER_HOP_HEIGHT = 0.35    # arc height for hop
PLAYER_SQUASH_SCALE = 0.85  # squash at land
INPUT_BUFFER_MAX = 1       # queued moves during hop

# Camera (isometric / trailing) – zoomed in to fill view and reduce blank areas
CAMERA_DISTANCE = 6.5
CAMERA_HEIGHT = 4.5
CAMERA_ANGLE = 32.0        # degrees from horizontal
CAMERA_SMOOTHING = 8.0     # follow speed (higher = snappier)
CAMERA_LOOK_AHEAD = 1.5    # look slightly ahead of player

# Lanes - generation
LANES_AHEAD = 15           # lanes to generate in front
LANES_BEHIND_CULL = 3      # cull lanes this many behind player
MIN_SAFE_LANES = 2         # min grass between roads/rivers
MAX_CONSECUTIVE_HAZARD = 2 # max roads/trains in a row
MAX_CONSECUTIVE_RIVER = 3  # rivers can repeat (2–3 water lanes) so it looks like continuous water, not a train

# Grass
GRASS_BLOCKER_CHANCE = 0.15  # chance per tile for tree/rock
GRASS_BLOCKER_CLUSTER = 0.3  # chance to add adjacent blocker

# Road
ROAD_LANE_CHANCE = 0.25
ROAD_VEHICLE_GAP_MIN = 2   # min tiles between cars
ROAD_VEHICLE_GAP_MAX = 4
ROAD_VEHICLE_SPEED_MIN = 2.0
ROAD_VEHICLE_SPEED_MAX = 6.0
ROAD_VEHICLES_PER_LANE_MIN = 1
ROAD_VEHICLES_PER_LANE_MAX = 3

# River (repeated water lanes so it feels like ocean/rivers, not a single train-like strip)
RIVER_LANE_CHANCE = 0.28
RIVER_LOG_GAP_MIN = 1
RIVER_LOG_GAP_MAX = 3
RIVER_LOG_SPEED_MIN = 1.5
RIVER_LOG_SPEED_MAX = 4.0
RIVER_LOG_LENGTH_MIN = 2
RIVER_LOG_LENGTH_MAX = 4
RIVER_DROWN_DELAY = 0.5    # seconds in water before death

# Train
TRAIN_LANE_CHANCE = 0.08
TRAIN_WARNING_TIME = 2.0   # seconds warning before train
TRAIN_SPEED = 15.0
TRAIN_LENGTH = 8           # tiles

# Doom (eagle / stay too long)
DOOM_TIME = 12.0           # seconds without forward progress
DOOM_WARNING_TIME = 3.0

# Scoring
SCORE_PER_ROW = 1
SAVE_FILE = "best_score.json"

# Audio (paths relative to project; use placeholders if no files)
SOUND_HOP = "sounds/hop.ogg"
SOUND_DEATH = "sounds/death.ogg"
SOUND_SPLASH = "sounds/splash.ogg"
SOUND_TRAIN_HORN = "sounds/train_horn.ogg"
SOUND_SCORE = "sounds/score.ogg"
SOUND_DOOM = "sounds/doom.ogg"
AUDIO_ENABLED = True

# Debug
DEBUG_COLLISION_BOXES = False
DEBUG_SHOW_FPS = True
