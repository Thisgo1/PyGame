import pygame, sys
from settings import *
from level import Level
from player import Player

class Game:
  def __init__(self) -> pygame:
    pygame.init() #inciando o pygame
    self.screen = pygame.display.set_mode((LARGURA_DA_TELA, ALTURA_DA_TELA))
    pygame.display.set_caption('Maranhão')
    self.clock = pygame.time.Clock()
    self.level = Level()

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      
      dt = self.clock.tick() / 1000 #delta time para atualizar o jogo
      self.level.run(dt)
      pygame.display.update()
      

if __name__ == "__main__":#checando se estamos no arquivo principal
  game = Game() #atribuindo a classe 
  game.run() #começando o jogo

