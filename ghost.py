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
        # IA simple : se diriger vers Pac-Man
        dx = pacman.x - self.x
        dy = pacman.y - self.y
        
        # Choisir la direction la plus proche
        if abs(dx) > abs(dy):
            if dx > 0 and self.can_move(maze, Direction.RIGHT):
                self.direction = Direction.RIGHT
            elif dx < 0 and self.can_move(maze, Direction.LEFT):
                self.direction = Direction.LEFT
        else:
            if dy > 0 and self.can_move(maze, Direction.DOWN):
                self.direction = Direction.DOWN
            elif dy < 0 and self.can_move(maze, Direction.UP):
                self.direction = Direction.UP
        
        # Déplacement
        if self.can_move(maze, self.direction):
            dx, dy = self.direction.value
            self.x += dx * self.speed
            self.y += dy * self.speed
    
    def can_move(self, maze, direction):
        dx, dy = direction.value
        new_x = int(self.x + dx)
        new_y = int(self.y + dy)
        
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
            return maze[new_y][new_x] != '#'
        return False
    
    def draw(self, screen):
        import pygame
        pygame.draw.circle(screen, self.color, 
                         (int(self.x * CELL_SIZE + CELL_SIZE // 2),
                          int(self.y * CELL_SIZE + CELL_SIZE // 2)), 
                         self.radius)

