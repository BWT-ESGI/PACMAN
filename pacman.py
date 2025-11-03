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
        if maze.can_move(self.x, self.y, self.next_direction):
            self.direction = self.next_direction
        
        if maze.can_move(self.x, self.y, self.direction):
            dx, dy = self.direction.value
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            if self.x < 0:
                self.x = MAZE_WIDTH - 1
            elif self.x >= MAZE_WIDTH:
                self.x = 0
    
    def can_move(self, maze, direction):
        return maze.can_move(self.x, self.y, direction)
    
    def set_direction(self, direction):
        self.next_direction = direction
    
    def draw(self, screen):
        import pygame
        # Convertir position monde en pixel : position entière = centre de cellule
        cell_x = int(self.x)
        cell_y = int(self.y)
        pixel_x = cell_x * CELL_SIZE + CELL_SIZE // 2
        pixel_y = cell_y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, YELLOW, (pixel_x, pixel_y), self.radius)

