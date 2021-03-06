# Smart Snake

Semestral project for BI-PYT - solving the game of Snake with AI. Comparison of different control algorithms attempting to solve the game. For results and implementation details see [report.pdf](https://github.com/kosorpet/smart-snake/blob/main/report.pdf)

## Installation

Use pip install -r requirements.txt for requirements 

```bash
pip install -r requirements.txt
```

## Usage
For keyboard play:

```bash
python smart_snake_game.py --keyboard
```

For A* pathfinding:
```bash
python smart_snake_game.py --astar
```

For Reinforcement learning:
```bash
python smart_snake_game.py --reinforcement
```

For Genetic algorithm:
```bash
python smart_snake_game.py --genetic
```

For testing:
```bash
pytest
```

![snake](https://github.com/kosorpet/smart-snake/blob/main/gif/snake.gif)

