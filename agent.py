from random import choice
from constants import (
    Direction, MAZE_WIDTH, MAZE_HEIGHT,
    AGENT_ALPHA, AGENT_GAMMA, AGENT_EPSILON,
    REWARD_DOT, REWARD_POWER_PELLET, REWARD_WALL, REWARD_EMPTY
)

class PacManAgent:
    """Mini agent pour contrôler Pac-Man automatiquement"""
    
    def __init__(self, pacman, maze):
        self.pacman = pacman
        self.maze = maze
        self.qtable = {}
        self.alpha = AGENT_ALPHA
        self.gamma = AGENT_GAMMA
        self.epsilon = AGENT_EPSILON
        self.enabled = False
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def get_state(self):
        return (int(self.pacman.x), int(self.pacman.y))
    
    def get_reward(self, cell):
        if cell == '.':
            return REWARD_DOT
        elif cell == 'o':
            return REWARD_POWER_PELLET
        elif cell == '#':
            return REWARD_WALL
        else:
            return REWARD_EMPTY
    
    def get_action(self):
        """Obtenir la meilleure action selon l'état actuel"""
        state = self.get_state()
        
        if state not in self.qtable:
            self.qtable[state] = {
                Direction.UP: 0,
                Direction.DOWN: 0,
                Direction.LEFT: 0,
                Direction.RIGHT: 0
            }
        
        from random import random
        if random() < self.epsilon:
            return choice(list(Direction))
        else:
            return max(self.qtable[state], key=self.qtable[state].get)
    
    def update(self):
        """Mettre à jour l'agent (apprentissage)"""
        if not self.enabled:
            return
        
        state = self.get_state()
        action = self.get_action()
        
        self.pacman.set_direction(action)
        
        new_x = int(self.pacman.x)
        new_y = int(self.pacman.y)
        
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            cell = self.maze[new_y][new_x]
            reward = self.get_reward(cell)
            new_state = (new_x, new_y)
            
            if new_state not in self.qtable:
                self.qtable[new_state] = {
                    Direction.UP: 0,
                    Direction.DOWN: 0,
                    Direction.LEFT: 0,
                    Direction.RIGHT: 0
                }
            
            max_future_q = max(self.qtable[new_state].values())
            current_q = self.qtable[state][action]
            
            self.qtable[state][action] = current_q + self.alpha * (
                reward + self.gamma * max_future_q - current_q
            )

