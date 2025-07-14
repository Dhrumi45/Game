# Import required modules
import pygame  # Main library used for game development
import sys     # Used to handle system-level operations like quitting the game
import random  # Provides random number generation (used for ball direction)
import time    # Used for time delays (e.g., show messages)

# Initialize pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 600, 600  # Screen size
WHITE = (255, 255, 255)   # Background color
BALL_COLOR = (255, 0, 0)  # Red color for the ball
PADDLE_COLOR = (0, 0, 255)  # Blue color for the paddle

# Brick colors for different rows
BRICK_COLORS = [
    (255, 0, 0),      # Red
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 128, 0),      # Green
    (0, 0, 255)       # Blue
]

# Game settings
BRICK_WIDTH = 80           # Width of each brick
BRICK_HEIGHT = 20          # Height of each brick
BRICK_ROWS = 5             # Number of rows of bricks
BRICK_COLUMNS = 8          # Number of columns of bricks
BRICK_SPACING = 10         # Space between bricks
PADDLE_WIDTH = 100         # Paddle width
PADDLE_HEIGHT = 10         # Paddle height
BALL_RADIUS = 10           # Ball radius
BALL_SPEED = 5             # Initial speed of the ball
PADDLE_SPEED = 10          # Paddle movement speed
LIVES = 3                  # Total lives player starts with

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create game window
pygame.display.set_caption("Brick Breaker")         # Set window title
clock = pygame.time.Clock()                         # Clock to control game FPS

# Function to create a list of brick rectangles
def create_bricks():
    brick_list = []  # Empty list to hold bricks
    for row in range(BRICK_ROWS):  # Loop through each row
        for col in range(BRICK_COLUMNS):  # Loop through each column
            brick_x = col * (BRICK_WIDTH + BRICK_SPACING)  # Calculate x-position
            brick_y = row * (BRICK_HEIGHT + BRICK_SPACING) + 50  # y-position with offset
            rect = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)  # Create brick rectangle
            brick_list.append((rect, BRICK_COLORS[row]))  # Store brick and its color
    return brick_list  # Return list of bricks

# Function to draw all bricks on the screen
def draw_bricks(bricks):
    for brick, color in bricks:  # Loop through all bricks
        pygame.draw.rect(screen, color, brick)  # Draw each brick with its color

# Function to show a centered message with optional score
def show_centered_message(message, score=None, duration=3):
    screen.fill(WHITE)  # Fill screen with white
    font_main = pygame.font.Font(None, 48)  # Main font for the message
    text_surface = font_main.render(message, True, (0, 0, 0))  # Render the message text
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))  # Center the message
    screen.blit(text_surface, text_rect)  # Display the message

    # If score is provided, show it below the message
    if score is not None:
        font_score = pygame.font.Font(None, 36)
        score_surface = font_score.render(f"Your Score: {score}", True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        screen.blit(score_surface, score_rect)

    pygame.display.flip()  # Update the screen
    time.sleep(duration)   # Wait before continuing

# Main function that runs the game loop
def run_game():
    # Initial ball position at center
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    current_ball_speed = BALL_SPEED  # Current speed (can increase)
    # Random horizontal direction; vertical goes upward
    ball_dx = random.choice([-1, 1]) * current_ball_speed
    ball_dy = -current_ball_speed

    # Set initial paddle position
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    paddle_y = HEIGHT - PADDLE_HEIGHT - 10  # Near the bottom

    bricks = create_bricks()  # Generate the bricks
    lives = LIVES  # Set initial lives
    score = 0      # Start score at 0

    # Show start screen
    show_centered_message("Start", duration=3)

    while True:  # Main game loop
        for event in pygame.event.get():  # Event loop
            if event.type == pygame.QUIT:  # Quit event
                pygame.quit()
                sys.exit()

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= PADDLE_SPEED  # Move paddle left
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += PADDLE_SPEED  # Move paddle right

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Wall collision (left/right)
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
            ball_dx *= -1  # Reverse x-direction

        # Top wall collision
        if ball_y - BALL_RADIUS <= 0:
            ball_dy *= -1  # Reverse y-direction

        # Create rectangles for paddle and ball for collision detection
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

        # Paddle collision
        if ball_rect.colliderect(paddle_rect):
            ball_dy *= -1  # Reverse ball y-direction

        # Brick collision
        for brick, color in bricks[:]:  # Iterate over a copy of the brick list
            if ball_rect.colliderect(brick):  # Collision detected
                bricks.remove((brick, color))  # Remove the brick
                ball_dy *= -1  # Reverse y-direction
                score += 10  # Increase score
                current_ball_speed += 0.1  # Slightly increase speed
                # Normalize speed direction with updated speed
                ball_dx = (ball_dx / abs(ball_dx)) * current_ball_speed
                ball_dy = (ball_dy / abs(ball_dy)) * current_ball_speed
                break  # Only one brick should be removed per frame

        # Win condition: all bricks removed
        if score >= 350:
            show_centered_message("You Win!", score)
            pygame.quit()
            sys.exit()

        # If ball goes below screen (missed paddle)
        if ball_y > HEIGHT:
            lives -= 1  # Decrease lives
            if lives == 0:  # Game over condition
                show_centered_message("Game Over!", score)
                pygame.quit()
                sys.exit()
            else:
                # Reset ball position and speed
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                current_ball_speed = BALL_SPEED
                ball_dx = random.choice([-1, 1]) * current_ball_speed
                ball_dy = -current_ball_speed

        # Drawing section
        screen.fill(WHITE)  # Clear screen
        pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)  # Draw ball
        pygame.draw.rect(screen, PADDLE_COLOR, paddle_rect)  # Draw paddle
        draw_bricks(bricks)  # Draw all bricks

        # Display score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {lives}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))

        pygame.display.flip()  # Update display
        clock.tick(60)  # Maintain 60 FPS

# Entry point of the script
def main():
    run_game()  # Start the game

# Run the game only if this file is executed directly
if __name__ == "__main__":
    main()
