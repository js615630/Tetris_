
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
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.SHAPES) - 1)
        self.color = random.randint(1, len(Tetromino.COLORS) - 1)
        self.rotation = 0

    def image(self):
        return self.SHAPES[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.SHAPES[self.type])

class Tetris:
    level = 2
    score = 0
    state = "start"
    height = 20
    width = 10
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0 for _ in range(width)] for _ in range(height)]
        self.score = 0
        self.state = "start"
        self.new_figure()
        self.running = True  # Define running as a class variable

    def new_figure(self):
        self.figure = Tetromino(5, 0)

    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y >= self.height or \
                       j + self.figure.x >= self.width or \
                       j + self.figure.x < 0 or \
                       self.field[i + self.figure.y][j + self.figure.x]:
                        return True
        return False

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.clear_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def clear_lines(self):
        lines = 0
        for i in range(1, self.height):
            if 0 not in self.field[i]:
                lines += 1
                del self.field[i]
                self.field.insert(0, [0 for _ in range(self.width)])
        self.score += lines ** 2

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def move_piece(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_piece(-1)
                elif event.key == pygame.K_RIGHT:
                    self.move_piece(1)
                elif event.key == pygame.K_DOWN:
                    self.go_down()
                elif event.key == pygame.K_UP:
                    self.rotate()

# Continue from the previous code snippet

    def draw(self, screen):
        # Fill the background
        screen.fill((0, 0, 0))

        # Draw the grid
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255), [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom], 1)
                if self.field[i][j]:
                    pygame.draw.rect(screen, Tetromino.COLORS[self.field[i][j]],
                                     [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2, self.zoom - 2])

        # Draw the current tetromino
        if self.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.figure.image():
                        pygame.draw.rect(screen, Tetromino.COLORS[self.figure.color],
                                         [self.x + self.zoom * (j + self.figure.x) + 1,
                                          self.y + self.zoom * (i + self.figure.y) + 1,
                                          self.zoom - 2, self.zoom - 2])

# Game initialization
size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 5
game = Tetris(20, 10)

while game.running:
    game.handle_events()  # This will set game.running to False when the quit event is detected
    if game.state == "start":
        game.go_down()

    game.draw(screen)
    pygame.display.flip()
    clock.tick(fps)