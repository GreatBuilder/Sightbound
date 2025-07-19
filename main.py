import pygame

# pygame setup
pygame.init()
pygame.mixer.init()
screen_width = 850
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
display = pygame.Surface((256, 256))
clock = pygame.time.Clock()
running = True
dt = 0

# Version
VERSION = "0.0.1 Initial version"
SHOW_VERSION = True

# Music and Sound
pygame.mixer.music.load("Assets/ambient_background.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
footsteps_sound = pygame.mixer.Sound("Assets/footsteps.mp3")
footsteps_sound.set_volume(1)
box_open_sound = pygame.mixer.Sound("Assets/box_open.mp3")
box_open_sound.set_volume(0.1)
box_close_sound = pygame.mixer.Sound("Assets/box_close.mp3")
box_close_sound.set_volume(0.1)
vent_open_sound = pygame.mixer.Sound("Assets/vent_open.mp3")
vent_open_sound.set_volume(0.3)
vent_close_sound = pygame.mixer.Sound("Assets/vent_close.mp3")
vent_close_sound.set_volume(0.3)

# Images
player_idle_imgs = [pygame.image.load("Assets/Idle1.png"), pygame.image.load("Assets/Idle2.png"), pygame.image.load("Assets/Idle3.png"), pygame.image.load("Assets/Idle4.png")]
player_walk_imgs = [pygame.image.load("Assets/Walk1.png"), pygame.image.load("Assets/Walk2.png"), pygame.image.load("Assets/Walk3.png")]
security_idle_imgs = [pygame.image.load("Assets/sec_idle_0.png"), pygame.image.load("Assets/sec_idle_1.png"), pygame.image.load("Assets/sec_idle_2.png"), pygame.image.load("Assets/sec_idle_3.png")]
security_walk_imgs = [pygame.image.load("Assets/sec_walk_0.png"), pygame.image.load("Assets/sec_walk_1.png"), pygame.image.load("Assets/sec_walk_2.png")]
floor_img = pygame.image.load("Assets/Floor.png")
wall_img = pygame.image.load("Assets/Wall.png")
box_img = pygame.image.load("Assets/Box.png")
vent_img = pygame.image.load("Assets/Vent.png")

game_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 3, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 3, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 2, 0, 3, 0, 2, 0, 3, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

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

    def update(self, dt, walls, boxes):
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
        
        all_obstacles = walls.sprites() + boxes.sprites()
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