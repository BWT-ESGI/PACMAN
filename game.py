import pygame
import sys
from constants import (
    CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE, DARK_BLUE, RED, PINK, CYAN, ORANGE,
    MAZE_LAYOUT, MAZE_LAYOUT_ORIGINAL, Direction,
    SCORE_DOT, SCORE_POWER_PELLET, INITIAL_LIVES, COLLISION_THRESHOLD, FPS,
    PACMAN_START_X, PACMAN_START_Y,
    GHOST_START_X, GHOST_START_Y,
    GHOST2_START_X, GHOST2_START_Y,
    GHOST3_START_X, GHOST3_START_Y,
    GHOST4_START_X, GHOST4_START_Y,
    UI_HEIGHT, FONT_SIZE, DOT_RADIUS, POWER_PELLET_RADIUS
)
from pacman import PacMan
from ghost import Ghost
from agent import PacManAgent
from maze import Maze

class Game:
    def __init__(self, use_agent=False):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        
        self.maze = Maze(MAZE_LAYOUT)
        
        # Initialisation des objets du jeu
        self.pacman = PacMan(PACMAN_START_X, PACMAN_START_Y)
        self.ghosts = [
            Ghost(GHOST_START_X, GHOST_START_Y, RED),
            Ghost(GHOST2_START_X, GHOST2_START_Y, PINK),
            Ghost(GHOST3_START_X, GHOST3_START_Y, CYAN),
            Ghost(GHOST4_START_X, GHOST4_START_Y, ORANGE)
        ]
        
        # Agent optionnel
        self.agent = PacManAgent(self.pacman, self.maze)
        if use_agent:
            self.agent.enable()
        
        # État du jeu
        self.score = 0
        self.lives = INITIAL_LIVES
        self.dots_eaten = 0
        self.total_dots = 0
        
        self.total_dots = self.maze.count_dots()
        
        self.running = True
        self.game_over = False
        self.collision_cooldown = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if not self.agent.enabled:  # Contrôles manuels seulement si agent désactivé
                    if event.key == pygame.K_UP:
                        self.pacman.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.set_direction(Direction.RIGHT)
                
                # Touche pour activer/désactiver l'agent
                if event.key == pygame.K_a:
                    if self.agent.enabled:
                        self.agent.disable()
                        print("Agent désactivé - Contrôles manuels")
                    else:
                        self.agent.enable()
                        print("Agent activé - Contrôle automatique")
                
                # Redémarrer le jeu
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
    
    def update(self):
        if not self.game_over:
            # Mise à jour de l'agent si activé
            if self.agent.enabled:
                self.agent.update()
            
            # Mise à jour de Pac-Man
            self.pacman.update(self.maze)
            
            pacman_cell_x = int(self.pacman.x)
            pacman_cell_y = int(self.pacman.y)
            
            if 0 <= pacman_cell_x < MAZE_WIDTH and 0 <= pacman_cell_y < MAZE_HEIGHT:
                eaten = self.maze.eat_dot(pacman_cell_x, pacman_cell_y)
                if eaten == '.':
                    self.score += SCORE_DOT
                    self.dots_eaten += 1
                elif eaten == 'o':
                    self.score += SCORE_POWER_PELLET
                    self.dots_eaten += 1
            
            # Mise à jour des fantômes
            for ghost in self.ghosts:
                ghost.update(self.maze, self.pacman)
            
            # Vérifier les collisions avec les fantômes
            if self.collision_cooldown <= 0:
                for ghost in self.ghosts:
                    if (abs(self.pacman.x - ghost.x) < COLLISION_THRESHOLD and 
                        abs(self.pacman.y - ghost.y) < COLLISION_THRESHOLD):
                        self.lives -= 1
                        self.collision_cooldown = 60  # 1 seconde de cooldown (60 frames)
                        if self.lives <= 0:
                            self.game_over = True
                        else:
                            # Repositionner seulement si on a encore des vies
                            self.pacman.x = PACMAN_START_X
                            self.pacman.y = PACMAN_START_Y
                            self.pacman.direction = Direction.RIGHT
                            self.pacman.next_direction = Direction.RIGHT
                        break
            else:
                self.collision_cooldown -= 1
            
            # Vérifier la victoire
            if self.dots_eaten >= self.total_dots:
                self.game_over = True
    
    def draw_maze(self):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                cell = self.maze.get_cell(x, y)
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell == '#':
                    pygame.draw.rect(self.screen, DARK_BLUE, rect)
                elif cell == '.':
                    pygame.draw.circle(self.screen, WHITE, 
                                    (x * CELL_SIZE + CELL_SIZE // 2,
                                     y * CELL_SIZE + CELL_SIZE // 2), DOT_RADIUS)
                elif cell == 'o':
                    pygame.draw.circle(self.screen, WHITE, 
                                    (x * CELL_SIZE + CELL_SIZE // 2,
                                     y * CELL_SIZE + CELL_SIZE // 2), POWER_PELLET_RADIUS)
    
    def draw_ui(self):
        ui_rect = pygame.Rect(0, MAZE_HEIGHT * CELL_SIZE, WINDOW_WIDTH, UI_HEIGHT)
        pygame.draw.rect(self.screen, BLACK, ui_rect)
        
        font = pygame.font.Font(None, FONT_SIZE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, MAZE_HEIGHT * CELL_SIZE + 10))
        
        # Vies
        lives_text = font.render(f"Vies: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, MAZE_HEIGHT * CELL_SIZE + 35))
        
        # État de l'agent
        agent_status = "Agent: ON" if self.agent.enabled else "Agent: OFF"
        agent_text = font.render(agent_status, True, WHITE)
        self.screen.blit(agent_text, (200, MAZE_HEIGHT * CELL_SIZE + 10))
        
        # Instructions
        if self.game_over:
            if self.dots_eaten >= self.total_dots:
                game_over_text = font.render("VICTOIRE! Appuyez sur R pour recommencer", True, WHITE)
            else:
                game_over_text = font.render("GAME OVER! Appuyez sur R pour recommencer", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, MAZE_HEIGHT * CELL_SIZE + 25))
            self.screen.blit(game_over_text, text_rect)
        else:
            if self.agent.enabled:
                instructions_text = font.render("Agent actif - Appuyez sur A pour désactiver", True, WHITE)
            else:
                instructions_text = font.render("Flèches: Jouer | A: Activer agent | R: Recommencer", True, WHITE)
            text_rect = instructions_text.get_rect(center=(WINDOW_WIDTH // 2, MAZE_HEIGHT * CELL_SIZE + 25))
            self.screen.blit(instructions_text, text_rect)
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_maze()
        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        self.draw_ui()
        pygame.display.flip()
    
    def restart_game(self):
        self.pacman = PacMan(PACMAN_START_X, PACMAN_START_Y)
        self.ghosts = [
            Ghost(GHOST_START_X, GHOST_START_Y, RED),
            Ghost(GHOST2_START_X, GHOST2_START_Y, PINK),
            Ghost(GHOST3_START_X, GHOST3_START_Y, CYAN),
            Ghost(GHOST4_START_X, GHOST4_START_Y, ORANGE)
        ]
        self.score = 0
        self.lives = INITIAL_LIVES
        self.dots_eaten = 0
        self.game_over = False
        self.collision_cooldown = 0
        
        self.maze.reset(MAZE_LAYOUT_ORIGINAL)
        
        # Réinitialiser l'agent
        self.agent = PacManAgent(self.pacman, self.maze)
        if self.agent.enabled:
            self.agent.enable()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

