import copy
import random

import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
CELL_SIZE = 8
STATE_WIDTH = (WINDOW_WIDTH - 16) // CELL_SIZE
STATE_HEIGHT = (WINDOW_HEIGHT - 16) // CELL_SIZE
BPM = 120

######
# TODO
# - Finish border art and reduce grid to not include border cells
######


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Conway's Game of Life", fps=60)
        pyxel.load("./assets.pyxres")
        self.cell_state = [
            [False for _ in range(STATE_WIDTH)] for _ in range(STATE_HEIGHT)
        ]
        self.cursor_pos_x = 8
        self.cursor_pos_y = 8
        self.running = False
        self.paused = True
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def neighborhood_watch(self, x, y):
        neighbors = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        total = 0

        for nx, ny in neighbors:
            if 0 <= x + nx < STATE_WIDTH and 0 <= y + ny < STATE_HEIGHT:
                if self.cell_state[y + ny][x + nx]:
                    total += 1

        return total

    def automata(self):
        new_state = copy.deepcopy(self.cell_state)

        for y_index, y_value in enumerate(self.cell_state):
            for x_index, x_value in enumerate(y_value):
                alive_neighbors = self.neighborhood_watch(x_index, y_index)

                if x_value:
                    if alive_neighbors < 2 or alive_neighbors > 3:
                        new_state[y_index][x_index] = False
                    else:
                        new_state[y_index][x_index] = True
                else:
                    if alive_neighbors == 3:
                        new_state[y_index][x_index] = True

        self.cell_state = new_state

    def in_cell(self):
        board_origin = (8, 8)
        board_width = STATE_WIDTH * 8
        board_height = STATE_HEIGHT * 8

        if pyxel.mouse_x > board_origin[0] and pyxel.mouse_x < board_width:
            if pyxel.mouse_y > board_origin[1] and pyxel.mouse_y < board_height:
                cell_x = (pyxel.mouse_x - board_origin[0]) // 8
                cell_y = (pyxel.mouse_y - board_origin[1]) // 8

                return (cell_x, cell_y)

        return False

    def cells(self):
        for y_index, y_value in enumerate(self.cell_state):
            for x_index, x_value in enumerate(y_value):
                x_loc = (x_index + 1) * CELL_SIZE
                y_loc = (y_index + 1) * CELL_SIZE
                if x_value:
                    pyxel.blt(x_loc, y_loc, 0, 0, 0, CELL_SIZE, CELL_SIZE, 2)

    def window_frame(self):
        corner_cords = [
            (0, 0),  # NW
            (WINDOW_WIDTH - CELL_SIZE * 2, 0),  # NE
            (0, WINDOW_HEIGHT - CELL_SIZE * 2),  # SW
            (
                WINDOW_WIDTH - CELL_SIZE * 2,
                WINDOW_HEIGHT - CELL_SIZE * 2,
            ),  # SE
        ]
        corner_sprite_cords = [(0, 16), (16, 16), (0, 32), (16, 32)]

        width_sprite_total = WINDOW_WIDTH // CELL_SIZE
        height_sprite_total = WINDOW_HEIGHT // CELL_SIZE

        for unit in range(width_sprite_total):
            x = unit * CELL_SIZE
            # TOP BAR
            y = 0
            if unit > 0 and unit < (width_sprite_total - 1):
                pyxel.blt(x, y, 0, 32, 8, CELL_SIZE, CELL_SIZE)
            # BOTTOM BAR
            y = WINDOW_HEIGHT - CELL_SIZE
            if unit > 0 and unit < (width_sprite_total - 1):
                pyxel.blt(x, y, 0, 32, 8, CELL_SIZE, CELL_SIZE)

        for unit in range(height_sprite_total):
            x = 0
            # LEFT BAR
            y = unit * CELL_SIZE
            if unit > 0 and unit < (height_sprite_total - 1):
                pyxel.blt(x, y, 0, 48, 8, CELL_SIZE, CELL_SIZE)
            # BOTTOM BAR
            x = WINDOW_WIDTH - CELL_SIZE
            if unit > 0 and unit < (height_sprite_total - 1):
                pyxel.blt(x, y, 0, 48, 8, CELL_SIZE, CELL_SIZE)

        # CORNERS
        for corner, sprite in zip(corner_cords, corner_sprite_cords):
            pyxel.blt(
                corner[0],
                corner[1],
                0,
                sprite[0],
                sprite[1],
                CELL_SIZE * 2,
                CELL_SIZE * 2,
                0,
            )

    def menu(self):
        width = WINDOW_WIDTH / 2
        height = WINDOW_HEIGHT / 2
        start = (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 4)

        pyxel.rect(start[0] + 4, start[1] + 4, width, height, 0)
        pyxel.rect(start[0], start[1], width, height, 5)
        pyxel.rect(start[0] + 4, start[1] + 4, width - 8, height - 8, 1)

        pyxel.text(
            start[0] + 32,
            start[1] + 16,
            "CELLULAR AUTOMATA",
            (pyxel.frame_count // 8) % 16,
        )

        pyxel.text(start[0] + 8, start[1] + 32, "SPACE/(START) = PAUSE/PLAY", 6)
        pyxel.text(start[0] + 8, start[1] + 40, "MOUSE/D-PAD = MOVE CURSOR", 6)
        pyxel.text(start[0] + 8, start[1] + 48, "MOUSE1/(A) = TOGGLE CELL", 6)
        pyxel.text(start[0] + 8, start[1] + 56, "RETURN/(Y) = TOGGLE AUTOMATA", 6)
        pyxel.text(start[0] + 8, start[1] + 64, "R/(X) = FILL RANDOM CELLS", 6)
        pyxel.text(start[0] + 8, start[1] + 72, "C/(SELECT) = CLEAR CELLS", 6)
        pyxel.text(start[0] + 8, start[1] + 112, "PRESS Q/(B) NOW TO QUIT", 6)

    def cursor(self):
        pyxel.blt(
            self.cursor_pos_x, self.cursor_pos_y, 0, 24, 0, CELL_SIZE, CELL_SIZE, 0
        )

    def cursor_controller(self):
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if self.cursor_pos_y - 8 >= 8:
                self.cursor_pos_y -= 8
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.cursor_pos_y + 8 < STATE_HEIGHT * 8:
                self.cursor_pos_y += 8
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if self.cursor_pos_x - 8 >= 8:
                self.cursor_pos_x -= 8
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.cursor_pos_x + 8 < STATE_WIDTH * 8:
                self.cursor_pos_x += 8

    def update(self):
        self.cursor_controller()
        if self.paused:
            if pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                pyxel.quit()
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
            if not self.paused:
                self.running = not self.running
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            if self.running:
                self.running = False
            self.paused = not self.paused
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
            self.cell_state = [
                [random.choice([True, False]) for _ in range(STATE_WIDTH)]
                for _ in range(STATE_HEIGHT)
            ]
        if pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.cell_state = [
                [False for _ in range(STATE_WIDTH)] for _ in range(STATE_HEIGHT)
            ]
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.in_cell():
                cell_x, cell_y = self.in_cell()
                self.cell_state[cell_y][cell_x] = not self.cell_state[cell_y][cell_x]
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            x = (self.cursor_pos_x // CELL_SIZE) - 1
            y = (self.cursor_pos_y // CELL_SIZE) - 1
            self.cell_state[y][x] = not self.cell_state[y][x]
        if self.running:
            if pyxel.frame_count % 30 == 0:
                self.automata()

    def draw(self):
        pyxel.cls(0)
        pyxel.dither(0.5)
        pyxel.rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 1)
        pyxel.dither(1)
        self.cells()
        self.window_frame()
        if self.paused:
            self.menu()
        self.cursor()


App()
