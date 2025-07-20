import pygame

pygame.mixer.init()

# Music and Sound
pygame.mixer.music.load("Assets/ambient_background.mp3")
footsteps_sound = pygame.mixer.Sound("Assets/footsteps.mp3")
box_open_sound = pygame.mixer.Sound("Assets/box_open.mp3")
box_close_sound = pygame.mixer.Sound("Assets/box_close.mp3")
vent_open_sound = pygame.mixer.Sound("Assets/vent_open.mp3")
vent_close_sound = pygame.mixer.Sound("Assets/vent_close.mp3")

# Set volumes
pygame.mixer.music.set_volume(0.1)
footsteps_sound.set_volume(1)
box_open_sound.set_volume(0.1)
box_close_sound.set_volume(0.1)
vent_open_sound.set_volume(0.3)
vent_close_sound.set_volume(0.3)

# Images
player_idle_imgs = [pygame.image.load("Assets/Idle1.png"), pygame.image.load("Assets/Idle2.png"), pygame.image.load("Assets/Idle3.png"), pygame.image.load("Assets/Idle4.png")]
player_walk_imgs = [pygame.image.load("Assets/Walk1.png"), pygame.image.load("Assets/Walk2.png"), pygame.image.load("Assets/Walk3.png")]
security_idle_imgs = [pygame.image.load("Assets/sec_idle_0.png"), pygame.image.load("Assets/sec_idle_1.png"), pygame.image.load("Assets/sec_idle_2.png"), pygame.image.load("Assets/sec_idle_3.png")]
security_walk_imgs = [pygame.image.load("Assets/sec_walk_0.png"), pygame.image.load("Assets/sec_walk_1.png"), pygame.image.load("Assets/sec_walk_2.png")]
floor_img = pygame.image.load("Assets/Floor.png") # 0 on the map
wall_img = pygame.image.load("Assets/Wall.png") # 1 on the map
box_img = pygame.image.load("Assets/Box.png") # 2 on the map
vent_img = pygame.image.load("Assets/Vent.png") # 3 on the map
key_img = pygame.image.load("Assets/Key.png") # 4 on the map

from inventory import ItemType

# Item Definitions
key_item = ItemType(name="Key", icon="Key.png")