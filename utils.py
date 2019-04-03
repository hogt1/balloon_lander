import pygame
#from pygame.locals import *

def debug_text(text):
    font = pygame.font.SysFont('', 20)
    # font.render returnerer et surface
    return font.render(text, False, (0, 0, 0))


def load_image(filename, size = (100, 100)):
    ''' Returnerer en surface med det skalerte bilde
    '''
    img = pygame.image.load(filename)
    img.convert()
    # Skalerer størrelsen på bilde til det som  passer best innenfor målet
    rect =  img.get_rect().fit(pygame.Rect((0, 0), size))
    # Lager en surface med samme størrelse som ønsket bilde (Likk mikk for at den skal bli transparent)
    image = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    # Tegner skalert bilde på Surface
    image.blit(pygame.transform.smoothscale(img, rect.size), (0,0))
    return image
