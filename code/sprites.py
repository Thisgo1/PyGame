import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class Water(Generic):
    def __init__(self, pos, frames, groups):

        # setup de animação
        self.frames = frames
        self.frame_index = 0

        # setup dos sprites
        super().__init__(
            pos=pos, surf=self.frames[self.frame_index], groups=groups, z=LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.frames):
            # como temos um número finito de sprites, sempre recomeçamos as animações
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
  def __init__(self, pos, surf, groups):
      super().__init__(pos, surf, groups)

class Tree(Generic):
  def __init__(self, pos, surf, groups, name):
      super().__init__(pos, surf, groups)
