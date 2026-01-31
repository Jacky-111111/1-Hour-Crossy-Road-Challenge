"""
Main game: init Panda3D, world, player, camera, UI, state machine, collision, scoring.
"""

import random
import math
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from panda3d.core import Vec3, Vec4, loadPrcFileData

import settings
from .state import GameState
from .input import InputManager, KEY_TO_DIR
from .camera import CameraController
from .audio import AudioManager
from .ui import UIManager
from .save import load_best_score, save_best_score
from world.lane import LaneType, GrassLane, RoadLane, RiverLane, TrainLane
from world.world_gen import WorldGenerator
from world import tiles as world_tiles
from world import obstacles as world_obstacles
from entities.player import Player
from entities.vehicle import Vehicle
from entities.log import Log
from entities.train import Train
from utils.math3d import grid_to_world


# Window and display (must be before ShowBase)
loadPrcFileData("", "window-title Crossy Road 3D")
loadPrcFileData("", "show-frame-rate-meter false")
loadPrcFileData("", f"win-size {settings.WINDOW_WIDTH} {settings.WINDOW_HEIGHT}")
loadPrcFileData("", f"fullscreen {'true' if settings.FULLSCREEN else 'false'}")


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0.4, 0.75, 0.95, 1)  # Bikini Bottom sky/ocean blue
        self.disableMouse()
        self.accept("escape", self.quit_game)
        # Match camera lens aspect ratio to window so 3D fills the window (no letterboxing)
        self._update_lens_aspect()
        self.accept("window-event", self._on_window_event)

        self.state = GameState.START
        self.score = 0
        self.best_score = load_best_score()
        self.max_reached_z = -1
        self.last_forward_time = 0.0
        self.drown_timer = 0.0
        self.in_water = False

        self.world_root = self.render.attachNewNode("world")
        self._setup_lighting()

        self.input_mgr = InputManager(settings.INPUT_BUFFER_MAX)
        self.camera_ctrl = CameraController(self)
        self.audio = AudioManager(self)
        self.audio.load_all()
        self.ui = UIManager(self)

        self.player = Player(self, self.world_root)
        self.world_gen = WorldGenerator()
        self.lanes = []  # list of (z_index, Lane, node_for_tiles, entities_list)
        self.vehicles = []
        self.logs = []
        self.trains = []
        self._lane_nodes = []
        self._lane_entities = []

        self._key_bindings()
        self.ui.show_start_screen()
        self.taskMgr.add(self._update_task, "update")
        self._frame_times = []

    def _setup_lighting(self):
        from panda3d.core import DirectionalLight, AmbientLight
        dlight = DirectionalLight("sun")
        dlight.setColor(Vec4(1, 1, 0.95, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -60, 0)
        self.render.setLight(dlnp)
        alight = AmbientLight("ambient")
        alight.setColor(Vec4(0.4, 0.45, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

    def _key_bindings(self):
        for key in ["w", "s", "a", "d", "space", "arrow_up", "arrow_down", "arrow_left", "arrow_right"]:
            self.accept(key, self._on_key, [key])
            self.accept(key + "-repeat", self._on_key, [key])
        self.accept("enter", self._on_enter)
        self.accept("return", self._on_enter)
        self.accept("r", self._on_restart)
        self.accept("f1", self._toggle_debug)

    def _on_key(self, key):
        if self.state == GameState.START:
            return
        if self.state == GameState.GAME_OVER:
            return
        direction = KEY_TO_DIR.get(key)
        if direction:
            self.input_mgr.push_direction(direction)

    def _on_enter(self):
        if self.state == GameState.START:
            self.state = GameState.PLAYING
            self.ui.hide_all()
            self.ui.show_hud(self.score, self.best_score)
            self._ensure_lanes()
            self.last_forward_time = self.taskMgr.globalClock.getFrameTime()
        elif self.state == GameState.GAME_OVER:
            self._on_restart()

    def _on_restart(self):
        if self.state != GameState.GAME_OVER:
            return
        self._reset_world()
        self.state = GameState.PLAYING
        self.score = 0
        self.max_reached_z = -1
        self.last_forward_time = self.taskMgr.globalClock.getFrameTime()
        self.ui.hide_all()
        self.ui.show_hud(self.score, self.best_score)
        self._ensure_lanes()

    def _toggle_debug(self):
        settings.DEBUG_COLLISION_BOXES = not getattr(settings, "DEBUG_COLLISION_BOXES", False)

    def _update_lens_aspect(self):
        """Set camera lens aspect ratio to window size so the view fills the window."""
        if self.win:
            w, h = self.win.getXSize(), self.win.getYSize()
            if h > 0:
                self.camLens.setAspectRatio(w / h)

    def _on_window_event(self, event):
        """On resize, keep lens aspect ratio matched to window."""
        self._update_lens_aspect()

    def _reset_world(self):
        for node in self._lane_nodes:
            node.removeNode()
        self._lane_nodes = []
        for ent_list in self._lane_entities:
            for e in ent_list:
                if hasattr(e, "remove"):
                    e.remove()
        self._lane_entities = []
        self.lanes = []
        self.vehicles = []
        self.logs = []
        self.trains = []
        self.world_gen = WorldGenerator()
        self.player.reset(settings.LANE_WIDTH // 2, 0)
        self.drown_timer = 0.0
        self.in_water = False

    def _ensure_lanes(self):
        """Generate lanes so we have LANES_AHEAD ahead of player."""
        player_z = self.player.grid_z
        need_up_to = player_z + settings.LANES_AHEAD
        while len(self.lanes) == 0 or self.lanes[-1][0] < need_up_to:
            z_idx = (self.lanes[-1][0] + 1) if self.lanes else 0
            lane = self.world_gen.next_lane(z_idx)
            node, entities = self._build_lane_visual(lane)
            self.lanes.append((z_idx, lane, node, entities))
            self._lane_nodes.append(node)
            self._lane_entities.append(entities)
            for e in entities:
                if isinstance(e, Vehicle):
                    self.vehicles.append(e)
                elif isinstance(e, Log):
                    self.logs.append(e)
                elif isinstance(e, Train):
                    self.trains.append(e)
                    self.audio.play_train_horn()

    def _build_lane_visual(self, lane):
        """Create tile + obstacle/entity visuals for a lane. Returns (root_node, entities_list)."""
        root = self.world_root.attachNewNode(f"lane_{lane.z_index}")
        ts = settings.TILE_SIZE
        lane_z = lane.z_index * ts
        entities = []
        if isinstance(lane, GrassLane):
            for x in range(settings.LANE_WIDTH):
                world_tiles.create_grass_tile(self.loader, root, x * ts, lane_z)
            for (gx, gz) in lane.blocked_tiles:
                world_obstacles.create_bikini_bottom_prop(self.loader, root, gx * ts, lane_z)
        elif isinstance(lane, RoadLane):
            for x in range(settings.LANE_WIDTH):
                world_tiles.create_road_tile(self.loader, root, x * ts, lane_z)
            gap_min = settings.ROAD_VEHICLE_GAP_MIN
            gap_max = settings.ROAD_VEHICLE_GAP_MAX
            n_vehicles = random.randint(
                settings.ROAD_VEHICLES_PER_LANE_MIN,
                settings.ROAD_VEHICLES_PER_LANE_MAX,
            )
            used = set()
            for _ in range(n_vehicles):
                gx = random.randint(0, settings.LANE_WIDTH - 1)
                if gx in used:
                    continue
                gap = random.randint(gap_min, gap_max)
                for dx in range(-gap, gap + 1):
                    used.add(gx + dx)
                v = Vehicle(self, root, lane_z, gx, lane.direction, lane.speed)
                entities.append(v)
        elif isinstance(lane, RiverLane):
            world_tiles.create_water_lane_surface(self.loader, root, lane_z)
            log_len_min = settings.RIVER_LOG_LENGTH_MIN
            log_len_max = settings.RIVER_LOG_LENGTH_MAX
            x = 0
            while x < settings.LANE_WIDTH:
                length = random.randint(log_len_min, log_len_max)
                length = min(length, settings.LANE_WIDTH - x)
                if length <= 0:
                    break
                start_x = (x + length / 2) * ts
                log = Log(self, root, lane_z, start_x, length, lane.direction, lane.speed)
                entities.append(log)
                gap = random.randint(settings.RIVER_LOG_GAP_MIN, settings.RIVER_LOG_GAP_MAX)
                x += length + gap
            # Guarantee at least 2 logs so river is always crossable (logs also wrap)
            if len(entities) == 0:
                length = min(log_len_max, settings.LANE_WIDTH)
                start_x = (settings.LANE_WIDTH / 2) * ts
                log = Log(self, root, lane_z, start_x, length, lane.direction, lane.speed)
                entities.append(log)
            if len(entities) == 1:
                # Add a second log offset so there's always coverage as they move
                length = random.randint(log_len_min, log_len_max)
                length = min(length, settings.LANE_WIDTH)
                start_x = (settings.LANE_WIDTH * 0.25) * ts if lane.direction > 0 else (settings.LANE_WIDTH * 0.75) * ts
                log2 = Log(self, root, lane_z, start_x, length, lane.direction, lane.speed)
                entities.append(log2)
        elif isinstance(lane, TrainLane):
            for x in range(settings.LANE_WIDTH):
                world_tiles.create_rail_tile(self.loader, root, x * ts, lane_z)
            train = Train(self, root, lane_z, random.choice([-1, 1]))
            entities.append(train)
        root.flattenStrong()
        return root, entities

    def _update_task(self, task):
        dt = globalClock.getDt()
        if dt > 0.1:
            dt = 0.016
        self._frame_times.append(dt)
        if len(self._frame_times) > 60:
            self._frame_times.pop(0)
        fps = 1.0 / (sum(self._frame_times) / len(self._frame_times)) if self._frame_times else 0

        if self.state == GameState.START:
            self.ui.update_hud(0, self.best_score, fps)
            return Task.cont
        if self.state == GameState.GAME_OVER:
            return Task.cont

        # PLAYING
        self._ensure_lanes()
        self._cull_lanes()
        self._process_input()
        self.player.update(dt)
        self._update_entities(dt)
        self._check_river_and_logs()
        self._check_collisions()
        self._check_doom(dt)
        self._update_score()
        self.camera_ctrl.set_target_from_player(self.player.grid_x, self.player.grid_z)
        self.camera_ctrl.update(dt)
        self.ui.update_hud(self.score, self.best_score, fps)
        return Task.cont

    def _cull_lanes(self):
        player_z = self.player.grid_z
        cull_before = player_z - settings.LANES_BEHIND_CULL
        while self.lanes and self.lanes[0][0] < cull_before:
            z_idx, lane, node, entities = self.lanes.pop(0)
            node.removeNode()
            self._lane_nodes.pop(0)
            for e in entities:
                if isinstance(e, Vehicle) and e in self.vehicles:
                    self.vehicles.remove(e)
                elif isinstance(e, Log) and e in self.logs:
                    self.logs.remove(e)
                elif isinstance(e, Train) and e in self.trains:
                    self.trains.remove(e)
                if hasattr(e, "remove"):
                    e.remove()
            self._lane_entities.pop(0)

    def _process_input(self):
        if not self.player.alive:
            return
        # Consume buffer or current key: one move per frame when not hopping
        if not self.player.is_hopping():
            direction = self.input_mgr.pop_direction()
            if direction:
                self._try_player_move(direction)
        else:
            # Buffer next move
            direction = self.input_mgr.pop_direction()
            if direction:
                self.input_mgr.push_direction(direction)

    def _is_tile_on_log(self, grid_x: int, grid_z: int) -> bool:
        """True if (grid_x, grid_z) is currently covered by a log (required to stand on water)."""
        ts = settings.TILE_SIZE
        center_x = grid_x * ts
        center_z = grid_z * ts
        for log in self.logs:
            if abs(log.lane_z - center_z) > ts * 0.5:
                continue
            if log.contains_point(center_x, center_z):
                return True
        return False

    def _try_player_move(self, direction: str):
        def is_blocked(nx, nz):
            if nx < 0 or nx >= settings.LANE_WIDTH:
                return True
            if nz < 0:
                return True
            for (z_idx, lane, _n, _e) in self.lanes:
                if z_idx != nz:
                    continue
                if isinstance(lane, RiverLane):
                    # Crossy Road rule: can only step onto water if a log/block is under that tile
                    if not self._is_tile_on_log(nx, nz):
                        return True
                    break
                if lane.is_blocked(nx):
                    return True
            return False
        if self.player.try_move(direction, is_blocked):
            self.audio.play_hop()
            if direction == "up":
                self.last_forward_time = self.taskMgr.globalClock.getFrameTime()
            self.player.riding_log = None

    def _update_entities(self, dt):
        for v in self.vehicles:
            v.update(dt)
        for log in self.logs:
            log.update(dt)
        for t in self.trains:
            t.update(dt)
            if t.is_warning():
                pass  # could flash warning light / play horn once
        # Ride on log: if player is in river lane and on a log, carry
        self._update_log_ride()

    def _update_log_ride(self):
        ts = settings.TILE_SIZE
        px, pz = self.player.get_world_pos()
        player_lane_z = self.player.grid_z * ts
        on_log = None
        for log in self.logs:
            if abs(log.lane_z - player_lane_z) > ts * 0.5:
                continue
            if log.contains_point(px, pz):
                on_log = log
                break
        if on_log:
            self.player.riding_log = on_log
            offset_x = (px - on_log.world_x) / ts
            offset_z = (pz - on_log.lane_z) / ts
            self.player.set_position_from_log(on_log.world_x, on_log.lane_z, offset_x, offset_z)
        else:
            self.player.riding_log = None

    def _check_river_and_logs(self):
        ts = settings.TILE_SIZE
        player_lane_z = self.player.grid_z * ts
        in_river = False
        for (z_idx, lane, _n, _e) in self.lanes:
            if not isinstance(lane, RiverLane):
                continue
            lane_z = z_idx * ts
            if abs(lane_z - player_lane_z) > ts * 0.3:
                continue
            in_river = True
            break
        if in_river and not self.player.riding_log:
            self.in_water = True
            self.drown_timer += globalClock.getDt()
            if self.drown_timer >= settings.RIVER_DROWN_DELAY:
                self._die("drown")
        else:
            self.in_water = False
            self.drown_timer = 0.0

    def _check_collisions(self):
        if not self.player.alive:
            return
        px, pz = self.player.get_world_pos()
        ts = settings.TILE_SIZE
        half = ts * 0.35
        for v in self.vehicles:
            min_x, max_x, min_z, max_z = v.get_bounds()
            if px + half >= min_x and px - half <= max_x and pz + half >= min_z and pz - half <= max_z:
                self._die("vehicle")
                return
        for t in self.trains:
            if not t.is_active():
                continue
            min_x, max_x, min_z, max_z = t.get_bounds()
            if px + half >= min_x and px - half <= max_x and pz + half >= min_z and pz - half <= max_z:
                self._die("train")
                return

    def _check_doom(self, dt):
        if not self.player.alive:
            return
        t = self.taskMgr.globalClock.getFrameTime()
        if t - self.last_forward_time >= settings.DOOM_TIME:
            self._die("doom")

    def _update_score(self):
        if self.player.grid_z > self.max_reached_z:
            self.max_reached_z = self.player.grid_z
            self.score += settings.SCORE_PER_ROW
            self.audio.play_score()
            if self.score > self.best_score:
                self.best_score = self.score
                save_best_score(self.best_score)
        self.world_gen.set_score(self.score)

    def _die(self, reason: str):
        if not self.player.alive:
            return
        self.player.kill()
        self.camera_ctrl.trigger_death_shake()
        if reason == "drown":
            self.audio.play_splash()
        elif reason == "train":
            self.audio.play_train_horn()
        elif reason == "doom":
            self.audio.play_doom()
        else:
            self.audio.play_death()
        self.state = GameState.GAME_OVER
        self.ui.show_game_over(self.score, self.best_score, on_restart=self._on_restart)

    def quit_game(self):
        self.userExit()
