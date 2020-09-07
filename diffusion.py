import argparse
import random
import ntpath
from PIL import Image
from copy import deepcopy

def clamp(x, smallest, largest): return max(smallest, min(x, largest))

class Automaton:
    
    def __init__(self):
        self.probabilities = [
            [0.05,  0.01, 0.05 ],
            [0.01,  0.0,  0.01 ],
            [0.01, 0.01,  0.01]]
        self.values = [
            [1,  0,  1],
            [0,  0,  0 ],
            [1, 0,  1]]
        self.seeds = set()
        self.p_direct = 0.2
        self.seed_value = 1
    def cell_step(self, grid, i, j, neighbours):
        s = 0
        for (k,l) in neighbours:
            s += int(random.random() < self.probabilities[k-i][l-j]) * self.values[k-i][l-j] * grid[k][l]
            if (k,l) in self.seeds:
                s += int(random.random() < self.p_direct) * self.seed_value
        return clamp(s,0,255)

class Simulation:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[0 for i in range(size_y)] for j in range(size_x)]
        self.automaton = Automaton()

    def get_moore_neighbourhood(self, i, j):
        return filter(
            lambda x : (0 <= x[0] < self.size_x) and (0 <= x[1] < self.size_y) ,
            [(i + k, j+l) for k in [-1,0,1] for l in [-1,0,1]])
    
    def sim_step(self):
        new_grid = deepcopy(self.grid)
        for i in range(self.size_x):
            for j in range(self.size_y):
                new_grid[i][j] = clamp(
                    new_grid[i][j] + self.automaton.cell_step(self.grid, i, j, self.get_moore_neighbourhood(i,j)),
                    0, 255)
        return new_grid
    
    def advance(self, n):
        for i in range(n):
            self.grid = self.sim_step()
    
    def animate(self,n):
        images = []
        for i in range(n):
            print(f'step {i+1} / {n}.')
            images.append(self.render())
            self.grid = self.sim_step()
        return images
    
    def render(self):
        img = Image.new("L", (self.size_x, self.size_y))
        for i in range(self.size_x):
            for j in range(self.size_y):
                img.putpixel((i,j), self.grid[i][j])
        return img

    def export(self,path,steps):
        for step in range(steps):
            print(f'step {step + 1} / {steps}.')
            self.advance()
        print(f'rendering last step to {path}')
        image = self.render()
        image.save(f'{path}.png')

    def export_gif(self,path,steps):
        images = self.animate(steps)
        images[0].save(f'{path}.gif',save_all=True,append_images = images[1:], loop = 0)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("steps", type=int)
    parser.add_argument("--seeds", type=int, default=100)
    args = parser.parse_args()

    random.seed()

    sim = Simulation(80,80)

    for i in range(args.seeds):
        k,l = random.randint(0,sim.size_x), random.randint(0,sim.size_y)
        if not ((k,l) in sim.automaton.seeds):
            sim.automaton.seeds.add((k,l))

    path = ntpath.dirname(
        ntpath.abspath(__file__)
    )
    sim.export_gif(f'{path}/{args.name}',args.steps)
