import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group, collision_sprites, tree_sprites):
        super().__init__(group)

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        # setup geral
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.z = LAYERS['main']

        # atributos para movimento
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # colisão

        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate((-126, -70))

        # timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }
        # ferramentas
        self.tools = ['axe', 'hoe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # sementes
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # inventory
        self.item_inventory = {
            'apple': 0,
            'wood': 0,
            'corn': 0,
            'tomato': 0
        }

        # interaction
        self.tree_sprites = tree_sprites

    def use_tool(self):
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        if self.selected_tool == 'hoe':
            pass
        if self.selected_tool == 'water':
            pass

    def get_target_position(self):

        self.target_pos = self.rect.center + \
            PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        pass

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

            # ferramentas
            # uso de ferramentas
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            # mudar ferramentas
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(
                    self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            # sementes
            # usar sementes
            if keys[pygame.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # mudar sementes
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                self.seed_index = self.seed_index if self.seed_index < len(
                    self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]

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
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # movimento vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # indo para direita
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # indo para esquerda
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0:  # indo para baixo
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # indo para cima
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.update_timers()
        self.get_target_position()
        self.get_status()
