import pygame
import sys
from random import randint
from pygame.locals import *
from pygame import image, Surface
from pygame.transform import rotate, flip, scale
from pygame.math import Vector2
from typing import Dict, Set
from math import sin


def get_outline(image, color=(0, 0, 0), threshold=127, thick=1):
    mask = pygame.mask.from_surface(image, threshold)
    outline_image = Surface(image.get_size()).convert_alpha()
    outline_image.fill((0, 0, 0, 0))
    outline_image.set_alpha(128)
    points = mask.outline()
    for i in range(0, len(points), 15):
        points.append((
            points[i][0] + randint(-2, 2),
            points[i][1] + randint(-2, 2)
        ))
    pygame.draw.lines(outline_image, color, True, points, 2*thick)
    pygame.draw.lines(outline_image, (0, 255, 255), True, points, thick)
    return outline_image


pygame.init()

# Colours
BACKGROUND = (205, 163, 72)
BLACK = (0, 0, 0)
WATER = (31, 93, 255)

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

frame_n = 0

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('BIG SAPO')

# SPRITES
BACKGROUND = image.load("imgs/background.png")
BIGSAPO = [image.load("imgs/frog_sit2.png")]
BIGSAPO_SHOCK = [image.load("imgs/frog_elec.png")]
TONGUE_MIDDLE = image.load("imgs/tongue_middle.png")
TONGUE_END = image.load("imgs/tongue_end.png")
SNAIL = [image.load("imgs/lesma.png")]
PETER = [
    image.load("imgs/eel/eel 1.png"),
    image.load("imgs/eel/eel 2.png"),
    image.load("imgs/eel/eel 3.png"),
    image.load("imgs/eel/eel 4.png"),
    image.load("imgs/eel/eel 5.png"),
    image.load("imgs/eel/eel 6.png"),
    image.load("imgs/eel/eel 7.png"),
    image.load("imgs/eel/eel 8.png"),
    image.load("imgs/eel/eel 9.png"),
    image.load("imgs/eel/eel 10.png"),
    image.load("imgs/eel/eel 11.png"),
    image.load("imgs/eel/eel 12.png"),
    image.load("imgs/eel/eel 13.png"),
]
FISH = [
    image.load("imgs/pexe/pexe 1.png"),
    image.load("imgs/pexe/pexe 2.png"),
    image.load("imgs/pexe/pexe 3.png"),
    image.load("imgs/pexe/pexe 4.png"),
    image.load("imgs/pexe/pexe 5.png"),
    image.load("imgs/pexe/pexe 6.png"),
    image.load("imgs/pexe/pexe 7.png"),
    image.load("imgs/pexe/pexe 8.png"),
    image.load("imgs/pexe/pexe 9.png"),
    image.load("imgs/pexe/pexe 10.png"),
]

SPRITES = {
    "fish": FISH,
    "peter": PETER,
    "snail": SNAIL,
}

catch_sound = pygame.mixer.Sound("imgs/jingles_SAX06.ogg")
fail_sound = pygame.mixer.Sound("imgs/highDown.ogg")
good_sound = pygame.mixer.Sound("imgs/powerUp2.ogg")


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

        if not isinstance(sprite, list):
            sprite = [sprite]

        self.name = name
        self.sprite = sprite
        self.pos: Vector2 = Vector2(0, 0)
        self.speed: Vector2 = Vector2(0, 0)
        self.rect = self.sprite[0].get_rect()

    def draw(self, window: Surface):
        frames = 5 // self.speed.x if self.speed.x else 1
        i = frame_n % (frames * len(self.sprite)) // frames
        i = int(i)
        window.blit(self.sprite[i], self.rect)

    def update(self):
        self.rect.move_ip(self.speed.x, self.speed.y)


entities: Dict[str, Set[Entity]]


frog = Entity(BIGSAPO, "frog")
frog.rect.centerx = WINDOW_WIDTH // 2
frog.rect.centery = 110
frog_bottom = frog.rect.bottom
frog.shocked = False

isca = Entity(TONGUE_END, "isca")
isca.rect.centerx = WINDOW_WIDTH // 2 + 1
isca.fish = None

tongue = Entity(TONGUE_MIDDLE, "tongue")
tongue.rect.centerx = WINDOW_WIDTH // 2 + 2

tongue.rect.top = frog_bottom - 30


def handle_isca(mouse_y: int):
    global entities, fish_caught, isca
    if not entities["isca"]:
        return

    if frog.shocked:
        frames = 10
        i = frame_n % (frames * 2) // frames
        i = int(i)
        sprites = BIGSAPO + BIGSAPO_SHOCK
        frog.sprite = [sprites[i]]
        if frog.shocked < 5:
            frog.sprite = BIGSAPO
        if frog.shocked > 0:
            frog.shocked -= 1

        thick = 5
        outline = get_outline(BIGSAPO[0], (150, 150, 255), 100, thick*2)
        WINDOW.blit(outline, frog.rect)
        outline = get_outline(tongue.sprite[0], (150, 150, 255), 100, thick)
        WINDOW.blit(outline, tongue.rect)
        outline = get_outline(isca.sprite[0], (150, 150, 255), 100, thick)
        WINDOW.blit(outline, isca.rect)

    for isca in entities["isca"]:
        diff = (mouse_y - isca.rect.centery) // 15
        diff += diff/diff if diff else 0
        isca.rect.move_ip(0, diff)
        isca.rect.y = max(isca.rect.y, frog_bottom + 10)

        scale_w = tongue.rect.size[0]
        scale_h = isca.rect.top - tongue.rect.top
        size = scale_w, max(scale_h, 10)
        tongue.sprite = [scale(f, size) for f in tongue.sprite]

        if isca.fish:
            isca.fish.rect.top = isca.rect.bottom - 30
            isca.fish.rect.centerx = isca.rect.centerx + 25
            frog_bottom_plus_tongue = frog_bottom + 10
            if isca.rect.y <= frog_bottom_plus_tongue:
                entities[isca.fish.name].remove(isca.fish)
                isca.fish = None
                catch_sound.play()
                fish_caught += 1


def handle_fish():
    global entities, SPRITES

    to_remove = set()

    def pound_boundaries(name: str, fishable: bool = False):
        for fish in entities[name]:
            fish_width = fish.rect.size[0]
            too_far_right = fish.rect.left - fish_width*1 > WINDOW_WIDTH
            too_far_left = fish.rect.right + fish_width*1 < 0
            if too_far_right or too_far_left:
                to_remove.add(fish)

            if fish.rect.colliderect(isca):
                if fishable and not isca.fish and not frog.shocked:
                    isca.fish = fish
                    fish.sprite = [rotate(f, 90) for f in SPRITES[name]]
                    if fish.speed.x < 0:
                        fish.sprite = [flip(f, True, False) for f in fish.sprite]
                    fish.speed.x = 0
                    good_sound.play()
                elif not frog.shocked and not fishable:
                    frog.shocked = 50
                    fail_sound.play()
                    if isca.fish:
                        to_remove.add(isca.fish)
                        isca.fish = None

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
    entity.speed.x = randint(1, 3) * mult
    if mult == 1:
        entity.rect.topright = randint(-100, 0), randint(frog_bottom + 30, WINDOW_HEIGHT)
    else:
        entity.sprite = [flip(f, True, False) for f in entity.sprite]
        entity.rect.topleft = randint(
            WINDOW_WIDTH, WINDOW_WIDTH+150), randint(frog_bottom + 30, WINDOW_HEIGHT-50)


my_font = pygame.font.SysFont('Arial', 30, bold=True)
fog = Surface((WINDOW_WIDTH, WINDOW_HEIGHT-110))
fog.fill(WATER)
for n in range(0, 255, 10):
    pygame.draw.line(fog, (255-n/2, 255-n/2, 255-n), (0, n*5), (WINDOW_WIDTH, n*5), 50)


def frame():
    # The main game loop
    WINDOW.blit(BACKGROUND, (0, 0))
    water = Surface((WINDOW_WIDTH, WINDOW_HEIGHT-frog.rect.bottom))
    water.fill(WATER)
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

            if name == "peter":
                frames = 5 // ent.speed.x if ent.speed.x else 1
                i = frame_n % (frames * len(ent.sprite)) // frames
                i = int(i) + 1
                i %= len(ent.sprite)
                thick = 10 * sin(frame_n*.15)
                thick = int(thick)
                outline = get_outline(ent.sprite[i], (150, 150, 255), 100, thick)
                WINDOW.blit(outline, ent.rect)

    mouse_y = pygame.mouse.get_pos()[1]
    text_surface = my_font.render(f"Fish caught: {fish_caught}", False, BLACK)
    WINDOW.blit(text_surface, (50, frog.rect.top))

    create_if_less_than(10, "fish")
    create_if_less_than(3, "peter")
    create_if_less_than(1, "snail")

    handle_isca(mouse_y)
    handle_fish()

    fog.set_alpha(64)
    WINDOW.blit(fog, (0, frog_bottom))

    frog.draw(WINDOW)

    # Render elements of the game
    pygame.display.update()
    fpsClock.tick(FPS)


async def main():
    global frame_n
    while 1:
        frame()
        frame_n += 1
        if frame_n > 1_000_000_000:
            frame_n = 0
        await asyncio.sleep(0)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
