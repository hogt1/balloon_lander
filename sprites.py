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
        y = math.sin(rad) * self.speed
        return x, y
    
    def set_direction_xy(self, x, y):
        # Kalkulerer direction ut i fra x og y. atan2 håndterer fortegn
        rad = math.atan2(y/self.speed, x/self.speed) # Vinkel i radianer
        self.direction = math.degrees(rad) # Kalkulerer om radianer til grader


class HotAirBalloon(BaseObject):
    def __init__(self, position, direction=0, speed=1):
        self.points = 0
        self.level = 1
        self.level_up = False
        self.hit = False
        BaseObject.__init__(self, direction, speed)
        # Synkende bilde
        filename = os.path.join(settings.ASSETS_DIR, settings.HOTAIR_BALLON_FILE)
        self.image_desc = utils.load_image(filename, settings.HOTAIR_BALLON_SIZE)
        
        self.burn_filename = filename = os.path.join(settings.ASSETS_DIR, settings.SOUND_BURN_FILE)
        # Stigende bilde
        filename = os.path.join(settings.ASSETS_DIR, settings.HOTAIR_BALLON_BURN_FILE)
        self.image_asc = utils.load_image(filename, settings.HOTAIR_BALLON_SIZE)
        
        self.image = self.image_desc
        self.rect = self.image.get_rect()

        self.rect.left = position[0]
        self.rect.top = position[1]
        self.direction = 0
        self.speed = settings.WIND

        self.burn_count = 0
        pygame.mixer.music.load(self.burn_filename)
    
    def burn(self):
        self.direction += settings.BURN
        if self.direction < -90:
            self.direction = -90
        if not pygame.mixer.get_busy():
            pygame.mixer.music.play(0)
        self.burn_count = 15



    def update(self):
        self.level_up = False
        self.direction += settings.BALLON_DESC_RATE
        if self.direction > 90:
            self.direction = 90

        dx, dy = self.direction_xy()

        if self.burn_count:
            self.image = self.image_asc
            self.burn_count -= 1
        else:
            self.image = self.image_desc
            if pygame.mixer.get_busy():
                pygame.mixer.stop()
        self.rect.top += dy
        self.rect.left += dx
        self.points = self.rect.left*self.level
        # Vi har landet
        if self.rect.top > (settings.SCREEN_HEIGHT - 1 - self.rect.height):
            self.rect.top = settings.SCREEN_HEIGHT - 1 - self.rect.height
            self.hit = True

        # Vi flyr ut av skjermen
        if self.rect.top < 0:
            self.rect.top = 0
            self.hit = True

        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.left > (settings.SCREEN_WIDTH -1):
            self.rect.right = 0
            self.level += 1
            self.speed += 0.3
            self.level_up = True

        '''
        if settings.DEBUG:
            draw_rect = self.rect
            draw_rect = pygame.rect.Rect(0,0, self.rect.width-1, self.rect.height -1)
            pygame.draw.rect(self.image, (255, 255, 255), draw_rect, 1)
        '''
        
    
class Cannonball(BaseObject):
    def __init__(self, position, direction=0, speed=0):
        BaseObject.__init__(self, direction, speed)
        filename = os.path.join(settings.ASSETS_DIR, settings.CANNONBALL_FILE)
        self.image = utils.load_image(filename, settings.CANNONBALL_SIZE)
        self.rect = self.image.get_rect()
        self.rect.left = position[0]
        self.rect.top = position[1]
            
    def update(self):
        self.rect.top += self.speed
        # Sjekker om vi går over topp eller bunn    
        if (self.rect.top > settings.SCREEN_HEIGHT - 1):
            self.rect.left = random.randint(0, settings.SCREEN_WIDTH - 1 - self.rect.width)
            self.rect.top = -self.rect.height

class Mine(BaseObject):
    def __init__(self, position, direction=0, speed=0):
        BaseObject.__init__(self, direction, speed)
        filename = os.path.join(settings.ASSETS_DIR, settings.MINE_FILE)
        self.image = utils.load_image(filename, settings.MINE_SIZE)
        self.rect = self.image.get_rect()
        
        # Starter random på skjermen
        self.rect.left = random.randint(200, settings.SCREEN_WIDTH - self.rect.width) - 1 
        self.rect.top = random.randint(0, settings.SCREEN_HEIGHT  - self.rect.height)
    
    def update(self):
        pass
        '''
        if settings.DEBUG:
            draw_rect = self.rect
            draw_rect = pygame.rect.Rect(0,0, self.rect.width-1, self.rect.height -1)
            pygame.draw.rect(self.image, (255, 255, 255), draw_rect, 1)
        '''
    


