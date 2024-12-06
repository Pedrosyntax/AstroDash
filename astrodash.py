import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the game window
width, height = 1080, 500  # Set the width and height of the game window
screen = pygame.display.set_mode((width, height))  # Create a display screen of the specified size
pygame.display.set_caption("TEST")  # Set the game window's title

# Load images (functions to load the images used in the game)
ship_image_path = r"C:\Users\appuambu\assests1\rocket.webp"
heart_image_path = r"C:\Users\appuambu\assests1\heart.webp"
background_image_path = r"C:\Users\appuambu\assests1\background.jpg"
fuel_image_path = r"C:\Users\appuambu\assests1\fuel.webp"
rocks_image_path = r"C:\Users\appuambu\assests1\rocks.webp"

# Function to load and resize images
def load_image(path, width, height):
    """Loads and resizes an image."""
    try:
        image = pygame.image.load(path)  # Load the image
        image = pygame.transform.scale(image, (width, height))  # Resize the image
        return image  # Return the resized image
    except pygame.error as e:
        print(f"Error loading image at {path}: {e}")
        sys.exit()  # Exit if the image fails to load

# Load all images into variables
ship_image = load_image(ship_image_path, 80, 50)  # Load ship image and resize it to 50x50 pixels
heart_image = load_image(heart_image_path, 30, 30)  # Load heart image (for lives) and resize it
background_image = load_image(background_image_path, width, height)  # Load background image and resize it to fit screen size
fuel_image = load_image(fuel_image_path, 30, 30)  # Load coin image
rocks_image = load_image(rocks_image_path, 50, 50)  # Load rock image (obstacle)

# Ship's initial position and movement settings
ship_x = width // 4  # Set horizontal position of the Ship (1/4 of screen width)
ship_y = height // 2  # Set vertical position of the Ship (center of the screen)
ship_speed = 5  # Speed at which the Ship moves up or down
ship_moving_up = False  # Flag to check if the Ship is moving up
ship_moving_down = False  # Flag to check if the Ship is moving down

# Lives, score, and coins
lives = 3  # Set initial lives to 3
fuel_collected = 0  # Initialize coins collected counter to 0
game_over = False  # Flag to check if the game is over (when lives run out)

# Create a list for rocks (obstacles) and coins
rocks = []
fuel = []

# Function to create a new rock
def create_rocks():
    rocks_x = random.randint(width, width + 200)  # Generate a random position for the rock
    rocks_y = random.randint(50, height - 50)  # Random height position
    rocks.append(pygame.Rect(rocks_x, rocks_y, 50, 50))  # Add the new rock to the rocks list

# Function to create a new coin
def create_fuel():
    fuel_x = random.randint(width, width + 200)  # Generate a random position for the coin
    fuel_y = random.randint(50, height - 50)  # Random height position
    fuel.append(pygame.Rect(fuel_x, fuel_y, 30, 30))  # Add the new coin to the coins list

# Main game loop
while True:
    screen.fill((0, 0, 0))  # Fill the screen with black color (background)

    # Draw the background image
    screen.blit(background_image, (0, 0))  # Blit the background image to the screen (draw it)

    # Handle events (keyboard input)
    for event in pygame.event.get():  # Loop through all events in the event queue
        if event.type == pygame.QUIT:  # If the user closes the game window
            pygame.quit()  # Quit pygame
            sys.exit()  # Exit the program

        if event.type == pygame.KEYDOWN:  # If a key is pressed down
            if event.key == pygame.K_UP:  # If the UP arrow key is pressed
                ship_moving_up = True  # Set the flag to True (move the ship up)
            if event.key == pygame.K_DOWN:  # If the DOWN arrow key is pressed
                ship_moving_down = True  # Set the flag to True (move the ship down)
            if event.key == pygame.K_r and game_over:  # If 'r' is pressed and the game is over
                # Reset the game
                lives = 3  # Reset lives to 3
                fuel_collected = 0  # Reset coins collected to 0
                ship_y = height // 2  # Reset ship's position to the center of the screen
                rocks.clear()  # Clear all rocks
                fuel.clear()  # Clear all coins
                game_over = False  # Set the game over flag to False (restart the game)

        # Detect key releases (when a key is released)
        if event.type == pygame.KEYUP:  # If a key is released
            if event.key == pygame.K_UP:  # If the UP arrow key is released
                ship_moving_up = False  # Set the flag to False (stop moving the ship up)
            if event.key == pygame.K_DOWN:  # If the DOWN arrow key is released
                ship_moving_down = False  # Set the flag to False (stop moving the ship down)

    # If the game is over, stop the ship's movement
    if not game_over:
        # Move the ship based on key states (whether keys are pressed or not)
        if ship_moving_up:  # If the UP key is pressed
            ship_y -= ship_speed  # Move the ship up by ship_speed pixels
        if ship_moving_down:  # If the DOWN key is pressed
            ship_y += ship_speed  # Move the ship down by ship_speed pixels

        # Prevent the ship from going off-screen (top or bottom)
        if ship_y < 0:  # If the ship moves above the screen
            ship_y = 0  # Set its position to the top of the screen
            lives -= 1  # Decrease lives by 1 when the ship hits the top
        if ship_y > height - ship_image.get_height():  # If the ship moves below the screen
            ship_y = height - ship_image.get_height()  # Set its position to the bottom of the screen
            lives -= 1  # Decrease lives by 1 when the ship hits the bottom

        # Create new rocks and coins at intervals
        if random.randint(1, 100) < 2:  # 2% chance to create a new rock
            create_rocks()
        if random.randint(1, 100) < 5:  # 5% chance to create a new coin
            create_fuel()

        # Update positions of rocks and coins
        for rock in rocks[:]:
            rock.x -= 5  # Move the rock to the left
            if rock.x < 0:  # If the rock moves off the screen
                rocks.remove(rock)  # Remove the rock from the list

            # Check for collision with the ship (if the ship hits the rock)
            if pygame.Rect(ship_x, ship_y, 50, 50).colliderect(rock):  # Collision detection
                lives -= 1  # Decrease lives by 1
                rocks.remove(rock)  # Remove the rock from the list after collision

        for fuel in fuel[:]:
            fuel.x -= 5  # Move the coin to the left
            if fuel.x < 0:  # If the coin moves off the screen
                fuel.remove(fuel)  # Remove the coin from the list

            # Check for collision with the ship (if the ship collects the coin)
            if pygame.Rect(ship_x, ship_y, 50, 50).colliderect(fuel):  # Collision detection
                fuel_collected += 1  # Increase the coin counter
                fuel.remove(fuel)  # Remove the coin from the list after collection

        # Game Over condition (when lives reach 0)
        if lives <= 0:
            game_over = True  # Set the game over flag to True when lives reach 0

    # Display game over screen and restart instructions
    if game_over:
        font = pygame.font.SysFont('grotesk', 60)  # Set font and size for game over text
        game_over_text = font.render("COOKED! Press 'R' to Restart", True, (255, 255, 255))  # Create text
        screen.blit(game_over_text, (width // 4, height // 2))  # Blit the text to the screen

    # Draw the ship (player's character)
    screen.blit(ship_image, (ship_x, ship_y))  # Draw the ship image at the current position

    # Draw the rocks (obstacles)
    for rock in rocks:
        screen.blit(rocks_image, rock)  # Draw each rock at its current position

    # Draw the coins
    for fuel in fuel:
        screen.blit(fuel_image, fuel)  # Draw each coin at its current position

    # Draw the remaining lives
    for i in range(lives):
        screen.blit(heart_image, (10 + 30 * i, 10))  # Draw heart icons for each remaining life

    # Draw the coins collected
    font = pygame.font.SysFont('grotesk', 30)  # Set font and size for text
    fuel_text = font.render(f"Fuel Level: {fuel_collected}", True, (255, 255, 255))  # Create text for coins
    screen.blit(fuel_text, (width - 150, 10))  # Blit the coins text to the top right

    # Update the display
    pygame.display.update()  # Update the display to show all the changes made

    # Control the game speed (frame rate)
    pygame.time.Clock().tick(60)  # Set the game to run at 60 frames per second