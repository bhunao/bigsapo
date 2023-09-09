import pygame
import sys
from random import randint
from pygame.locals import *
from pygame import image, Surface
from pygame.transform import rotate, flip
from pygame.math import Vector2
from typing import Dict, Set
pygame.init()

# Colours
BACKGROUND = (205, 163, 72)
WATER = (31, 93, 255)

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

SPRITES = {
    "fish": FISH,
    "peter": PETER,
    "snail": SNAIL,
}

catch_sound = pygame.mixer.Sound("imgs/jingles_SAX06.ogg")


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
        self.name = name
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
                entities[isca.fish.name].remove(isca.fish)
                isca.fish = None
                fish_caught += 1


def handle_fish():
    global entities, SPRITES

    to_remove = set()

    def pound_boundaries(name: str, fishable: bool = False):
        for fish in entities[name]:
            fish_width = fish.rect.size[0]
            too_far_right = fish.rect.left - fish_width*2 > WINDOW_WIDTH
            too_far_left = fish.rect.right + fish_width*2 < 0
            if too_far_right or too_far_left:
                to_remove.add(fish)

            if fishable and fish.rect.colliderect(isca) and not isca.fish:
                isca.fish = fish
                fish.sprite = rotate(SPRITES[name], 90)
                if fish.speed.x < 0:
                    fish.sprite = flip(fish.sprite, True, False)
                fish.speed.x = 0
                catch_sound.play()

    pound_boundaries("fish", fishable=True)
    pound_boundaries("snail", fishable=True)
    pound_boundaries("peter")

    for entity in to_remove:
        entities[entity.name].remove(entity)


def create_if_less_than(n, name: str):
    global entities
    total_entity = len(entities.get(name, []))
    if total_entity >= n:
        return

    match name:
        case "fish":
            entity = Entity(FISH, "fish")
        case "snail":
            entity = Entity(SNAIL, "snail")
        case "peter":
            entity = Entity(PETER, "peter")
    coisa = -1, 1
    mult = coisa[randint(0, 1)]
    entity.speed.x = randint(1, 2) * mult
    if mult == 1:
        entity.rect.topright = randint(-100, 0), randint(150, WINDOW_HEIGHT)
    else:
        entity.sprite = flip(entity.sprite, True, False)
        entity.rect.topleft = randint(
            WINDOW_WIDTH, WINDOW_WIDTH+150), randint(150, WINDOW_HEIGHT)


looping = True
my_font = pygame.font.SysFont('Arial', 30)


def frame():
    # The main game loop
    WINDOW.fill(BACKGROUND)
    water = Surface((WINDOW_WIDTH, WINDOW_HEIGHT-110))
    water.fill(WATER)
    WINDOW.blit(water, (0, 110))
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
    create_if_less_than(10, "fish")
    create_if_less_than(3, "peter")
    create_if_less_than(1, "snail")
    handle_fish()

    fog = Surface((WINDOW_WIDTH, WINDOW_HEIGHT-110))
    fog.fill(WATER)
    fog.set_alpha(128)
    WINDOW.blit(fog, (0, 110))

    frog.draw(WINDOW)

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
