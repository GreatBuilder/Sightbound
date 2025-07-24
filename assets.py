import pygame
from settings import screen_width, screen_height
from item_type import ItemType

pygame.mixer.init()

# Music and Sound
pygame.mixer.music.load("Assets/Audio/ambient_background.mp3")
pygame.mixer.music.set_volume(0.3)
menu_btn_sounds = [pygame.mixer.Sound("Assets/Audio/menu_btn_1.mp3"), pygame.mixer.Sound("Assets/Audio/menu_btn_2.mp3"), pygame.mixer.Sound("Assets/Audio/btn_click.mp3")]
footsteps_sound = pygame.mixer.Sound("Assets/Audio/footsteps.mp3")
box_open_sound = pygame.mixer.Sound("Assets/Audio/box_open.mp3")
box_close_sound = pygame.mixer.Sound("Assets/Audio/box_close.mp3")
vent_open_sound = pygame.mixer.Sound("Assets/Audio/vent_open.mp3")
vent_close_sound = pygame.mixer.Sound("Assets/Audio/vent_close.mp3")
key_pickup_sound = pygame.mixer.Sound("Assets/Audio/key_pickup.mp3")
key_drop_sound = pygame.mixer.Sound("Assets/Audio/key_drop.mp3")

# Set volumes
vents = 0.3
keys = 0.4
boxes = 0.2
footsteps = 1
footsteps_sound.set_volume(footsteps)
box_open_sound.set_volume(boxes)
box_close_sound.set_volume(boxes)
vent_open_sound.set_volume(vents)
vent_close_sound.set_volume(vents)
key_pickup_sound.set_volume(keys)
key_drop_sound.set_volume(keys)

# UI Images
main_menu_img_raw = pygame.image.load("Assets/UI/main_menu_bg.png")
settings_menu_img_raw = pygame.image.load("Assets/UI/settings_menu_bg.png")
play_btn_img_raw = pygame.image.load("Assets/UI/play_btn.png")
settings_gear_img_raw = pygame.image.load("Assets/UI/settings_gear.png")
back_btn_img_raw = pygame.image.load("Assets/UI/back_btn.png")
info_btn_img_raw = pygame.image.load("Assets/UI/info_btn.png")
vol_btn_img = pygame.image.load("Assets/UI/vol_full.png")
pause_btn_img = pygame.image.load("Assets/UI/pause_btn.png")

# Resizing UI
main_menu_img = pygame.transform.scale(main_menu_img_raw, (screen_width, screen_height))
settings_menu_img = pygame.transform.scale(settings_menu_img_raw, (screen_width, screen_height))
play_btn_img = pygame.transform.scale(play_btn_img_raw, (290, 150))
settings_gear_img = pygame.transform.scale(settings_gear_img_raw, (98, 90))
back_btn_img = pygame.transform.scale(back_btn_img_raw, (113, 90))
info_btn_img = pygame.transform.scale(info_btn_img_raw, (90, 90))
vol_btn_img = pygame.transform.scale(vol_btn_img, (95, 90))
pause_btn_img = pygame.transform.scale(pause_btn_img, (103, 90))

# Characters
player_idle_imgs = [pygame.image.load("Assets/Characters/Idle1.png"), pygame.image.load("Assets/Characters/Idle2.png"), pygame.image.load("Assets/Characters/Idle3.png"), pygame.image.load("Assets/Characters/Idle4.png")]
player_walk_imgs = [pygame.image.load("Assets/Characters/Walk1.png"), pygame.image.load("Assets/Characters/Walk2.png"), pygame.image.load("Assets/Characters/Walk3.png")]
security_idle_imgs = [pygame.image.load("Assets/Characters/sec_idle_0.png"), pygame.image.load("Assets/Characters/sec_idle_1.png"), pygame.image.load("Assets/Characters/sec_idle_2.png"), pygame.image.load("Assets/Characters/sec_idle_3.png")]
security_walk_imgs = [pygame.image.load("Assets/Characters/sec_walk_0.png"), pygame.image.load("Assets/Characters/sec_walk_1.png"), pygame.image.load("Assets/Characters/sec_walk_2.png")]

# Tiles
floor_img = pygame.image.load("Assets/Tiles/Floor.png")
wall_img = pygame.image.load("Assets/Tiles/Wall.png")
box_img = pygame.image.load("Assets/Tiles/Box.png")
vent_img = pygame.image.load("Assets/Tiles/Vent.png")
key_img = pygame.image.load("Assets/Tiles/Key.png")
door_img = pygame.image.load("Assets/Tiles/door.png")

# UI
key_inv_img = pygame.image.load("Assets/UI/Key_inv.png")
inv_slot_img = pygame.image.load("Assets/UI/inventory_slot.png")
inv_select_img = pygame.image.load("Assets/UI/Inv_Select.png")

# Item Definitions
key_item = ItemType(name="Key", world_img=key_img, inv_img=key_inv_img)