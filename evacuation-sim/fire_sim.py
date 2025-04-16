
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from IPython.display import clear_output
from common_plot import plotgrid

# Create forest grid (trees, roads, houses, etc.)
forest = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [3, 3, 22, 3, 4, 4, 3, 22, 3, 3],
    [3, 3, 3, 22, 4, 4, 22, 3, 3, 3],
    [3, 3, 3, 3, 4, 4, 3, 3, 3, 3],
    [3, 3, 22, 4, 4, 4, 4, 22, 3, 3]
])

# Randomly ignite a tree in top row
forest[0][np.random.choice(10)] = 2

# Fire spread logic
def step_forest(forest):
    new_forest = forest.copy()
    N = forest.shape[0]
    for i in range(N):
        for j in range(N):
            cell = forest[i, j]
            if cell == 2:
                new_forest[i, j] = 5
            elif cell == 5:
                new_forest[i, j] = 6
            elif cell == 6:
                new_forest[i, j] = 6
            if cell == 2:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < N and 0 <= nj < N and (dx != 0 or dy != 0):
                            if forest[ni, nj] == 1 and random.random() < 0.6:
                                new_forest[ni, nj] = 2
    return new_forest

# Simulate fire
for t in range(20):
    clear_output(wait=True)
    print(f"Step {t}")
    plotgrid(forest, step_num=t)
    forest = step_forest(forest)
    time.sleep(0.5)

