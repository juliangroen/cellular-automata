import copy
import random

import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
CELL_SIZE = 8
STATE_WIDTH = int((WINDOW_WIDTH - 16) / CELL_SIZE)
STATE_HEIGHT = int((WINDOW_HEIGHT - 16) / CELL_SIZE)
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
        # self.cell_state = [
        #     [random.choice([True, False]) for _ in range(STATE_WIDTH)]
        #     for _ in range(STATE_HEIGHT)
        # ]
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
            (int(WINDOW_WIDTH - CELL_SIZE * 2), 0),  # NE
            (0, int(WINDOW_HEIGHT - CELL_SIZE * 2)),  # SW
            (
                int(WINDOW_WIDTH - CELL_SIZE * 2),
                int(WINDOW_HEIGHT - CELL_SIZE * 2),
            ),  # SE
        ]
        corner_sprite_cords = [(0, 16), (16, 16), (0, 32), (16, 32)]

        width_sprite_total = int(WINDOW_WIDTH / CELL_SIZE)
        height_sprite_total = int(WINDOW_HEIGHT / CELL_SIZE)

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

        buttons_string = """\
SPACE = PAUSE
\n
LEFT CLICK = CREATE CELL
\n
RIGHT CLICK = DELETE CELL
\n
RETURN = TOGGLE AUTOMATA
\n
R = GENERATE RANDOM CELLS
"""

        pyxel.rect(start[0] + 4, start[1] + 4, width, height, 0)
        pyxel.rect(start[0], start[1], width, height, 5)
        pyxel.rect(start[0] + 4, start[1] + 4, width - 8, height - 8, 1)
        pyxel.text(start[0] + 32, start[1] + 16, "CELLULAR AUTOMATA", 6)
        pyxel.text(start[0] + 16, start[1] + 36, buttons_string, 6)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_RETURN):
            if not self.paused:
                self.running = not self.running
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.running:
                self.running = False
            self.paused = not self.paused
        if pyxel.btnp(pyxel.KEY_R):
            self.cell_state = [
                [random.choice([True, False]) for _ in range(STATE_WIDTH)]
                for _ in range(STATE_HEIGHT)
            ]
        if pyxel.btnp(pyxel.KEY_C):
            self.cell_state = [
                [False for _ in range(STATE_WIDTH)] for _ in range(STATE_HEIGHT)
            ]
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx = int(pyxel.mouse_x / CELL_SIZE)
            my = int(pyxel.mouse_y / CELL_SIZE)
            self.cell_state[my][mx] = not self.cell_state[my][mx]
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


App()
