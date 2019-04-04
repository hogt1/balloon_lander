import os
import sys
import pygame
from pygame.locals import *
import settings
import utils
from sprites import HotAirBalloon, Cannonball, Mine


os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
clock = pygame.time.Clock()
pygame.font.init() # Initaliserer fonter

pygame.key.set_repeat(10, 10)

#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.DOUBLEBUF) 
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)) 
surface = pygame.Surface(screen.get_size())
surface.convert()

bg_img = pygame.image.load(os.path.join(settings.ASSETS_DIR, settings.BACKGROUND_FILE))
bg_img.convert()
# Lager en surface med samme størrelse som ønsket bilde (Likk mikk for at den skal bli transparent)
background = pygame.Surface(surface.get_rect().size, pygame.SRCALPHA, 32)
# Tegner skalert bilde på Surface
background.blit(pygame.transform.smoothscale(bg_img, surface.get_rect().size), (0,0))



balloon = pygame.sprite.GroupSingle()
balloon.add(HotAirBalloon((1, 200)))

#cannonballs = []
#for n in range(1):
#    cannonballs.append(Cannonball((100,0)))

mines = pygame.sprite.Group()

def add_mine():
    mine = Mine((0,0))
    if not pygame.sprite.spritecollideany(mine, mines):
        mines.add(mine)
    else:
        add_mine()


for n in range(10):
    add_mine()

def display_points(points):
    font = pygame.font.SysFont('', 20)
    # font.render returnerer et surface
    ts = font.render(f'{points}', False, (0, 0, 0))
    surface.blit(ts, (surface.get_rect().right-ts.get_rect().width-10, 10))


def game_over():
    for n in range(6):
        surface.fill((255, 0, 0))
        screen.blit(surface, (0,0))
        pygame.display.flip()
        pygame.display.update()
        pygame.time.wait(200)

        surface.fill((255, 255, 255))
        screen.blit(surface, (0,0))
        pygame.display.flip()
        pygame.display.update()
        pygame.time.wait(200)
            
        pygame.quit()
        sys.exit()




while True:
    pygame.event.pump()
    for event in pygame.event.get():
        # Avslutter ved Window X eller Q tast
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                balloon.sprite.burn() 

    if balloon.sprite.level_up:
        add_mine()
                
    surface.blit(background, (0,0))
    mines.update()
    mines.draw(surface)
    balloon.update()
    balloon.draw(surface)

    surface.blit(utils.debug_text('{}'.format(int(clock.get_fps()))), (0,0))
    display_points(int(balloon.sprite.points))

    screen.blit(surface, (0,0))
 
    pygame.display.flip()
    pygame.display.update()
    clock.tick(settings.FPS)
    # Sjekker om vi traff topp eller bunn av skjermen
    if balloon.sprite.hit:
        game_over()
    
    # Sjekker om det er noen rect for sprite som overlapper
    mine_hit = pygame.sprite.spritecollideany(balloon.sprite, mines)
    if mine_hit:
        # Sjekker om de overlapper på pixelnivå
        ballon_mask = pygame.mask.from_surface(balloon.sprite.image)
        mine_mask = pygame.mask.from_surface(mine_hit.image)
        offset_x = mine_hit.rect.left - balloon.sprite.rect.left
        offset_y = mine_hit.rect.top - balloon.sprite.rect.top
        overlap = ballon_mask.overlap(mine_mask, (offset_x, offset_y))
        #print(overlap)
        if overlap:
            game_over()
