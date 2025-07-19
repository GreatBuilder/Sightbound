import pygame
from settings import *
from assets import *
from sprites import *

# pygame setup
pygame.init()
pygame.display.set_caption("Sightbound")
screen = pygame.display.set_mode((screen_width, screen_height))
display = pygame.Surface((256, 256))
clock = pygame.time.Clock()
running = True
dt = 0

# Game states
game_paused = False

pygame.mixer.music.play(-1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text)
    screen.blit(img, (x, y))

def get_interactable_object(player_pos, game_map, boxes, vents):
    tile_x = int(player_pos[0] // 16)
    tile_y = int(player_pos[1] // 16)

    # Check for vent interaction (standing on it)
    if game_map[tile_y][tile_x] == 3: # 3 is vent
        for vent in vents:
            if vent.rect.collidepoint(player_pos):
                return vent

    # Check for box interaction (next to it)
    if game_map[tile_y][tile_x] == 0: # Must be on a floor tile
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            check_x, check_y = tile_x + dx, tile_y + dy
            if 0 <= check_y < len(game_map) and 0 <= check_x < len(game_map[0]):
                if game_map[check_y][check_x] == 2: # 2 is box
                    for box in boxes:
                        if box.rect.collidepoint(check_x * 16 + 8, check_y * 16 + 8):
                            return box

    return None

def main():
    global running, dt

    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    floor_sprites = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    vent_sprites = pygame.sprite.Group()
    player = None

    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x, y = col_index * 16, row_index * 16
            floor = Floor(x, y)
            floor_sprites.add(floor)
            all_sprites.add(floor)
            if tile == 1:
                wall = Wall(x, y)
                wall_sprites.add(wall)
                all_sprites.add(wall)
            elif tile == 2:
                box = Box(x, y)
                box_sprites.add(box)
                all_sprites.add(box)
            elif tile == 3:
                vent = Vent(x, y)
                vent_sprites.add(vent)
                all_sprites.add(vent)
            elif tile == 0 and player is None:
                player = Player(x + 8, y + 8)

    if not player:
        print("No starting position for player found!")
        return

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if player.hidden:
                        player.unhide()
                    else:
                        interactable = get_interactable_object(player.pos, game_map, box_sprites, vent_sprites)
                        if interactable:
                            player.hide(interactable)

        display.fill((0, 0, 0))

        player.update(dt, wall_sprites, box_sprites)

        camera_offset_x = player.rect.centerx - display.get_width() / 2
        camera_offset_y = player.rect.centery - display.get_height() / 2

        for sprite in sorted([s for s in all_sprites if s is not player], key=lambda s: s.rect.bottom):
            display.blit(sprite.image, (sprite.rect.x - camera_offset_x, sprite.rect.y - camera_offset_y))

        display.blit(player.image, (player.rect.x - camera_offset_x, player.rect.y - camera_offset_y))

        screen.blit(pygame.transform.scale(display, (screen_width, screen_height)), (0, 0))

        if SHOW_VERSION:
            font = pygame.font.Font(None, 24)
            text = font.render(VERSION, True, (255, 0, 0))
            text_rect = text.get_rect(bottomright=(screen_width - 10, screen_height - 10))
            screen.blit(text, text_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    pygame.quit()

main()