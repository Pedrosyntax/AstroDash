
import pygame
import sys
import random
import time

pygame.init()  # --> necessary before using nay functionality

width, height = 1200, 980  # --> size of the window 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AstroDash")

ship = pygame.image.load("AstroDash\images\pship.png")
ship_x, ship_y = 300,200

ship = pygame.transform.scale(ship, (100, 100)) #size

running = True
while running:
    for event in pygame.event.get(): # keyboard presses, closing window, mouse clicks
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    screen.blit(ship,(ship_x, ship_y))
    pygame.display.update()
pygame.quit()



