import pygame
from settings import *
from assets import *
from sprites import Player, Wall, Floor, Box, Vent, Key, Door
from inventory import Inventory

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
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def get_interactable_object(player, game_map, boxes, vents, keys, doors):
    player_tile_x = int(player.pos[0] // 16)
    player_tile_y = int(player.pos[1] // 16)

    # Priority 1: Check for objects the player is colliding with (e.g., keys on the ground)
    for key in keys:
        if key.rect.colliderect(player.rect):
            return key

    # Priority 2: Check for objects adjacent to the player (e.g., doors, boxes to hide in)
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        check_x, check_y = player_tile_x + dx, player_tile_y + dy
        if 0 <= check_y < len(game_map) and 0 <= check_x < len(game_map[0]):
            tile_content = game_map[check_y][check_x]
            if tile_content == 5:  # Door
                for door in doors:
                    if door.rect.x // 16 == check_x and door.rect.y // 16 == check_y:
                        return door
            elif tile_content == 2:  # Box
                for box in boxes:
                    if box.rect.x // 16 == check_x and box.rect.y // 16 == check_y:
                        return box

    # Priority 3: Check for objects the player is standing on (e.g., vents, boxes)
    tile_under_player = game_map[player_tile_y][player_tile_x]
    if tile_under_player == 3:  # Vent
        for vent in vents:
            if vent.rect.collidepoint(player.pos):
                return vent
    elif tile_under_player == 2: # Box
        for box in boxes:
            if box.rect.collidepoint(player.pos):
                return box

    return None

def main():
    global running, dt

    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    floor_sprites = pygame.sprite.Group()
    box_sprites = pygame.sprite.Group()
    vent_sprites = pygame.sprite.Group()
    key_sprites = pygame.sprite.Group()
    door_sprites = pygame.sprite.Group()
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
            elif tile == 4:
                key = Key(x, y)
                key_sprites.add(key)
                all_sprites.add(key)
            elif tile == 5:
                door = Door(x, y)
                door_sprites.add(door)
                all_sprites.add(door)
            elif tile == 0 and player is None:
                player = Player(x + 8, y + 8)

    if player is None:
        print("No starting position for player found!")
        return

    inventory = Inventory(inv_slot_img, inv_select_img)

    # Lighting surface
    fog = pygame.Surface((display.get_width(), display.get_height()), pygame.SRCALPHA)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    interactable = get_interactable_object(player, game_map, box_sprites, vent_sprites, key_sprites, door_sprites)
                    if interactable:
                        if isinstance(interactable, Door):
                            selected_item = inventory.get_selected_item()
                            if selected_item == key_item:
                                interactable.unlock()
                                key_pickup_sound.play()
                                inventory.drop_item() # Removes key from selected slot
                        elif isinstance(interactable, Key):
                            inventory.add_item(key_item)
                            key_pickup_sound.play()
                            game_map[interactable.rect.y // 16][interactable.rect.x // 16] = 0
                            interactable.kill()
                        elif isinstance(interactable, (Box, Vent)):
                            if player.hidden:
                                player.unhide()
                            else:
                                player.hide(interactable)
                if event.key == pygame.K_1:
                    inventory.selected_slot = 0
                if event.key == pygame.K_2:
                    inventory.selected_slot = 1
                if event.key == pygame.K_3:
                    inventory.selected_slot = 2
                if event.key == pygame.K_4:
                    inventory.selected_slot = 3
                if event.key == pygame.K_q:
                    dropped_item_type = inventory.drop_item()
                    if dropped_item_type:
                        if dropped_item_type == key_item:
                            key_drop_sound.play()
                        tile_x = int(player.pos.x // 16)
                        tile_y = int(player.pos.y // 16)
                        # Prevent dropping items in walls or boxes
                        if game_map[tile_y][tile_x] not in [1, 2]:
                            game_map[tile_y][tile_x] = 4 # Mark as key
                            new_item = Key(tile_x * 16, tile_y * 16) # Create at topleft of tile
                            all_sprites.add(new_item)
                            key_sprites.add(new_item)

        display.fill((0, 0, 0))

        player.update(dt, wall_sprites, box_sprites, door_sprites)

        camera_offset_x = player.rect.centerx - display.get_width() / 2
        camera_offset_y = player.rect.centery - display.get_height() / 2

        for sprite in sorted([s for s in all_sprites if s is not player], key=lambda s: s.rect.bottom):
            display.blit(sprite.image, (sprite.rect.x - camera_offset_x, sprite.rect.y - camera_offset_y))

        display.blit(player.image, (player.rect.x - camera_offset_x, player.rect.y - camera_offset_y))

        # Render lighting
        fog.fill(NIGHT_COLOR)
        player_center_on_display = (player.rect.centerx - camera_offset_x, player.rect.centery - camera_offset_y)
        pygame.draw.circle(fog, LIGHT_COLOR, player_center_on_display, LIGHT_RADIUS)
        display.blit(fog, (0, 0))

        inventory.draw(display)

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