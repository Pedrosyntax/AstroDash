import pygame
import sys
import random
import time
import requests
from io import BytesIO

pygame.init()

width, height = 1200, 980
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AstroDash")

CHOP = r"C:\Users\Pedro\Desktop\fonts\Chopsic.otf"
try:
    chopsic_font = pygame.font.Font(CHOP, 30)
except FileNotFoundError:
    print(f"Error: Could not load font at {CHOP}")
    pygame.quit()
    sys.exit()

def load_image(url, width, height):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = pygame.image.load(BytesIO(response.content))
        image = pygame.transform.scale(image, (width, height)) 
        return image
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")
    except pygame.error as e:
        print(f"error loading image: {e}")
    return None
    
ship_image = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/pship.png?raw=true", 120, 120)
ship_powered_image = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/pship2.png?raw=true", 120, 120)
heart_image = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/heart.png?raw=true", 60, 60)
heart_gray = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/lifegrey.png?raw=true", 60, 60)
background_image_loop = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/space2.png?raw=true", 1200, 1000)
fuel_image = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/fuel.png?raw=true", 70, 70)
rocks_image = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/rocks.png?raw=true", 70, 70)
start_screen_image = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/start.jpg?raw=true", width, 1000)
lost_screen_image = load_image("https://github.com/Pedrosyntax/AstroDash/blob/main/lost.png?raw=true", width, 1000)

if not all ([ship_image, ship_powered_image, heart_image, heart_gray, background_image_loop, fuel_image, rocks_image, start_screen_image, lost_screen_image]):
    print("Error: One or more images failed to load.")
    pygame.quit()
    sys.exit()

#ship variables
ship_x = width // 1.25
ship_y = height // 1.25 
ship_speed = 4
boosted_speed = 8
ship_moving_left = False
ship_moving_right = False
is_boost_active = False
boost_start_time = None 
boost_duration = 5

# Game variables
ship_x = width // 1.25
ship_y = height // 1.25
ship_speed = 4
boosted_speed = 8
is_boost_active = False
boost_start_time = None
boost_duration = 5
lives = 3
fuel_percentage = 100
game_over = False
rocks = []
fuel = []
game_speed = 4
score = 0
last_score_update = time.time()
bg_scroll_y = 0

def create_rocks():
    rocks_x = random.randint(50, width - 50)
    rocks_y = random.randint(-200, -50)
    rocks.append(pygame.Rect(rocks_x, rocks_y, 50, 50))

def create_fuel():
    fuel_x = random.randint(50, width - 50)
    fuel_y = random.randint(-200, -50)
    fuel.append(pygame.Rect(fuel_x, fuel_y, 30, 30))

def display_lives():
    lives_text = chopsic_font.render("Lives:", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    for i in range(3):  # Maximum of 3 lives
        x_position = 120 + (i * 60)  # Start after "Lives:" text
        if i < lives:
            screen.blit(heart_image, (x_position, 2.5))
        else:
            screen.blit(heart_gray, (x_position, 2.5))
            
def start_screen():
    while True:
        screen.blit(start_screen_image, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

# Game over screen
def game_over_screen():
    while True:
        screen.blit(lost_screen_image, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main game loop
while True:
    start_screen()
    ship_x, ship_y = width // 1.25, height // 1.25
    lives, fuel_percentage, score = 3, 100, 0
    rocks, fuel = [], []
    game_over = False
    low_fuel_warning = False
    is_boost_active = False
    bg_scroll_y = 0
    last_score_update = time.time()

    while not game_over:
        screen.fill((107, 107, 107))
        bg_scroll_y += game_speed
        if bg_scroll_y >= height:
            bg_scroll_y = 0
        screen.blit(background_image_loop, (0, bg_scroll_y - height))
        screen.blit(background_image_loop, (0, bg_scroll_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship_moving_left = True
                if event.key == pygame.K_RIGHT:
                    ship_moving_right = True
                if event.key == pygame.K_UP and not is_boost_active:
                    is_boost_active = True
                    boost_start_time = time.time()
                    game_speed = boosted_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    ship_moving_left = False
                if event.key == pygame.K_RIGHT:
                    ship_moving_right = False

        if is_boost_active:
            remaining_time = boost_duration - (time.time() - boost_start_time)
            if remaining_time <= 0:
                is_boost_active = False
                game_speed = 4
            else:
                countdown_text = chopsic_font.render(f"Boost: {int(remaining_time)}", True, (255, 0, 0))
                screen.blit(countdown_text, (10, 130))

        
        if fuel_percentage > 0:
            if ship_moving_left:
                ship_x -= ship_speed
            if ship_moving_right:
                ship_x += ship_speed
        else:
            ship_y += game_speed // 2

            if ship_y > height:
                game_over_screen()
        
        ship_x = max(0, min(width - ship_image.get_width(), ship_x))
        if random.randint(1, 100) < 5.5:
            create_rocks()
        if random.randint(1, 100) < 2:
            create_fuel()

        for rock in rocks[:]:
            rock.y += game_speed
            if rock.y > height:
                rocks.remove(rock)
            if pygame.Rect(ship_x, ship_y, 50, 80).colliderect(rock):
                lives -= 1
                rocks.remove(rock)
        
        for f in fuel[:]:
            f.y += game_speed
            if f.y > height:
                fuel.remove(f)
            if pygame.Rect(ship_x, ship_y, 50, 80).colliderect(f):
                fuel_percentage = min(100, fuel_percentage + 20)
                fuel.remove(f)
        fuel_percentage -= 0.04
        if fuel_percentage <= 0:
            fuel_percentage = 0

        current_ship_image = ship_powered_image if is_boost_active else ship_image
        screen.blit(current_ship_image, (ship_x, ship_y))
        for rock in rocks:
            screen.blit(rocks_image, rock)
        for f in fuel:
            screen.blit(fuel_image, f)

        display_lives()

        if time.time() - last_score_update >= 1.5:
            score  += 2
            last_score_update = time.time()

        fuel_colour= (255, 0, 0) if fuel_percentage <= 20 else (255, 255, 255)
        score_text = chopsic_font.render(f"Score: {score}", True, (255, 255, 255))
        fuel_text = chopsic_font.render(f"Fuel: {int(fuel_percentage)}%", True, fuel_colour)
        screen.blit(score_text, (10, 90))
        screen.blit(fuel_text, (10, 50))

        if lives <= 0:
            game_over_screen()

        pygame.display.update()
        pygame.time.Clock().tick(60)
    