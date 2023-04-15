import pygame
from settings import *
from player import Player


class Level:
    def __init__(self) -> None:

        # get the display surface/ pegue a superficie do que esta sendo mostrado
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
    
        self.setup()
        
        
    def setup(self): #incia nosso player no level
      self.player = Player((640,360), self.all_sprites) #cria uma instancia da classe player 
      

    def run(self, dt):
        self.display_surface.fill('black') #torna a tela preta para que não se perceba a mudança de frames
        self.all_sprites.draw(self.display_surface) #faz com que os sprites apareçam na tela
        self.all_sprites.update() #atualiza todos os sprites
        
