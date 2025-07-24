import pygame
from settings import *
from assets import *
from inventory import Inventory
from sprites import Player, Wall, Floor, Box, Vent, Key, Door

# pygame setup
pygame.init()
pygame.display.set_caption("Sightbound")
screen = pygame.display.set_mode((screen_width, screen_height))
display = pygame.Surface((256, 256))
clock = pygame.time.Clock()
running = True
dt = 0
game_map = level_1_map
key_channel = pygame.mixer.Channel(3)

# game states
game_paused = False
pause_btn_hovered = False

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

# MAIN MENU
def main_menu():
    play_btn_hovered = False
    settings_gear_hovered = False
    while True:
        play_btn_rect = play_btn_img.get_rect(center=(screen_width // 2, (screen_height // 2) + 325))
        settings_gear_rect = settings_gear_img.get_rect(bottomright=(screen_width - 10, screen_height - 10))
        
        screen.blit(main_menu_img, (0, 0))
        
        # play button hover
        if play_btn_rect.collidepoint(pygame.mouse.get_pos()):
            scaled_play_btn_img = pygame.transform.scale(play_btn_img, (309, 160))
            if not play_btn_hovered:
                menu_btn_sounds[0].play()
                play_btn_hovered = True
        else:
            scaled_play_btn_img = pygame.transform.scale(play_btn_img, (290, 150))
            if play_btn_hovered:
                play_btn_hovered = False

        scaled_play_btn_rect = scaled_play_btn_img.get_rect(center=(screen_width // 2, (screen_height // 2) + 325))

        # update play button on the screen
        screen.blit(scaled_play_btn_img, scaled_play_btn_rect)

        # settings gear hover
        if settings_gear_rect.collidepoint(pygame.mouse.get_pos()):
            scaled_settings_gear_img = pygame.transform.scale(settings_gear_img, (106, 98))
            if not settings_gear_hovered:
                menu_btn_sounds[0].play()
                settings_gear_hovered = True
        else:
            scaled_settings_gear_img = pygame.transform.scale(settings_gear_img, (98, 90))
            if settings_gear_hovered:
                settings_gear_hovered = False

        # update settings gear button on the screen
        scaled_settings_gear_rect = scaled_settings_gear_img.get_rect(bottomright=(screen_width - 10, screen_height - 10))
        screen.blit(scaled_settings_gear_img, scaled_settings_gear_rect)

        # version text
        if SHOW_VERSION:
            font = pygame.font.Font(None, 24)
            text = font.render(VERSION, True, (255, 0, 0))
            text_rect = text.get_rect(topleft=(10, 10))
            screen.blit(text, text_rect)

        # Handle events after buttons are positioned
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_btn_sounds[2].play()
                return False  # Quit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if scaled_play_btn_rect.collidepoint(event.pos):
                    return True # Play
                if scaled_settings_gear_rect.collidepoint(event.pos):
                    menu_btn_sounds[2].play()
                    return "settings" # Open settings menu

        pygame.display.flip()
        clock.tick(60)

def settings():
    global vol_btn_img
    global game_paused
    back_btn_hovered = False
    info_btn_hovered = False
    vol_btn_hovered = False
    vol_btn_state = "full"
    while True:
        screen.fill((0, 0, 0))
        screen.blit(settings_menu_img, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # --- Back Button --- #
        # Use a temporary rect for initial collision check
        temp_back_rect = pygame.transform.scale(back_btn_img, (113, 90)).get_rect(bottomright=(screen_width - 10, screen_height - 10))
        if 'scaled_back_btn_rect' in locals(): # Use previous frame's rect if available
            temp_back_rect = scaled_back_btn_rect

        if temp_back_rect.collidepoint(mouse_pos):
            scaled_back_btn_img = pygame.transform.scale(back_btn_img, (123, 98))
            if not back_btn_hovered:
                menu_btn_sounds[0].play()
                back_btn_hovered = True
        else:
            scaled_back_btn_img = pygame.transform.scale(back_btn_img, (113, 90))
            if back_btn_hovered:
                back_btn_hovered = False
        scaled_back_btn_rect = scaled_back_btn_img.get_rect(bottomright=(screen_width - 10, screen_height - 10))
        screen.blit(scaled_back_btn_img, scaled_back_btn_rect)

        # --- Info Button --- #
        temp_info_rect = pygame.transform.scale(info_btn_img, (90, 90)).get_rect(bottomleft=(10, screen_height - 10))
        if 'scaled_info_btn_rect' in locals():
            temp_info_rect = scaled_info_btn_rect

        if temp_info_rect.collidepoint(mouse_pos):
            scaled_info_btn_img = pygame.transform.scale(info_btn_img, (100, 100))
            if not info_btn_hovered:
                menu_btn_sounds[0].play()
                info_btn_hovered = True
        else:
            scaled_info_btn_img = pygame.transform.scale(info_btn_img, (90, 90))
            if info_btn_hovered:
                info_btn_hovered = False
        scaled_info_btn_rect = scaled_info_btn_img.get_rect(bottomleft=(10, screen_height - 10))
        screen.blit(scaled_info_btn_img, scaled_info_btn_rect)

        # --- Volume Button --- #
        temp_vol_rect = pygame.transform.scale(vol_btn_img, (95, 90)).get_rect(center=(75, 300))
        if 'scaled_vol_btn_rect' in locals():
            temp_vol_rect = scaled_vol_btn_rect

        if temp_vol_rect.collidepoint(mouse_pos):
            scaled_vol_btn_img = pygame.transform.scale(vol_btn_img, (110, 100))
            if not vol_btn_hovered:
                menu_btn_sounds[0].play()
                vol_btn_hovered = True
        else:
            scaled_vol_btn_img = pygame.transform.scale(vol_btn_img, (95, 90))
            if vol_btn_hovered:
                vol_btn_hovered = False
        scaled_vol_btn_rect = scaled_vol_btn_img.get_rect(center=(75, 300))
        screen.blit(scaled_vol_btn_img, scaled_vol_btn_rect)

        # Handle events after buttons are positioned
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_btn_sounds[2].play()
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if scaled_back_btn_rect.collidepoint(event.pos):
                    menu_btn_sounds[2].play()
                    if not game_paused:
                        return True
                    else:
                        return 'paused'
                if scaled_info_btn_rect.collidepoint(event.pos):
                    # Display popup with how to play the game
                    menu_btn_sounds[2].play()
                    pass
                if scaled_vol_btn_rect.collidepoint(event.pos):
                    # change sprite to mute
                    menu_btn_sounds[2].play()
                    if vol_btn_state == "full":
                        vol_btn_state = "mute"
                        vol_btn_img = pygame.image.load("Assets/UI/vol_mute.png")
                        pygame.mixer.music.set_volume(0)
                        footsteps_sound.set_volume(0)
                        box_open_sound.set_volume(0)
                        box_close_sound.set_volume(0)
                        vent_open_sound.set_volume(0)
                        vent_close_sound.set_volume(0)
                        key_pickup_sound.set_volume(0)
                        key_drop_sound.set_volume(0)
                    else:
                        vol_btn_state = "full"
                        pygame.mixer.music.set_volume(1)
                        vol_btn_img = pygame.image.load("Assets/UI/vol_full.png")
                        footsteps_sound.set_volume(footsteps)
                        box_open_sound.set_volume(boxes)
                        box_close_sound.set_volume(boxes)
                        vent_open_sound.set_volume(vents)
                        vent_close_sound.set_volume(vents)
                        key_pickup_sound.set_volume(keys)
                        key_drop_sound.set_volume(keys)

        pygame.display.flip()
        clock.tick(60)

def main():
    global running, dt, game_paused, pause_btn_hovered

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

    inventory = Inventory()

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
                                key_channel.play(key_pickup_sound)
                                inventory.drop_item() # Removes key from selected slot
                        elif isinstance(interactable, Key):
                            inventory.add_item(key_item)
                            key_channel.play(key_pickup_sound)
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
                            key_channel.play(key_drop_sound)
                        tile_x = int(player.pos.x // 16)
                        tile_y = int(player.pos.y // 16)
                        # Prevent dropping items in walls, boxes or vents
                        if game_map[tile_y][tile_x] not in [1, 2, 3]:
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

        # --- Pause Button --- #
        mouse_pos = pygame.mouse.get_pos()
        temp_pause_rect = pygame.transform.scale(pause_btn_img, (103, 90)).get_rect(topright=(screen_width - 10, 10))
        if 'scaled_pause_btn_rect' in locals():
            temp_pause_rect = scaled_pause_btn_rect

        if temp_pause_rect.collidepoint(mouse_pos):
            scaled_pause_btn_img = pygame.transform.scale(pause_btn_img, (113, 100))
            if not pause_btn_hovered:
                menu_btn_sounds[0].play()
                pause_btn_hovered = True
        else:
            scaled_pause_btn_img = pygame.transform.scale(pause_btn_img, (103, 90))
            if pause_btn_hovered:
                pause_btn_hovered = False
        scaled_pause_btn_rect = scaled_pause_btn_img.get_rect(topright=(screen_width - 10, 10))

        inventory.draw(display)
        player.ui_update(display)
        
        screen.blit(pygame.transform.scale(display, (screen_width, screen_height)), (0, 0))
        screen.blit(scaled_pause_btn_img, scaled_pause_btn_rect)

        if SHOW_VERSION:
            font = pygame.font.Font(None, 24)
            text = font.render(VERSION, True, (255, 0, 0))
            text_rect = text.get_rect(topleft=(10, 10))
            screen.blit(text, text_rect)

        pygame.display.flip()

        dt = clock.tick(60) / 1000
    pygame.quit()

# Game loop
while True:
    choice = main_menu()
    if choice is True:
        pygame.mixer.music.play(-1)
        main()
    elif choice == "settings":
        settings_result = settings()
        if settings_result is False:
            break
    else:  # Quit
        break