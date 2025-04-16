import numpy as np
import random
import time
from IPython.display import clear_output

class TownBoard:
    def __init__(self, size=20, num_houses=10):
        self.size = size
        self.num_houses = num_houses
        self.grid = np.zeros((size, size), dtype=int)
        self.cell_types = {
            0: {'name': 'tree', 'emoji': '🌲', 'flammable': True},
            1: {'name': 'house', 'emoji': '🏠', 'flammable': True},
            2: {'name': 'fire', 'emoji': '🔥', 'flammable': False},
            3: {'name': 'burned', 'emoji': '🪵', 'flammable': False},
            4: {'name': 'road', 'emoji': '⬛', 'flammable': False},
            5: {'name': 'tower', 'emoji': '🗼', 'flammable': False},
            6: {'name': 'car', 'emoji': '🚗', 'flammable': False},
            13: {'name':'tornado','emoji':'🌪️','flammable':False},
            14: {'name':'destroyed', 'emoji': '🪵', 'flammable': False}
        }
        self.warning_active = False
        self.house_paths = []
        self.cars = []
        self.car_times = []

    def generate_town(self):
        self.grid.fill(0)
        center = self.size // 2
        self.grid[center][center] = 5
        self.house_positions = []
        placed = 0
        while placed < self.num_houses:
            x, y = random.randint(1, self.size - 2), random.randint(1, self.size - 2)
            if self.grid[y][x] == 0:
                self.grid[y][x] = 1
                path = self._connect_to_edge(x, y)
                if path:
                    self.house_positions.append((x, y))
                    self.house_paths.append(path)
                    placed += 1

    def _connect_to_edge(self, x, y):
        edges = [(0, y), (self.size - 1, y), (x, 0), (x, self.size - 1)]
        ex, ey = min(edges, key=lambda pos: abs(pos[0] - x) + abs(pos[1] - y))
        path = []
        cx, cy = x, y
        while cx != ex:
            cx += 1 if ex > cx else -1
            if self.grid[cy][cx] == 0:
                self.grid[cy][cx] = 4
            path.append((cx, cy))
        while cy != ey:
            cy += 1 if ey > cy else -1
            if self.grid[cy][cx] == 0:
                self.grid[cy][cx] = 4
            path.append((cx, cy))
        return path

    def assign_cars(self):
        for path in self.house_paths:
            if not path:
                continue
            start = path[0]
            x, y = start
            delay = 0
            self.cars.append([x, y, path[:], delay, 0])  # (x, y, path, delay, steps)

    def move_cars(self):
        updated_cars = []
        for x, y, path, delay, steps in self.cars:
            if delay > 0:
                updated_cars.append([x, y, path, delay - 1, steps + 1])
                continue
            self.grid[y][x] = 4  # Leave behind a road
            if path:
                x, y = path.pop(0)
                if 0 <= x < self.size and 0 <= y < self.size:
                    self.grid[y][x] = 6
                    updated_cars.append([x, y, path, 0, steps + 1])
            else:
                self.car_times.append(steps)
        self.cars = updated_cars

    def display(self):
        clear_output(wait=True)
        if self.warning_active:
            print("\n🚨 TORNADO WARNING 🚨\n🚨 WEE-OO WEE-OO 🚨\n")
        for row in self.grid:
            print(' '.join(self.cell_types[cell]['emoji'] for cell in row))
        print("\nLegend: 🌲 Tree | 🏠 House | 🌪️ Tornado | 🪵 Destroyed | ⬛ Road | 🗼 Tower | 🚗 Car")


class TornadoSimulator:
    """Simulates a tornado moving through the town"""
    def __init__(self, town_board):
        self.board = town_board
        self.time_step = 0
        self.path = []

        x, y = random.randint(0, len(self.board.grid)-1), random.randint(0, len(self.board.grid)-1)
        starts=[(0,y),(x,0),(len(self.board.grid)-1,y),(x,len(self.board.grid)-1)]
        self.board.grid[starts[np.random.choice(len(starts))]]=13
        x,y=np.where(self.board.grid==13)
        self.path.append((x[0],y[0]))

        self.warning_triggered = False
        self.evacuated_reported = False

        
        self.board.warning_active = True
        self.board.assign_cars()
        self.warning_triggered = True
        self.destroyed_cars=[]
    
    def move(self):
        """move tornado to adjacent cells"""
        x,y=self.path[-1]
        options=[]
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    for k in range(4):
                        options.append((x+dx,y+dy))
                nx, ny = x+dx, y+dy
                if 0<=nx<len(self.board.grid) and 0<=ny<len(self.board.grid):
                    if (nx,ny) in self.path:
                        options.append((nx,ny))
                    else:
                        for k in range(3):
                            options.append((nx,ny))

        #set old to destroyed
        self.board.grid[(x,y)]=14
        
        #set tornado
        new=options[np.random.choice(len(options))]
        self.board.grid[new]=13
        self.path.append(new)
        self.time_step += 1

        
    def hit_check(self):
        #check whether it hit an occupied house or car
        for car in self.board.cars:
            if car[0]==self.path[-1][0] and car[1]==self.path[-1][0]:
                self.board.cars.remove(car)
                                
                
    
    def simulate(self, steps=50, delay=0.3):
        """Run complete tornado simulation"""
        for t in range(steps):
            self.board.display()
            self.move()
            self.hit_check()
            self.board.move_cars()
            time.sleep(delay)


# Example usage
if __name__ == "__main__":
    # Create town with random house clusters (20-40% coverage)
    town = TownBoard(15)
    town.generate_town()
    
    # Simulate fire spread
    fire = TornadoSimulator(town)
    fire.simulate(steps=10, delay=0.5)
    print("\n🚗 All vehicles evacuated!")
    for i, t in enumerate(town.car_times):
        print(f"Car {i+1} evacuated in {t} minutes")
    if town.car_times:
        print(f"Total evacuation time: {max(town.car_times)} minutes")
    print(len(fire.destroyed_cars),'car(s) destroyed')