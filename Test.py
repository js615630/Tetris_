
import pygame
import random
import json

# Initialize pygame
pygame.init()

def read_high_score():
    try:
        with open('high_score.json', 'r') as f:
            data = json.load(f)
            return data.get('high_score', 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def write_high_score(score):
    with open('high_score.json', 'w') as f:
        json.dump({'high_score': score}, f)


class Tetromino:
    COLORS = [
        (0, 255, 255),  # Cyan I
        (255, 165, 0),  # Orange L
        (0, 0, 255),  # Blue J
        (255, 255, 0),  # Yellow O
        (0, 255, 0),  # Green S
        (255, 0, 0),  # Red Z
        (128, 0, 128),  # Purple T
        (255, 255, 255)  # White for flashing
    ]

    SHAPES = [
        # I Tetromino
        [[4, 5, 6, 7], [2, 6, 10, 14], [8, 9, 10, 11], [1, 5, 9, 13]],
        # O Tetromino
        [[4, 5, 8, 9], [4, 5, 8, 9], [4, 5, 8, 9], [4, 5, 8, 9]],
        # L Tetromino
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]],
        # J Tetromino
        [[0, 4, 5, 6], [1, 5, 9, 10], [4, 5, 6, 10], [0, 1, 5, 9]],
        # S Tetromino
        [[6, 7, 9, 10], [1, 5, 6, 10], [6, 7, 9, 10], [1, 5, 6, 10]],
        # Z Tetromino
        [[4, 5, 9, 10], [2, 6, 5, 9], [4, 5, 9, 10], [2, 6, 5, 9]],
        # T Tetromino
        [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],
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
        self.lines_to_clear = []
        self.high_score = read_high_score()
        self.next_round_score = 10  # Points needed to win the current round
        self.total_rounds_won = 0  # Keep track of how many rounds have been won
        self.initial_speed = 2  # Starting speed, adjust as necessary
        self.speed_increase = 1  # Speed increase per round
        self.current_speed = self.initial_speed  # Current speed of falling pieces
        # Initialize the game
        self.start_new_round()

    def start_new_round(self):
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.new_figure()
        self.state = "start"
        # Increase speed for each new round
        self.current_speed += self.speed_increase  # Increase the speed for the next round

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
        if self.score > self.high_score:
            self.high_score = self.score
            write_high_score(self.high_score)
        if self.score >= self.next_round_score:
            self.total_rounds_won += 1  # Increment the round won counter
            self.next_round_score += 15  # Update the score target for the next round
            self.start_new_round()  # Start a new round


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
                elif event.key == pygame.K_r:  # Reset the game when 'R' is pressed
                    self.reset_game()

    def clear_lines(self):
        self.lines_to_clear = [i for i in range(1, self.height) if 0 not in self.field[i]]
        if self.lines_to_clear:
            for _ in range(4):  # Flash 4 times
                pygame.time.delay(100)  # Flashing delay
                self.draw(screen, flash=True)
                pygame.display.flip()
                pygame.time.delay(100)
            for i in self.lines_to_clear:
                del self.field[i]
                self.field.insert(0, [0 for _ in range(self.width)])
            self.score += len(self.lines_to_clear) ** 2
            self.lines_to_clear = []  # Reset the lines to clear

    def draw(self, screen, flash=False):
        # Fill the background
        screen.fill((0, 0, 0))

        # Draw the grid
        for i in range(self.height):
            for j in range(self.width):
                # Flash effect for lines to clear
                if flash and i in self.lines_to_clear:
                    flash_color = (255, 255, 255)  # White for flashing
                    pygame.draw.rect(screen, flash_color,
                                     [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2,
                                      self.zoom - 2])
                else:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom], 1)
                    if self.field[i][j] > 0:
                        pygame.draw.rect(screen, Tetromino.COLORS[self.field[i][j]],
                                         [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2,
                                          self.zoom - 2])

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

            # Display the current score
            font = pygame.font.SysFont('comicsans', 30, True)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            screen.blit(score_text, (self.x + self.width * self.zoom + 10, 20))

            # Display the high score
            high_score_text = font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
            screen.blit(high_score_text, (self.x + self.width * self.zoom + 10, 50))

        # Draw Game Over text when the game state is "gameover"
        if self.state == "gameover":
            game_over_text = font.render('GAME OVER', 1, (255, 0, 0))
            screen.blit(game_over_text, (self.x + 20, self.y + self.height * self.zoom / 2 - 20))

    def reset_game(self):
        self.field = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0  # Reset score
        self.state = "start"
        self.new_figure()
        self.lines_to_clear = []
        self.next_round_score = 10  # Reset the target score for winning the round
        self.total_rounds_won = 0  # Reset the total rounds won
        self.current_speed = self.initial_speed  # Reset to the original speed
        self.running = True  # Keep the game running


# Game initialization
size = (800, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 3
game = Tetris(20, 10)

while game.running:
    game.handle_events()  # This will set game.running to False when the quit event is detected
    if game.state == "start":
        game.go_down()

    game.draw(screen)
    pygame.display.flip()
    clock.tick(game.current_speed)