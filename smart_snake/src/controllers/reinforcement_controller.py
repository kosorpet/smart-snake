import torch
import random

from pyglet import window

from smart_snake.src.game.game import Game
from smart_snake.src.models.neural_net_model import NNet, QTrainer
from smart_snake.src.helper.helpers import get_state, plot
from collections import deque
import pyglet

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class AgentFunction:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # controls randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        # input layer size, hidden layer size, output size
        self.model = NNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        # random move
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        # get move from model
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # model can return raw number, get index of max value, convert to action
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


class ReinforcementController:
    def __init__(self):
        self.game_window = window.Window(800, 800, "Smart snake (Reinforcement)")
        self.game = Game(self.game_window.width, self.game_window.height)
        self.agent = AgentFunction()
        self.plot_scores = []
        self.total_score = 0

        @self.game_window.event
        def on_draw():
            self.game_window.clear()
            self.game.draw()

    def training_loop(self, dt):
        # get old state
        state_old = get_state(self.game)
        # get move
        final_move = self.agent.get_action(state_old)
        # perform move and get new state
        reward, done, score = self.game.update_action_reward(final_move)
        state_new = get_state(self.game)
        # train short memory
        self.agent.train_short_memory(state_old, final_move, reward, state_new, done)
        # remember
        self.agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            self.game.reset()
            self.agent.n_games += 1
            self.agent.train_long_memory()
            self.plot_scores.append(score)
            self.total_score += score
            plot(self.plot_scores, title="Training", xlabel="Games", ylabel="Score")

    def run(self):
        pyglet.clock.schedule_interval(self.training_loop, 1 / 30)
        pyglet.app.run()
