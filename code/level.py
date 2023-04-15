import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic


class Level:
    def __init__(self) -> None:

        # get the display surface/ pegue a superficie do que esta sendo mostrado
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):  # incia nosso player no level
        self.player = Player((640, 360), self.all_sprites)
        Generic(
            pos=(0, 0),
            surf=pygame.image.load(
                '../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'])
        # cria uma instancia da classe player

    def run(self, dt):
        # torna a tela preta para que não se perceba a mudança de frames
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)  # faz com que os sprites apareçam na tela
        self.all_sprites.update(dt)  # atualiza todos os sprites

        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
      self.offset.x = player.rect.centerx - LARGURA_DA_TELA / 2
      self.offset.y = player.rect.centery - ALTURA_DA_TELA / 2
      
      for layer in LAYERS.values():
        for sprite in self.sprites():
            if sprite.z == layer:
              offset_rect = sprite.rect.copy()
              offset_rect.center -= self.offset
              self.display_surface.blit(sprite.image, offset_rect)


  
