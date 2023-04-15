import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # setup geral
        self.image = pygame.Surface((32, 64))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)

        # atributos para movimento
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()

        # vertical
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
    def move(self, dt):
      
      #normalizing a vector / normalizando um vetor
        if self.direction.magnitude() > 0:
          self.direction = self.direction.normalize()
        
        #movimento horizontal
        self.pos.x += self.direction.x *self.speed *dt
        self.rect.centerx = self.pos.x
        
        #movimento vertical
        self.pos.y += self.direction.y *self.speed *dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)