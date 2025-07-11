import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600                     # Screen dimensions
FPS = 60                                     # Frames per second
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20        # Paddle size
BALL_RADIUS = 10                             # Ball size
BLOCK_WIDTH, BLOCK_HEIGHT = 70, 20           # Block size
BLOCK_COLOR = (255, 255, 0)                  # Block color (yellow)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_COLOR = (0, 0, 255)                   # Paddle color (blue)
BALL_COLOR = (255, 0, 0)                     # Ball color (red)

# Set up the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Breaker")

# Font for displaying score and game over message
font = pygame.font.SysFont("Arial", 30)

# Paddle initial position and speed
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10
paddle_speed = 10

# Ball initial position and direction
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4 * random.choice([1, -1])     # Horizontal direction: random left or right
ball_dy = -4                             # Vertical direction: upwards
score = 0                                # Initial score

# Create blocks and store them in a list
blocks = []
for i in range(7):
    for j in range(4):
        block_x = i * (BLOCK_WIDTH + 10) + 60
        block_y = j * (BLOCK_HEIGHT + 5) + 60
        blocks.append(pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT))

# Function to draw the paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, PADDLE_COLOR, pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the ball
def draw_ball(x, y):
    pygame.draw.circle(screen, BALL_COLOR, (x, y), BALL_RADIUS)

# Function to draw the blocks
def draw_blocks():
    for block in blocks:
        pygame.draw.rect(screen, BLOCK_COLOR, block)

# Function to check collision of ball with blocks
def check_collision_with_blocks(ball_rect):
    global score
    for block in blocks[:]:
        if ball_rect.colliderect(block):
            blocks.remove(block)        # Remove block if hit
            score += 10                 # Increase score
            return True
    return False

# Main Game Loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)     # Limit game to FPS

    # Event handling (e.g. quit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with window edges
    if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
        ball_dx = -ball_dx
    if ball_y <= BALL_RADIUS:
        ball_dy = -ball_dy
    if ball_y >= HEIGHT - BALL_RADIUS:
        # Game Over when ball touches bottom
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2,
                                     HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

    # Ball collision with paddle
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    if paddle_rect.colliderect(pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)):
        ball_dy = -ball_dy

    # Ball collision with blocks
    ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    check_collision_with_blocks(ball_rect)

    # Drawing
    screen.fill(BLACK)                        # Clear screen
    draw_paddle(paddle_x, paddle_y)           # Draw paddle
    draw_ball(ball_x, ball_y)                 # Draw ball
    draw_blocks()                             # Draw blocks

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()                   # Update screen

# Quit the game
pygame.quit()
