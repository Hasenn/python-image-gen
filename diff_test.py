import random
import ntpath
from PIL import Image
from copy import deepcopy

#A very simple stochastic cellular automaton

N_STEPS = 15
SIZE = 100

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def get_moore_neighbourhood(i, j):
    return filter(lambda x : (0 <= x[0] < SIZE) and (0 <= x[1] < SIZE) ,[(i + k, j+l) for k in [-1,0,1] for l in [-1,0,1]])

def next_step(grid, seeds, p_direct, p_indirect):
    new_grid = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            for k,l in get_moore_neighbourhood(i,j):
                if (k,l) in seeds:
                    new_grid[i][j] += clamp(int(random.random() < p_direct) * 15, 0, 255)
                else:
                    new_grid[i][j] +=  clamp(int(random.random() < p_indirect) * new_grid[k][l], 0, 255)
    return new_grid

def main():
    img = Image.new("L", (SIZE,SIZE))
    random.seed()

    seeds = set()
    for i in range(200):
        k,l = random.randint(0,SIZE), random.randint(0,SIZE)
        if not ((k,l) in seeds):
            seeds.add((k,l))
    
    grid = [[0 for i in range(SIZE)] for j in range(SIZE)]
    p_direct = 0.1
    p_indirect = 0.05

    for i in range(N_STEPS):
        grid = next_step(grid,seeds,p_direct,p_indirect)
    
    for i in range(SIZE):
        for j in range(SIZE):
            img.putpixel((i,j),grid[i][j])
    print(__file__)
    #img.save(ntpath.dirname(__file__) + "diffusion.png")

if __name__ == "__main__":
    main()