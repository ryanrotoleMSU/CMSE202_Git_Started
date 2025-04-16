import numpy as np
import time
from IPython.display import clear_output
from common_plot import plotgrid  # import the emoji grid function

# Step 1: Create the forest with road, houses, and grass zones
forest = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],  # road
    [3, 3, 22, 3, 4, 4, 3, 22, 3, 3],
    [3, 3, 3, 22, 4, 4, 22, 3, 3, 3],
    [3, 3, 3, 3, 4, 4, 3, 3, 3, 3],
    [3, 3, 22, 4, 4, 4, 4, 22, 3, 3]
])

# Step 2: Start the tornado in a random top row cell
forest[0][np.random.choice(10)] = 13  # tornado marker

# Step 3: Define tornado movement step function
def step_forest(forest):
    new_forest = forest.copy()
    N = forest.shape[0]
    for i in range(N):
        for j in range(N):
            if forest[i, j] == 13:  # current tornado
                new_forest[i, j] = 14  # mark as destroyed
                spread_targets = []
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < N and 0 <= nj < N:
                        spread_targets.append((ni, nj))
                if spread_targets:
                    ni, nj = spread_targets[np.random.choice(len(spread_targets))]
                    new_forest[ni, nj] = 13  # new tornado position
    return new_forest

# Step 4: Define rescue plan
rescue_steps = {
    1: [(9, 2)], 2: [(9, 3)], 3: [(9, 4)],
    4: [(7, 3)], 5: [(7, 4)], 6: [(8, 4)],
    8: [(6, 2)], 9: [(5, 2)], 10: [(5, 3)],
    16: [(6, 7)], 17: [(5, 7)],
    24: [(7, 6)], 28: [(9, 7)]
}
rescue_targets = {(9,2), (7,3), (6,2), (6,7), (7,6), (9,7)}
rescued_times = {}
houses_destroyed = []

# Step 5: Run the simulation
for t in range(36):
    clear_output(wait=True)
    print(f"Step {t}")
    highlights = rescue_steps.get(t, [])

    # Log successful rescues
    for coord in highlights:
        if coord in rescue_targets and coord not in rescued_times and coord not in houses_destroyed:
            rescued_times[coord] = t

    # Tornado collision with house before rescue
    for i in range(10):
        for j in range(10):
            if forest[i, j] == 13:
                if (i,j) in rescue_targets and (i,j) not in rescued_times:
                    houses_destroyed.append((i,j))
                    print(f"💥 Tornado destroyed house at {i,j} before rescue!")
                elif (i,j) in highlights:
                    print(f"⚠️ Tornado hit EMS at {i,j}!")

    plotgrid(forest, highlight_roads=highlights, house_status=rescued_times, step_num=t)
    forest = step_forest(forest)
    time.sleep(0.5)

# Final rescue summary
print("\n✅ Rescue Summary:")
for house, time_step in rescued_times.items():
    print(f"🏠 House at {house} rescued at time {time_step}")

print("\n❌ Houses destroyed by tornado:")
for h in houses_destroyed:
    print(f"💥 {h}")

