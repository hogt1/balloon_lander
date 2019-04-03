import os
import sys
import pygame
from pygame.locals import *
import settings
from sprites import HotAirBalloon, Cannonball, Mine

pygame.init()
pygame.font.init() # Initaliserer fonter


#screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE) 
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)) 
surface = pygame.Surface(screen.get_size())
surface.convert()

bg_img = pygame.image.load(os.path.join(settings.ASSETS_DIR, settings.BACKGROUND_FILE))
bg_img.convert()
# Lager en surface med samme størrelse som ønsket bilde (Likk mikk for at den skal bli transparent)
background = pygame.Surface(surface.get_rect().size, pygame.SRCALPHA, 32)
# Tegner skalert bilde på Surface
background.blit(pygame.transform.smoothscale(bg_img, surface.get_rect().size), (0,0))



balloons = []
for n in range(1):
    balloons.append(HotAirBalloon(surface))

cannonballs = []
for n in range(1):
    cannonballs.append(Cannonball(surface))

mines = []
for n in range(10):
    mines.append(Mine(surface))

while True:
    pygame.event.pump()
    for event in pygame.event.get():
        # Avslutter ved Window X eller Q tast
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            elif event.key == K_UP:
                for balloon in balloons:
                    balloon.burn()        
            
    surface.fill((255, 255, 255))
    surface.blit(background, (0,0))
    for mine in mines:
        mine.draw()
        
    for balloon in balloons:
        balloon.draw()

    for cannonball in cannonballs:
        cannonball.draw()

    screen.blit(surface, (0,0))
    pygame.display.flip()
    pygame.display.update()