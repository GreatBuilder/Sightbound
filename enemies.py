import pygame
from assets import security_idle_imgs, security_walk_imgs

class Security(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.idle_frames = security_idle_imgs
        self.walk_frames = security_walk_imgs
        self.frames = self.idle_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.pos = pygame.math.Vector2(x, y) # starting spawn position
        self.rect = self.image.get_rect(center=self.pos)
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.moving = False
        self.direction = 'right'
        self.speed = 85
        self.footsteps_channel = pygame.mixer.Channel(0) # change this to different footstep sounds later
    
    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            original_image = self.frames[self.current_frame]
            center = self.rect.center
            self.image = pygame.transform.flip(original_image, self.direction == 'left', False)
            self.rect = self.image.get_rect(center=center)
    
    def update(self, dt):
        self.animate(dt)