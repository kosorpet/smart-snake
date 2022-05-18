import copy
import random
from math import sqrt, floor

import pyglet
from pyglet import window

from smart_snake.src.game.game import Game
from smart_snake.src.helper.helpers import plot
from smart_snake.src.models.individual import Individual

POPULATION_SIZE = 36
TOURNAMENT_SIZE = 10
MUTATION_PROBABILITY = 0.5


class GeneticController:
    def __init__(self):
        self.game_window = window.Window(1000, 1000, "Smart snake (Genetic)")
        self.population = self.create_population()
        self.games = self.create_games()
        self.generations = 0
        self.plot_scores = []
        self.plot_average_scores = []

        @self.game_window.event
        def on_draw():
            pass
            self.game_window.clear()
            for game in self.games:
                game.draw(score=False)

    def create_population(self):
        population = []
        for _ in range(POPULATION_SIZE):
            population.append(Individual())
        return population

    def create_games(self):
        width = self.game_window.width / sqrt(POPULATION_SIZE)
        height = self.game_window.height / sqrt(POPULATION_SIZE)
        games = []
        for i in range(floor(sqrt(POPULATION_SIZE))):
            for j in range(floor(sqrt(POPULATION_SIZE))):
                games.append(Game(width, height, i * width, j * height))
        return games

    def generation_done(self):
        return all([ind.done for ind in self.population])

    def generation_step(self):
        for ind, game in zip(self.population, self.games):
            ind.execute(game)

    def calculate_fitness(self):
        for ind, game in zip(self.population, self.games):
            ind.calculate_fitness(game)

    def reset(self):
        for ind, game in zip(self.population, self.games):
            ind.reset()
            game.reset()

    def selection(self):
        new_generation = []
        for _ in range(POPULATION_SIZE):
            # select random tournament, fittest individual continues
            winner = None
            best = 0
            for i in range(TOURNAMENT_SIZE):
                candidate = random.choice(self.population)
                if (candidate.fitness > best):
                    best = candidate.fitness
                    winner = candidate
            new_generation.append(copy.deepcopy(winner))
        self.population = new_generation

    def crossover(self):
        crossed = []
        for _ in range(POPULATION_SIZE):
            parentA = copy.deepcopy(random.choice(self.population))
            parentB = copy.deepcopy(random.choice(self.population))
            parentA.crossover(parentB)
            crossed.append(parentA)
        self.population = crossed

    def mutation(self):
        for ind in self.population:
            if random.uniform(0, 1) <= MUTATION_PROBABILITY:
                ind.mutate()

    def find_best(self):
        return max(g.snake.len for g in self.games)

    def calculate_average_score(self):
        return sum(g.snake.len for g in self.games) / POPULATION_SIZE

    def new_generation(self):
        # plot scores
        self.plot_scores.append(self.find_best())
        self.plot_average_scores.append(self.calculate_average_score())
        plot(self.plot_scores, self.plot_average_scores, "Evolution", "Generation", "Score")

        self.generations += 1
        # Execute steps of genetic algorithm
        self.calculate_fitness()
        self.selection()
        self.crossover()
        self.mutation()
        self.reset()

    def game_loop(self, dt):
        if not self.generation_done():
            self.generation_step()
            return
        self.new_generation()

    def run(self):
        pyglet.clock.schedule_interval(self.game_loop, 1 / 60)
        pyglet.app.run()
