import argparse
import random
import ntpath
from PIL import Image
from copy import deepcopy

def clamp(x, smallest, largest): return max(smallest, min(x, largest))

class Automaton:
    def __init__(self):
        pass
    def cell_step(self, grid, i, j, neighbours):
        pass

class Sim:
    def __init__(self, size_x, size_y, automaton):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[0 for i in range(size_y)] for j in range(size_x)]
        self.automaton : Automaton = automaton

    def get_moore_neighbourhood(self, i, j):
        return filter(
                lambda x : 
                    (0 <= x[0] < self.size_x) and (0 <= x[1] < self.size_y),
                [(i + k, j+l) for k in [-1,0,1] for l in [-1,0,1]]
                )
    
    def sim_step(self):
        new_grid = deepcopy(self.grid)
        for i in range(self.size_x):
            for j in range(self.size_y):
                new_grid[i][j] = clamp(
                    new_grid[i][j] + self.automaton.cell_step(
                        self.grid,
                        i, j,
                        self.get_moore_neighbourhood(i,j)),
                        0, 255
                        )
        return new_grid
    
    def advance(self, n):
        for i in range(n):
            self.grid = self.sim_step()
    
    def render_list(self,n):
        images = []
        for i in range(n):
            print(f'step {i+1} / {n}.', end='\r')
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
            print(f'step {step + 1} / {steps}.', end='\r')
            self.advance()
        print(f'rendering last step to {path}')
        image = self.render()
        image.save(f'{path}.png')

    def export_list(self,path,steps):
        images = self.render_list(steps)
        images[0].save(f'{path}.gif', save_all=True, append_images = images[1:], loop = 0)


