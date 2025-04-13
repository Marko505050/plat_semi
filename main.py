import pygame
from pygame import *

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Create window
win_height = 500
win_width = 700
window = display.set_mode((win_width, win_height))
window.fill((160, 160, 160))

# Play music
mixer.init()
mixer.music.load("undertale_087. Hopes and Dreams.mp3")
mixer.music.play()
gravity = 0.5
jump_strength = -10

# Player class
class Player():
    def __init__(self, player_image, player_x, player_y, player_speed):
        try:
            self.image = pygame.transform.scale(pygame.image.load(player_image), (48, 70))
        except pygame.error as e:
            print(f"Error loading player image: {e}")
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
        self.vel_y = 0
        self.on_ground = False
        self.is_climbing = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_d]:
            self.rect.x += self.speed  # Move right
        if keys[K_a]:
            self.rect.x -= self.speed  # Move left
        if keys[K_SPACE] and not self.is_climbing:
            self.jump()

        # Climb up/down if on ladder and using the up/down keys
        if self.is_climbing:
            if keys[K_w]:
                self.rect.y -= self.speed  # Move up
            if keys[K_s]:
                self.rect.y += self.speed  # Move down

    def move(self, platforms):
        self.vel_y += gravity  # Apply gravity
        self.rect.y += self.vel_y  # Update vertical position

        self.on_ground = False  # Assume player is not on the ground
        
        for platform in platforms:
            # Check if the player is falling and collides with the platform
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top  # Position player on top of the platform
                self.vel_y = 0  # Stop downward velocity
                self.on_ground = True  # The player is on the ground/platform
                break  # No need to check other platforms if already grounded

    def jump(self):
        if self.on_ground:
            self.vel_y = jump_strength

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_collide(self, obj):
        return self.rect.colliderect(obj.rect)

# Initialize player
step = 4
player = Player("sr21ef1d1d5a747-removebg-preview.png", 100, 370, step)

# Spikes class
class Spikes():
    def __init__(self, image, x, y):
        try:
            self.image = pygame.transform.scale(pygame.image.load(image), (75, 40))
        except pygame.error as e:
            print(f"Error loading spikes image: {e}")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_collide(self, sprite):
        return self.rect.colliderect(sprite.rect)

# Initialize spikes
spikes_list = [
    Spikes("png-klev-club-vayd-p-shipi-dlya-igri-png-2-removebg-preview.png", 255, 185),
    Spikes("png-klev-club-vayd-p-shipi-dlya-igri-png-2-removebg-preview.png", 300, 420),
    Spikes("png-klev-club-vayd-p-shipi-dlya-igri-png-2-removebg-preview.png", 00, 420)
]

# Ladder class
class Ladder():
    def __init__(self, image, x, y):
        try:
            self.image = pygame.transform.scale(pygame.image.load(image), (80, 210))
        except pygame.error as e:
            print(f"Error loading ladder image: {e}")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Initialize ladder
ladder = Ladder("Знімок_екрана_2025-03-16_103930-removebg-preview.png", 600, 245)

# Portal class
class Portal():
    def __init__(self, image, x, y):
        try:
            self.image = pygame.transform.scale(pygame.image.load(image), (35, 35))
        except pygame.error as e:
            print(f"Error loading portal image: {e}")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Initialize portal
portal = Portal("3113939-middle-removebg-preview.png", 500, 300)

# Platform class
class Platform():
    def __init__(self, image, x, y):
        try:
            self.image = pygame.transform.scale(pygame.image.load(image), (150, 75))
        except pygame.error as e:
            print(f"Error loading platform image: {e}")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Initialize platforms (2 lines of platforms)
platforms = []
x = -100
for i in range(7):
    platform = Platform("xfhf.png", x + i * 132, 450)  # Top row
    platforms.append(platform)

# Second row of platforms at a lower height (y = 210)
for i in range(7):
    platform = Platform("xfhf.png", x + i * 320, 210)  # Bottom row
    platforms.append(platform)

# Game loop
game = True
finish = False

while game:
    for e in pygame.event.get():
        if e.type == QUIT:
            game = False
    
    # Fill window with background color before drawing
    window.fill((160, 160, 160))

    # Update player movement
    player.update()

    # Move player with gravity and collision checks
    player.move(platforms)  # Pass the list of platforms here

    # Check ladder collision
    if player.is_collide(ladder):  # Corrected typo here from `is_colide` to `is_collide`
        player.rect.x = 615  # Set player position to ladder position
        player.rect.y = 200  # Set player position to ladder position
        player.is_climbing = True  # Enable climbing when the player is on the ladder
    else:
        player.is_climbing = False  # Disable climbing when not on the ladder

    # Draw all elements
    player.draw(window)
    
    # Draw spikes
    for spike in spikes_list:
        window.blit(spike.image, spike.rect)
    
    window.blit(ladder.image, ladder.rect)
    window.blit(portal.image, portal.rect)
    
    # Draw platforms
    for platform in platforms:
        window.blit(platform.image, platform.rect)

    # Check collision with spikes
    for spike in spikes_list:
        if spike.is_collide(player):
            print("Player hit spikes!")
            # Reset player position or restart the level
            player.rect.x = 100
            player.rect.y = 370  # Reset to initial position

    # Update display
    pygame.display.update()
    clock.tick(60)

# Quit Pygame
pygame.quit()