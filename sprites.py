import pygame

from assets import (
    wall_img, floor_img, box_img, vent_img, key_img, door_img,
    player_idle_imgs, player_walk_imgs,
    footsteps_sound, box_open_sound, box_close_sound,
    vent_open_sound, vent_close_sound
)
from settings import game_map

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = key_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-2, -2)


class DroppedItem(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.image = self.item_type.world_img
        self.rect = self.image.get_rect(center=(x, y))

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = door_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-2, -2)

    def unlock(self):
        game_map[self.rect.y // 16][self.rect.x // 16] = 0
        self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-2, -2)

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = floor_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = box_img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-8, -4) # Shrink hitbox

class Vent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = vent_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.idle_frames = player_idle_imgs
        self.walk_frames = player_walk_imgs
        self.frames = self.idle_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.pos = pygame.math.Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.moving = False
        self.direction = 'right'
        self.speed = 85
        self.hidden = False
        self.hiding_spot = None
        self.footsteps_channel = pygame.mixer.Channel(0)
        self.box_channel = pygame.mixer.Channel(1)
        self.vent_channel = pygame.mixer.Channel(2)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            original_image = self.frames[self.current_frame]
            center = self.rect.center
            self.image = pygame.transform.flip(original_image, self.direction == 'left', False)
            self.rect = self.image.get_rect(center=center)
            if self.hidden:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)

    def hide(self, spot):
        self.hidden = True
        self.hiding_spot = spot
        self.pos = pygame.math.Vector2(spot.rect.center)
        self.rect.center = self.pos
        if isinstance(spot, Box):
            self.box_channel.play(box_open_sound)
        elif isinstance(spot, Vent):
            self.vent_channel.play(vent_open_sound)

    def unhide(self):
        if isinstance(self.hiding_spot, Box):
            self.box_channel.play(box_close_sound)
            # Find a valid floor tile to move to
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                check_x = self.hiding_spot.rect.centerx // 16 + dx
                check_y = self.hiding_spot.rect.centery // 16 + dy
                if 0 <= check_y < len(game_map) and 0 <= check_x < len(game_map[0]):
                    if game_map[check_y][check_x] == 0:
                        self.pos = pygame.math.Vector2(check_x * 16 + 8, check_y * 16 + 8)
                        break
        else: # It's a vent
            self.vent_channel.play(vent_close_sound)
            self.pos = pygame.math.Vector2(self.hiding_spot.rect.center)

        self.rect.center = self.pos
        self.hidden = False
        self.hiding_spot = None

    def update(self, dt, walls, boxes, doors):
        if self.hidden:
            self.animate(dt)
            return
        keys = pygame.key.get_pressed()
        
        vec = pygame.math.Vector2(0, 0)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vec.x = -1
            self.direction = 'left'
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vec.x = 1
            self.direction = 'right'
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vec.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vec.y = 1

        if vec.length() > 0:
            vec.normalize_ip()
            if not self.moving:
                self.footsteps_channel.play(footsteps_sound, -1)
            self.moving = True
        else:
            if self.moving:
                self.footsteps_channel.stop()
            self.moving = False

        # Horizontal movement and collision
        self.pos.x += vec.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        
        all_obstacles = walls.sprites() + boxes.sprites() + doors.sprites()
        for obstacle in all_obstacles:
            hitbox = getattr(obstacle, 'hitbox', obstacle.rect)
            if self.rect.colliderect(hitbox):
                if vec.x > 0:
                    self.rect.right = hitbox.left
                elif vec.x < 0:
                    self.rect.left = hitbox.right
        self.pos.x = self.rect.centerx

        # Vertical movement and collision
        self.pos.y += vec.y * self.speed * dt
        self.rect.centery = round(self.pos.y)

        for obstacle in all_obstacles:
            hitbox = getattr(obstacle, 'hitbox', obstacle.rect)
            if self.rect.colliderect(hitbox):
                if vec.y > 0:
                    self.rect.bottom = hitbox.top
                elif vec.y < 0:
                    self.rect.top = hitbox.bottom
        self.pos.y = self.rect.centery
        
        if self.moving:
            self.frames = self.walk_frames
        else:
            self.frames = self.idle_frames
        
        self.animate(dt)