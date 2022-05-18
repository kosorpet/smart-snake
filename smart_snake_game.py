import sys
from smart_snake.src.controllers.astar_controller import AStarController
from smart_snake.src.controllers.genetic_controller import GeneticController
from smart_snake.src.controllers.reinforcement_controller import ReinforcementController
from smart_snake.src.controllers.keyboard_controller import KeyboardController


def start_gamemode(arg):
    if arg == '--keyboard':
        KeyboardController().run()

    if arg == '--reinforcement':
        ReinforcementController().run()

    if arg == '--astar':
        AStarController().run()

    if arg == '--genetic':
        GeneticController().run()

def main():
    arg = read_args()
    if not ( arg == '--reinforcement' or arg == '--astar' or arg == '--keyboard' or arg == '--genetic'):
        print("Usage: python smart_snake [--keyboard | --astar | --reinforcement | --genetic]")
        return

    start_gamemode(arg)

def read_args():
    if len(sys.argv) != 2:
        print("Usage: python smart_snake [--keyboard | --astar | --reinforcement | --genetic]")
        return ''

    return sys.argv[1]

if __name__ == '__main__':
    main()



