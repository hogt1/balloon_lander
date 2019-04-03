import os
import sys
import random
import pygame
import math
from pygame.locals import *
import settings
import utils

class BaseObject(pygame.sprite.Sprite):
    def __init__(self, direction, speed):
        self.direction = direction
        self.speed = speed
        pygame.sprite.Sprite.__init__(self)
    
    def direction_xy(self):
        # Python operere med radianer og ikke grader
        rad = math.radians(self.direction)

        # Regner ut x og y komponenten fra vektoren "speed*direction"
        x = math.cos(rad) * self.speed
        y = math.sin(rad) * self.speed + settings.GRAVITY
        return x, y
    
    def set_direction_xy(x, y):
        # Kalkulerer direction ut i fra x og y. atan2 håndterer fortegn
        rad = math.atan2(y/self.speed, x/self.speed) # Vinkel i radianer
        self.direction = math.degrees(rad) # Kalkulerer om radianer til grader



class HotAirBalloon(BaseObject):
    def __init__(self, position, direction=0, speed=1):
        BaseObject.__init__(self, direction, speed)
        # Synkende bilde
        filename = os.path.join(settings.ASSETS_DIR, settings.HOTAIR_BALLON_FILE)
        self.image_desc = utils.load_image(filename, settings.HOTAIR_BALLON_SIZE)
        
        # Stigende bilde
        filename = os.path.join(settings.ASSETS_DIR, settings.HOTAIR_BALLON_BURN_FILE)
        self.image_asc = utils.load_image(filename, settings.HOTAIR_BALLON_SIZE)
        
        self.image = self.image_desc
        self.rect = self.image.get_rect()

        
        # Starter på midten av skjermen
        self.rect.topleft = position
    
    def burn(self):
                # Python operere med radianer og ikke grader
        rad = math.radians(self.direction)

        # Regner ut x og y komponenten fra vektoren "speed*direction"
        x = math.cos(rad) * self.speed
        y = (math.sin(rad) * self.speed) + settings.BURN

        # Kalkulerer direction ut i fra x og y. atan2 håndterer fortegn
        rad = math.atan2(y/self.speed, x/self.speed) # Vinkel i radianer
        self.direction = math.degrees(rad) # Kalkulerer om radianer til grader

    def update(self):
        # Python operere med radianer og ikke grader
        rad = math.radians(self.direction)

        # Regner ut x og y komponenten fra vektoren "speed*direction"
        x = math.cos(rad) * self.speed
        y = math.sin(rad) * self.speed + settings.GRAVITY

        # Vi har landet
        if y > (settings.SCREEN_HEIGHT - 1):
            y = settings.SCREEN_HEIGHT - 1

        # Vi flyr ut av skjermen
        if y < 0:
            y = 1

        if x < 0:
            x = 0
        
        if (x + self.rect.width) > (settings.SCREEN_WIDTH -1):
            x = settings.SCREEN_WIDTH -1 - self.rect.width
            
        # Setter ny posisjon
        self.rect.left += x
        self.rect.top  += y

        # Kalkulerer direction ut i fra x og y. atan2 håndterer fortegn
        rad = math.atan2(y/self.speed, x/self.speed) # Vinkel i radianer
        self.direction = math.degrees(rad) # Kalkulerer om radianer til grader

    
    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect.topleft)
        if settings.DEBUG:
            surface.blit(
                utils.debug_text('{:.0f}° {}'.format(self.direction, self.speed)),
                (self.rect.left,self.rect.top-20))


class Cannonball(BaseObject):
    def __init__(self, position, direction=0, speed=0):
        BaseObject.__init__(self, direction, speed)
        filename = os.path.join(settings.ASSETS_DIR, settings.CANNONBALL_FILE)
        self.image = utils.load_image(filename, settings.CANNONBALL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
            
    def update(self):
        self.rect.top += self.speed
        # Sjekker om vi går over topp eller bunn    
        if (self.rect.top > self.surface.get_rect().bottom):
            self.rect.left = random.randint(0, self.surface.get_rect().width - self.rect.width)
            self.rect.top = -self.rect.height

    def draw(self):
        self.update()
        self.surface.blit(self.image, self.rect.topleft)

class Mine(BaseObject):
    def __init__(self,surface):
        BaseObject.__init__(self)
        self.surface = surface
        filename = os.path.join(settings.ASSETS_DIR, settings.MINE_FILE)
        self.image = utils.load_image(filename, settings.MINE_SIZE)
        self.rect = self.image.get_rect()
        
        # Starter random på toppen utenfor skjermen
        self.rect.left = random.randint(0, self.surface.get_rect().width - self.rect.width)
        self.rect.top = random.randint(0, self.surface.get_rect().height - self.rect.height)
    
    def update(self):
        pass

    def draw(self):
        self.update()
        self.surface.blit(self.image, self.rect.topleft)

    


