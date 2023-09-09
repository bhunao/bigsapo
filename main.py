import pygame
import sys
from random import randint
from pygame.locals import *
from pygame import image, Surface
from pygame.transform import rotate
from pygame.math import Vector2
from typing import Dict, Set
pygame.init()

# Colours
BACKGROUND = (205, 163, 72)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')

# SPRITES
BIGSAPO = image.load("imgs/frog_sit.png")
SNAIL = image.load("imgs/lesma.png")
PETER = image.load("imgs/INGHIA.png")
FISH = image.load("imgs/goldfish.png")
TONGUE_MIDDLE = image.load("imgs/tongue_middle.png")
TONGUE_END = image.load("imgs/tongue_end.png")


entities = dict()
fish_caught = 0


class Entity:
    sprite: Surface
    pos: Vector2
    speed: Vector2

    def __init__(self, sprite: Surface, name="any"):
        global entities
        if not entities.get(name):
            entities[name] = {self}
        entities[name].add(self)
        self.sprite = sprite
        self.pos: Vector2 = Vector2(0, 0)
        self.rect = self.sprite.get_rect()
        self.speed: Vector2 = Vector2(0, 0)

    def draw(self, window: Surface):
        window.blit(self.sprite, self.rect)

    def update(self):
        self.rect.move_ip(self.speed.x, self.speed.y)


entities: Dict[str, Set[Entity]]


frog = Entity(BIGSAPO, "frog")
frog.rect.centerx = WINDOW_WIDTH // 2
Entity(SNAIL, "snail")
Entity(PETER, "peter")
Entity(FISH, "fish")

isca = Entity(TONGUE_END, "isca")
isca.rect.centerx = WINDOW_WIDTH // 2 + 1
isca.fish = None

tongue = Entity(TONGUE_MIDDLE, "tongue")
tongue.rect.centerx = WINDOW_WIDTH // 2 + 2
tongue.rect.top = frog.rect.bottom


def handle_isca(mouse_y: int):
    global entities, fish_caught
    if not entities["isca"]:
        return

    for isca in entities["isca"]:
        diff = (mouse_y - isca.rect.centery) // 15
        diff += diff/diff if diff else 0
        isca.rect.move_ip(0, diff)
        isca.rect.y = max(isca.rect.y, frog.rect.bottom + 10)

        scale_w = tongue.rect.size[0]
        scale_h = isca.rect.top - tongue.rect.top
        size = scale_w, max(scale_h, 10)
        tongue.sprite = pygame.transform.scale(tongue.sprite, size)

        if isca.fish:
            isca.fish.rect.top = isca.rect.bottom - 20
            isca.fish.rect.centerx = isca.rect.centerx + 20
            if isca.rect.y <= 135:
                entities["fish"].remove(isca.fish)
                isca.fish = None
                fish_caught += 1


def handle_fish():
    global entities

    to_remove = set()
    for fish in entities["fish"]:
        fish_width = fish.rect.size[0]
        too_far_right = fish.rect.left - fish_width*2 > WINDOW_WIDTH
        too_far_left = fish.rect.right + fish_width*2 < 0
        if too_far_right or too_far_left:
            to_remove.add(fish)

        if fish.rect.colliderect(isca) and not isca.fish:
            fish.speed.x = 0
            isca.fish = fish
            fish.sprite = rotate(fish.sprite, 90)
            print("PEIXE NA ISCA", isca.fish)

    for fish in to_remove:
        entities["fish"].remove(fish)


def create_fish_if_less_than_n(n):
    global entities
    total_fish = len(entities["fish"])
    if total_fish >= n:
        return

    fish = Entity(FISH, "fish")
    fish.rect.topright = randint(-100, 0), randint(100, WINDOW_HEIGHT)
    fish.speed.x = randint(1, 2)


looping = True
my_font = pygame.font.SysFont('Arial', 30)


def frame():
    # The main game loop
    WINDOW.fill(BACKGROUND)
    # Get inputs
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Processing
    # This section will be built out later
    for name, entity_set in entities.items():
        for ent in entity_set:
            ent.draw(WINDOW)
            ent.update()

    mouse_y = pygame.mouse.get_pos()[1]
    text = f"{mouse_y}"
    text_surface = my_font.render(text, False, (0, 0, 0))
    WINDOW.blit(text_surface, (0, 0))
    text_surface = my_font.render(f"{isca.rect.y}", False, (0, 0, 0))
    WINDOW.blit(text_surface, (200, 0))
    text_surface = my_font.render(f"{fish_caught}", False, (0, 0, 0))
    WINDOW.blit(text_surface, (700, 0))
    handle_isca(mouse_y)
    create_fish_if_less_than_n(10)
    handle_fish()
    # Render elements of the game
    pygame.display.update()
    fpsClock.tick(FPS)


async def main():
    while 1:
        frame()
        await asyncio.sleep(0)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
