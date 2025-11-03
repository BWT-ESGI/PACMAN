from constants import Direction, CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT, YELLOW, PACMAN_SPEED

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.speed = PACMAN_SPEED
        self.radius = CELL_SIZE // 2 - 2
        
    def update(self, maze):
        if self.can_move(maze, self.next_direction):
            self.direction = self.next_direction
        
        if self.can_move(maze, self.direction):
            dx, dy = self.direction.value
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            if self.x < 0:
                self.x = MAZE_WIDTH - 1
            elif self.x >= MAZE_WIDTH:
                self.x = 0
    
    def can_move(self, maze, direction):
        dx, dy = direction.value
        new_x = int(self.x + dx)
        new_y = int(self.y + dy)
        
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            return maze[new_y][new_x] != '#'
        return True
    
    def set_direction(self, direction):
        self.next_direction = direction
    
    def draw(self, screen):
        import pygame
        pygame.draw.circle(screen, YELLOW, 
                         (int(self.x * CELL_SIZE + CELL_SIZE // 2),
                          int(self.y * CELL_SIZE + CELL_SIZE // 2)), 
                         self.radius)

