import os
import sys
import pygame
from pygame.locals import *
import settings
import utils
from sprites import HotAirBalloon, Cannonball, Mine

clock = pygame.time.Clock()
pygame.init()
pygame.font.init() # Initaliserer fonter

pygame.key.set_repeat(10, 10)

screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE) 
#screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)) 
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
    balloons.append(HotAirBalloon((1, 200)))

cannonballs = []
for n in range(1):
    cannonballs.append(Cannonball((100,0)))

mines = []
for n in range(10):
    mines.append(Mine((0,0)))

while True:
    pygame.event.pump()
    for event in pygame.event.get():
        # Avslutter ved Window X eller Q tast
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                for balloon in balloons:
                    balloon.burn()        
            
    surface.fill((255, 255, 255))
    surface.blit(background, (0,0))
    for mine in mines:
        mine.draw(surface)
        
    for balloon in balloons:
        balloon.draw(surface)

    for cannonball in cannonballs:
        cannonball.draw(surface)
    surface.blit(utils.debug_text('{}'.format(int(clock.get_fps()))), (0,0))

    screen.blit(surface, (0,0))
 
    pygame.display.flip()
    pygame.display.update()
    clock.tick(settings.FPS)
 