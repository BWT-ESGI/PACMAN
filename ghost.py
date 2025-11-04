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
        self.has_left_spawn = False
    
    def is_in_spawn(self, x, y):
        """Vérifie si le ghost est dans la zone de spawn"""
        # Zone de spawn: x entre 12-16, y entre 8-11
        return 12 <= x <= 16 and 8 <= y <= 11
        
    def would_collide_with_ghost(self, maze, direction, other_ghosts):
        """Vérifie si se déplacer dans cette direction causerait une collision avec un autre ghost"""
        if not maze.can_move(self.x, self.y, direction):
            return True
        
        dx, dy = direction.value
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        new_cell_x = int(new_x)
        new_cell_y = int(new_y)
        
        current_cell_x = int(self.x)
        current_cell_y = int(self.y)
        
        for other_ghost in other_ghosts:
            if other_ghost == self:
                continue
            other_cell_x = int(other_ghost.x)
            other_cell_y = int(other_ghost.y)
            
            # Collision si dans la même cellule après le mouvement
            if new_cell_x == other_cell_x and new_cell_y == other_cell_y:
                return True
            
            # Vérifier aussi si l'autre ghost est dans notre cellule actuelle et veut aller dans la même direction
            if (current_cell_x == other_cell_x and current_cell_y == other_cell_y):
                other_dx, other_dy = other_ghost.direction.value
                if (other_dx == dx and other_dy == dy):
                    return True
        
        return False
    
    def update(self, maze, pacman, other_ghosts=None):
        if other_ghosts is None:
            other_ghosts = []
        
        cell_x = int(self.x)
        cell_y = int(self.y)
        
        # Si le ghost est encore dans le spawn, prioriser la sortie
        if not self.has_left_spawn and self.is_in_spawn(cell_x, cell_y):
            # Essayer de trouver une direction qui sort du spawn
            # Priorité: UP (sortie principale), puis LEFT/RIGHT, puis DOWN
            exit_directions = []
            
            # Tester toutes les directions possibles pour trouver celles qui sortent du spawn
            for direction in [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]:
                if maze.can_move(self.x, self.y, direction):
                    dx, dy = direction.value
                    new_cell_x = cell_x + dx
                    new_cell_y = cell_y + dy
                    # Si cette direction nous fait sortir du spawn, l'ajouter
                    if not self.is_in_spawn(new_cell_x, new_cell_y):
                        exit_directions.append(direction)
            
            # Si on a trouvé des directions de sortie, choisir la première (UP en priorité)
            if exit_directions:
                for direction in exit_directions:
                    if not self.would_collide_with_ghost(maze, direction, other_ghosts):
                        self.direction = direction
                        break
            else:
                # Sinon, essayer n'importe quelle direction valide pour bouger
                for direction in [Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN]:
                    if maze.can_move(self.x, self.y, direction) and not self.would_collide_with_ghost(maze, direction, other_ghosts):
                        self.direction = direction
                        break
            
            # Vérifier si on a quitté le spawn après le mouvement
            if maze.can_move(self.x, self.y, self.direction):
                dx, dy = self.direction.value
                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed
                new_cell_x = int(new_x)
                new_cell_y = int(new_y)
                
                if not self.is_in_spawn(new_cell_x, new_cell_y):
                    self.has_left_spawn = True
        else:
            # Une fois sorti du spawn, suivre Pac-Man normalement
            # Mais ne jamais revenir dans le spawn
            dx = pacman.x - self.x
            dy = pacman.y - self.y
            
            # Liste des directions possibles, en priorité vers Pac-Man
            preferred_directions = []
            
            # Déterminer les directions préférées vers Pac-Man
            if abs(dx) > abs(dy):
                if dx > 0:
                    preferred_directions.append(Direction.RIGHT)
                else:
                    preferred_directions.append(Direction.LEFT)
                if dy > 0:
                    preferred_directions.append(Direction.DOWN)
                else:
                    preferred_directions.append(Direction.UP)
            else:
                if dy > 0:
                    preferred_directions.append(Direction.DOWN)
                else:
                    preferred_directions.append(Direction.UP)
                if dx > 0:
                    preferred_directions.append(Direction.RIGHT)
                else:
                    preferred_directions.append(Direction.LEFT)
            
            # Tester les directions préférées (en évitant les collisions avec les autres ghosts et le spawn)
            for direction in preferred_directions:
                if maze.can_move(self.x, self.y, direction):
                    dx_dir, dy_dir = direction.value
                    new_cell_x = cell_x + dx_dir
                    new_cell_y = cell_y + dy_dir
                    # Éviter de revenir dans le spawn
                    if not self.is_in_spawn(new_cell_x, new_cell_y) and not self.would_collide_with_ghost(maze, direction, other_ghosts):
                        self.direction = direction
                        break
            
            # Si aucune direction préférée n'est disponible, essayer toutes les autres directions
            if not maze.can_move(self.x, self.y, self.direction) or self.would_collide_with_ghost(maze, self.direction, other_ghosts):
                for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                    if maze.can_move(self.x, self.y, direction):
                        dx_dir, dy_dir = direction.value
                        new_cell_x = cell_x + dx_dir
                        new_cell_y = cell_y + dy_dir
                        # Éviter de revenir dans le spawn
                        if not self.is_in_spawn(new_cell_x, new_cell_y) and not self.would_collide_with_ghost(maze, direction, other_ghosts):
                            self.direction = direction
                            break
        
        # Se déplacer dans la direction choisie
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

