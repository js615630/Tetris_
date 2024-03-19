import pygame
import random

# Initialize pygame
pygame.init()

class Tetromino:
    COLORS = [
        (0, 255, 255),  # Cyan I
        (255, 165, 0),  # Orange L
        (0, 0, 255),    # Blue J
        (255, 255, 0),  # Yellow O
        (0, 255, 0),    # Green S
        (255, 0, 0),    # Red Z
        (128, 0, 128)   # Purple T
    ]
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 0, 0], [1, 1, 1]],  # L
        [[0, 0, 1], [1, 1, 1]],  # J
        [[1, 1], [1, 1]],  # O
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1, 0], [0, 1, 1]],  # Z
        [[0, 1, 0], [1, 1, 1]]   # T
    ]

    def __init__(self, x, y):
        self.type = random.randint(0, len(self.SHAPES) - 1)
        self.shape = self.SHAPES[self.type]
        self.color = self.COLORS[self.type]
        self.x = x
        self.y = y

    def rotate(self):
        self.shape = [ [ self.shape[y][x] for y in range(len(self.shape)) ] for x in range(len(self.shape[0]) - 1, -1, -1) ]

class Tetris:
    SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
    GRID_WIDTH, GRID_HEIGHT = 10, 20
    BLOCK_SIZE = 30

    def __init__(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = [[(0,0,0) for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = Tetromino(5, 0)
        self.next_piece = Tetromino(5, 0)
        self.fall_time = 0
        self.fall_speed = 0.3

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.handle_events()
            self.draw_grid()
            self.draw_tetromino(self.current_piece)
            self.update()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_piece.x -= 1
                if event.key == pygame.K_RIGHT:
                    self.current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    self.current_piece.y += 1
                if event.key == pygame.K_UP:
                    self.current_piece.rotate()

    def draw_grid(self):
        for i, row in enumerate(self.grid):
            for j, color in enumerate(row):
                pygame.draw.rect(self.screen, color, (j*self.BLOCK_SIZE, i*self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE), 0)

    def draw_tetromino(self, piece):
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, piece.color, ((piece.x + j)*self.BLOCK_SIZE, (piece.y + i)*self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE), 0)

    def update(self):
        # Update game logic (movement, collision detection, etc.)
        pass

if __name__ == "__main__":
    game = Tetris()
    game.run()

