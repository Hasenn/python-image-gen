import argparse
import random
import ntpath
import simulation

def clamp(x, smallest, largest): return max(smallest, min(x, largest))

class DiffusionAutomaton(simulation.Automaton):
    
    def __init__(self):
        self.probabilities = [
            [0.05,  0.1, 0.05 ],
            [0.01,  0.0,  0.1 ],
            [0.1, 0.01,  0.01]]
        self.values = [
            [-1,  0,  -2],
            [0,  0,  4 ],
            [1, 0,  -2]]
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("steps",    type=int)
    parser.add_argument("--seeds",  type=int, default=100)
    parser.add_argument("--size-x", type=int, default=120)
    parser.add_argument("--size-y", type=int, default=120)
    args = parser.parse_args()

    random.seed()

    sim = simulation.Sim(
        args.size_x,
        args.size_y,
        DiffusionAutomaton()
        )

    for i in range(args.seeds):
        k,l = random.randint(0,sim.size_x), random.randint(0,sim.size_y)
        if not ((k,l) in sim.automaton.seeds):
            sim.automaton.seeds.add((k,l))

    path = ntpath.dirname(
        ntpath.abspath(__file__)
    )
    sim.export(f'{path}/{args.name}',args.steps)