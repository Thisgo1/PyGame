from pygame.math import Vector2

# tela
LARGURA_DA_TELA = 1280
ALTURA_DA_TELA = 720
TILE_SIZE = 64

# sobreposição de posições
OVERLAY_POSITION = {
    "tool": (40, ALTURA_DA_TELA - 15),
    "seed": (70, ALTURA_DA_TELA - 5)}

PLAYER_TOOL_OFFSET = {
    "left": Vector2(-50, 40),
    "right": Vector2(50, 40),
    "up": Vector2(0, -10),
    "down": Vector2(0, 50)
}

LAYERS = {
    "water": 0,
    "ground": 1,
    "soil": 2,
    "soil water": 3,
    "rain floor": 4,
    "house bottom":5,
    "ground plant": 6,
    "main": 7,
    "house top" : 8,
    "fruit": 9,
    "rain drops": 10
}
