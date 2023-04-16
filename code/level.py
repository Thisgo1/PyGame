import pygame
from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from support import *


class Level:
    def __init__(self) -> None:

        # get the display surface/ pegue a superficie do que esta sendo mostrado
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):  # incia nosso player no level
        tmx_data = load_pygame('../data/map.tmx')

        # casa
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf,
                        self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf,
                        self.all_sprites, LAYERS['main'])
        # cerca
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf,
                    [self.all_sprites, self.collision_sprites])

        # água
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames,
                  self.all_sprites)

        # Flores e companhia
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [
                       self.all_sprites, self.collision_sprites])

        # arvores
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites,
                        self.collision_sprites, self.tree_sprites],
                name=obj.name,
                player_add=self.player_add
            )

        # camada de colisões
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE),
                    pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites,
                    self.tree_sprites)
        Generic(
            pos=(0, 0),
            surf=pygame.image.load(
                '../graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'])
        # cria uma instancia da classe player

    def player_add(self, item, count=1):
        self.player.item_inventory[item] += count

    def run(self, dt):
        # torna a tela preta para que não se perceba a mudança de frames
        self.display_surface.fill('black')
        # faz com que os sprites apareçam na tela
        self.all_sprites.custom_draw(self.player)
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
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                # analytics
                # if sprite == player:
                #     pygame.draw.rect(self.display_surface, 'red', offset_rect,5)
                #     hitbox_rect = player.hitbox.copy()
                #     hitbox_rect.center= offset_rect.center
                #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                #     target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                #     pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)
