import copy
import random

import pyxel


class App:
    def __init__(self):
        pyxel.init(64, 64, title="Conway's Game of Life", fps=60)
        # self.cell_state = [
        #     [False for _ in range(pyxel.width)] for _ in range(pyxel.height)
        # ]
        self.cell_state = [
            [random.choice([True, False]) for _ in range(pyxel.width)]
            for _ in range(pyxel.height)
        ]
        self.running = True
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
            if 0 <= x + nx < pyxel.width and 0 <= y + ny < pyxel.height:
                if self.cell_state[y + ny][x + nx]:
                    total += 1

        return total

    def automata(self):
        new_state = copy.deepcopy(self.cell_state)

        for y_index, y_value in enumerate(self.cell_state):
            for x_index, x_value in enumerate(y_value):
                alive_neighbors = self.neighborhood_watch(x_index, y_index)
                print(alive_neighbors) if alive_neighbors > 1 else None

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
                [random.choice([True, False]) for _ in range(pyxel.width)]
                for _ in range(pyxel.height)
            ]
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.cell_state[pyxel.mouse_y][pyxel.mouse_x] = not self.cell_state[
                pyxel.mouse_y
            ][pyxel.mouse_x]
        if self.running:
            if pyxel.frame_count % 16 == 0:
                self.automata()

    def draw(self):
        pyxel.cls(0)
        for y_index, y_value in enumerate(self.cell_state):
            for x_index, x_value in enumerate(y_value):
                if x_value:
                    pyxel.pset(x_index, y_index, 6)


App()
