import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        # setup geral
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # atributos para movimento
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool)
        }
        # ferramentas
        self.selected_tool = 'axe'

    def use_tool(self):
        print(self.selected_tool)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:

            # direções
            # vertical
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
                # horizontal
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # uso de ferramentas
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

    def get_status(self):
        # checa se o jogador esta se mexendo, e depois adicionar _idle ao status
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        # uso de ferramentas
        if self.timers['tool use'].active:
            if 'idle' in self.status:
                self.status = self.status.split(
                    '_')[0] + '_' + self.selected_tool

    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
            'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
            'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            # como temos um número finito de sprites, sempre recomeçamos as animações
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def move(self, dt):

        # normalizing a vector / normalizando um vetor
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # movimento horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # movimento vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.update_timers()
        self.get_status()
