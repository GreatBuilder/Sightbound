import pygame
from settings import screen_width, screen_height
pygame.mixer.init()

# Music and Sound
pygame.mixer.music.load("Assets/Audio/ambient_background.mp3")
footsteps_sound = pygame.mixer.Sound("Assets/Audio/footsteps.mp3")
box_open_sound = pygame.mixer.Sound("Assets/Audio/box_open.mp3")
box_close_sound = pygame.mixer.Sound("Assets/Audio/box_close.mp3")
vent_open_sound = pygame.mixer.Sound("Assets/Audio/vent_open.mp3")
vent_close_sound = pygame.mixer.Sound("Assets/Audio/vent_close.mp3")
key_pickup_sound = pygame.mixer.Sound("Assets/Audio/key_pickup.mp3")
key_drop_sound = pygame.mixer.Sound("Assets/Audio/key_drop.mp3")
menu_btn_sounds = [pygame.mixer.Sound("Assets/Audio/menu_btn_1.mp3"), pygame.mixer.Sound("Assets/Audio/menu_btn_2.mp3")]

# Set volumes
pygame.mixer.music.set_volume(0.5)
footsteps_sound.set_volume(1)
box_open_sound.set_volume(0.1)
box_close_sound.set_volume(0.1)
vent_open_sound.set_volume(0.3)
vent_close_sound.set_volume(0.3)
key_pickup_sound.set_volume(0.3)
key_drop_sound.set_volume(0.5)

# Images

# Characters
player_idle_imgs = [pygame.image.load("Assets/Characters/Idle1.png"), pygame.image.load("Assets/Characters/Idle2.png"), pygame.image.load("Assets/Characters/Idle3.png"), pygame.image.load("Assets/Characters/Idle4.png")]
player_walk_imgs = [pygame.image.load("Assets/Characters/Walk1.png"), pygame.image.load("Assets/Characters/Walk2.png"), pygame.image.load("Assets/Characters/Walk3.png")]
security_idle_imgs = [pygame.image.load("Assets/Characters/sec_idle_0.png"), pygame.image.load("Assets/Characters/sec_idle_1.png"), pygame.image.load("Assets/Characters/sec_idle_2.png"), pygame.image.load("Assets/Characters/sec_idle_3.png")]
security_walk_imgs = [pygame.image.load("Assets/Characters/sec_walk_0.png"), pygame.image.load("Assets/Characters/sec_walk_1.png"), pygame.image.load("Assets/Characters/sec_walk_2.png")]
# Tiles
floor_img = pygame.image.load("Assets/Tiles/Floor.png") # 0 on the map
wall_img = pygame.image.load("Assets/Tiles/Wall.png") # 1 on the map
box_img = pygame.image.load("Assets/Tiles/Box.png") # 2 on the map
vent_img = pygame.image.load("Assets/Tiles/Vent.png") # 3 on the map
key_img = pygame.image.load("Assets/Tiles/Key.png") # 4 on the map
door_img = pygame.image.load("Assets/Tiles/door.png") # 5 on the map
# UI
key_inv_img = pygame.image.load("Assets/UI/Key_inv.png")
inv_slot_img = pygame.image.load("Assets/UI/inventory_slot.png")
inv_select_img = pygame.image.load("Assets/UI/Inv_Select.png")
main_menu_img = pygame.image.load("Assets/UI/main_menu_bg.png")
play_btn_img = pygame.image.load("Assets/UI/play_btn.png")
settings_gear_img = pygame.image.load("Assets/UI/settings_gear.png")
main_menu_img = pygame.transform.scale(main_menu_img, (screen_width, screen_height))
play_btn_img = pygame.transform.scale(play_btn_img, (200, 200))
settings_gear_img = pygame.transform.scale(settings_gear_img, (75, 75))

from item_type import ItemType

# Item Definitions
key_item = ItemType(name="Key", world_img=key_img, inv_img=key_inv_img)