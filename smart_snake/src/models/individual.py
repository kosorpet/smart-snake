import random
from smart_snake.src.models.neural_net_model import NNet
from smart_snake.src.helper.helpers import get_state
import torch


class Individual:
    def __init__(self):
        self.brain = NNet(11, 256, 3)
        self.done = False
        self.fitness = 0
        self.steps = 0

    def get_action(self, state):
        final_move = [0, 0, 0]
        state0 = torch.tensor(state, dtype=torch.float)
        prediction = self.brain(state0)
        # model can return raw number, get index of max value, convert to action
        move = torch.argmax(prediction).item()
        final_move[move] = 1
        return final_move

    def execute(self, game):
        if not self.done:
            state = get_state(game)
            action = self.get_action(state)
            self.done = game.update_action(action)
            self.steps += 1

    def reset(self):
        self.done = False
        self.steps = 0

    def calculate_fitness(self, game):
        self.fitness = 2 ** (game.snake.len + 4)

    def mutate_param(self, param):
        with torch.no_grad():
            if param.dim() == 1:
                for i in range(len(param)):
                    if random.uniform(0, 1) <= 0.5:
                        param.data[i] += random.uniform(-0.35, 0.35)

            elif param.dim() == 2:
                for i in range(len(param)):
                    for j in range(len(param[0])):
                        if random.uniform(0, 1) <= 0.5:
                            param.data[i][j] += random.uniform(-0.35, 0.35)

    def crossover_params(self, param1, param2):
        with torch.no_grad():
            if param1.dim() == 1:
                for i in range(len(param1)):
                    if random.uniform(0, 1) <= 0.5:
                        param1.data[i] = param2.data[i]

            elif param1.dim() == 2:
                for i in range(len(param1)):
                    for j in range(len(param1[0])):
                        if random.uniform(0, 1) <= 0.5:
                            param1.data[i][j] = param2.data[i][j]

    def crossover(self, other):
        for t1, t2 in zip(self.brain.parameters(), other.brain.parameters()):
            self.crossover_params(t1, t2)

    def mutate(self):
        for param in self.brain.parameters():
            self.mutate_param(param)
