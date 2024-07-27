import copy
import random

import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
CELL_SIZE = 8
STATE_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
STATE_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)
BPM = 120


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title="Conway's Game of Life", fps=60)
        pyxel.load("./assets.pyxres")
        # self.cell_state = [
        #     [False for _ in range(pyxel.width)] for _ in range(pyxel.height)
        # ]
        self.cell_state = [
            [random.choice([True, False]) for _ in range(STATE_WIDTH)]
            for _ in range(STATE_HEIGHT)
        ]
        self.running = False
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

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.running = not self.running
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
        for y_index, y_value in enumerate(self.cell_state):
            for x_index, x_value in enumerate(y_value):
                x_loc = x_index * CELL_SIZE
                y_loc = y_index * CELL_SIZE
                pyxel.dither(0.5)
                pyxel.blt(x_loc, y_loc, 0, 16, 0, CELL_SIZE, CELL_SIZE)
                pyxel.dither(1)
                if x_value:
                    pyxel.blt(x_loc, y_loc, 0, 0, 0, CELL_SIZE, CELL_SIZE, 0)


App()
