import pygame  # Import the pygame module to create the game
import random  # Import random module for random number generation

# Initialize all imported Pygame modules
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600  # Dimensions of the game window
FPS = 60  # Frames per second (controls game speed)
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50  # Size of the player rectangle
BALL_RADIUS = 20  # Radius of each falling ball
MAX_BALLS = 5  # Maximum number of balls on the screen at the same time
MIN_SPEED, MAX_SPEED = 3, 8  # Minimum and maximum falling speed of the balls
WHITE = (255, 255, 255)  # RGB value for white color
RED = (255, 0, 0)  # RGB value for red color (balls)
BLUE = (0, 0, 255)  # RGB value for blue color (player)
BLACK = (0, 0, 0)  # RGB value for black color (background)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a game window
pygame.display.set_caption("Ball Dodge Game")  # Set the window title

# Font setup for displaying game over text
font = pygame.font.SysFont("Arial", 40)

# Player's initial position and movement speed
player_x = WIDTH // 2 - PLAYER_WIDTH // 2  # Center the player horizontally
player_y = HEIGHT - PLAYER_HEIGHT - 10  # Position player near bottom of the screen
player_speed = 8  # Speed at which the player moves

balls = []  # List to store ball data (position and speed)

# Function to draw the player rectangle
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, PLAYER_WIDTH, PLAYER_HEIGHT))  # Draw player as a blue rectangle

# Function to create a new falling ball with random x-position and speed
def create_ball():
    x = random.randint(0, WIDTH - BALL_RADIUS * 2)  # Random horizontal position
    y = -BALL_RADIUS * 2  # Start ball just above the top of the screen
    speed = random.randint(MIN_SPEED, MAX_SPEED)  # Random falling speed
    return [x, y, speed]  # Return as a list [x-position, y-position, speed]

# Function to draw all balls on the screen
def draw_balls(balls):
    for ball in balls:
        pygame.draw.circle(screen, RED, (ball[0], ball[1]), BALL_RADIUS)  # Draw red ball

# Function to update ball positions
def move_balls(balls):
    for ball in balls:
        ball[1] += ball[2]  # Move ball downward by its speed
        if ball[1] > HEIGHT:  # If ball goes below the screen
            balls.remove(ball)  # Remove it from the list
            balls.append(create_ball())  # Create and add a new ball

# Function to check for collision between player and any ball
def check_collision(player_rect, balls):
    for ball in balls:
        # Create a rectangle around the ball to check for collision
        ball_rect = pygame.Rect(ball[0] - BALL_RADIUS, ball[1] - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        if player_rect.colliderect(ball_rect):  # Check if player rectangle collides with ball rectangle
            return True  # Collision detected
    return False  # No collision

# Game loop control variable
running = True
clock = pygame.time.Clock()  # Clock to control frame rate

# Create initial set of balls
for _ in range(MAX_BALLS):
    balls.append(create_ball())  # Append new balls to the list

# Main game loop
while running:
    clock.tick(FPS)  # Limit the game to run at FPS frames per second

    # Handle events such as closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if quit event is triggered
            running = False  # End game loop

    # Detect key presses
    keys = pygame.key.get_pressed()

    # Move player left, ensuring it stays on screen
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    # Move player right, ensuring it stays on screen
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH:
        player_x += player_speed

    # Update positions of all balls
    move_balls(balls)

    # Create a rectangle for the player for collision detection
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Check for collision with any ball
    if check_collision(player_rect, balls):
        # Show "Game Over" text
        game_over_text = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2,
                                     HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.update()  # Update screen to show the text
        pygame.time.wait(2000)  # Pause for 2 seconds
        running = False  # Exit game loop

    # Drawing everything on the screen
    screen.fill(BLACK)  # Clear screen with black background
    draw_player(player_x, player_y)  # Draw player
    draw_balls(balls)  # Draw all balls

    pygame.display.update()  # Refresh display with the new drawings

# Exit Pygame
pygame.quit()
