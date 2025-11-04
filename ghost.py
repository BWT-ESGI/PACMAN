from constants import Direction, CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT, GHOST_SPEED

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = Direction.UP
        self.speed = GHOST_SPEED
        self.radius = CELL_SIZE // 2 - 2
        self.target_x = x
        self.target_y = y
        
    def update(self, maze, pacman):
        dx = pacman.x - self.x
        dy = pacman.y - self.y
        
        if abs(dx) > abs(dy):
            if dx > 0 and maze.can_move(self.x, self.y, Direction.RIGHT):
                self.direction = Direction.RIGHT
            elif dx < 0 and maze.can_move(self.x, self.y, Direction.LEFT):
                self.direction = Direction.LEFT
        else:
            if dy > 0 and maze.can_move(self.x, self.y, Direction.DOWN):
                self.direction = Direction.DOWN
            elif dy < 0 and maze.can_move(self.x, self.y, Direction.UP):
                self.direction = Direction.UP
        
        if maze.can_move(self.x, self.y, self.direction):
            dx, dy = self.direction.value
            self.x += dx * self.speed
            self.y += dy * self.speed
    
    def can_move(self, maze, direction):
        return maze.can_move(self.x, self.y, direction)
    
    def draw(self, screen):
        import pygame
        cell_x = int(self.x)
        cell_y = int(self.y)
        pixel_x = cell_x * CELL_SIZE + CELL_SIZE // 2
        pixel_y = cell_y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, self.color, (pixel_x, pixel_y), self.radius)

