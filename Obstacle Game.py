import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Hello Pygame")
clock = pygame.time.Clock()

# Sprite class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width, x, y, speed):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((167, 255, 100))
        self.image.set_colorkey((255, 100, 98))
        
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

        self.velocity_y = 0
        self.gravity = 0.15
        self.jumping = False

        self.direction = "right"
        
    # Move your player left, right, and jump
    def update(self):
        # Handle movement behavior using keyboard inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            for platform in platforms:
                if player.rect.colliderect(platform):
                    self.rect.left = platform.right

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            for platform in platforms:
                if player.rect.colliderect(platform):
                    self.rect.right = platform.left
            

        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity_y = -12
            self.jumping = True

        old_loc = self.rect.copy()

        # Gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # collision with the top and bottom of each platform
        for platform in platforms:
            if self.rect.colliderect(platform):

                if old_loc.bottom <= platform.top and self.velocity_y >= 0:
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.jumping = False

                elif old_loc.top >= platform.top and self.velocity_y < 0:
                    self.rect.top = platform.bottom
                    self.velocity_y = 0

    
        # collision with enemies or spikes
        for spike_list in spikes_set_precheckpoint:
            for spike in spike_list:
                if self.rect.colliderect(spike):
                    self.rect.center = (350, 633)

        for spike_list in spikes_set_postcheckpoint:
            for spike in spike_list:
                if self.rect.colliderect(spike):
                    self.rect.center = (2650, 633)

        for enemy in enemies_precheckpoint:
            if self.rect.colliderect(enemy):
                player.rect.center = (350, 633)

        for enemy in enemies_postcheckpoint:
            if self.rect.colliderect(enemy):
                player.rect.center = (2650, 633)

        if self.rect.colliderect(bullet):
            player.rect.center = (2650, 633)

        # Ground collision
        if self.rect.bottom >= 650:
            self.rect.bottom = 650
            self.velocity_y = 0
            self.jumping = False
                    
    def enemy1_move(self):
        if self.direction == "right":
            self.rect.x += self.speed

            if self.rect.x >= 850:
                self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed

            if self.rect.x <= 500:
                self.direction = "right"

    def enemy2_3_5_6_move(self):
        if self.direction == "right":
            self.rect.y -= self.speed
            if self == enemy2 or self == enemy5 or self == enemy6:
                if self.rect.y <= -50:
                    self.direction = "down"
            if self == enemy3:
                if self.rect.y <= -150:
                    self.direction = "down"
    
        if self.direction == "down":
            self.rect.y += self.speed
            if self == enemy5 or self == enemy6:
                if self.rect.y >= 633:
                    self.direction = "up"
            if self == enemy2:
                if self.rect.y >= 420:
                    self.direction = "up"

            if self == enemy3:
                if self.rect.y >= 320:
                    self.direction = "up"

        if self.direction == "up":
            self.rect.y -= self.speed
            
            if self == enemy2 or self == enemy5 or self == enemy6:
                if self.rect.y <= -50:
                    self.direction = "down"
            if self == enemy3:
                if self.rect.y <= -150:
                    self.direction = "down"

    def shoot(self):
        self.rect.x -= self.speed

        if self.rect.x <= 2850:
            self.rect.center = (3550, 480)

        

# Creating sprites, platforms, and enemies
player = Sprite((255, 0, 0), 33, 33, 350, 633, 5)
enemy1 = Sprite((255,165,0), 33, 33, 675, 333, 1)
enemy2 = Sprite((0,0,255), 33, 33, 1900, 420, 1)
enemy3 = Sprite((128,0,128), 33, 33, 2150, 320, 1)
enemy4 = Sprite((0,0,0), 33, 33, 3550, 483, 1)
enemy5 = Sprite((255, 0, 255), 33, 33, 4700, 633, 3)
enemy6 = Sprite((0,255,255), 33, 33, 4800, 633, 4)
bullet = Sprite((0,0,0), 5, 15, 3550, 483, 4)
enemies_precheckpoint = [enemy1, enemy2, enemy3]
enemies_postcheckpoint = [enemy4, enemy5, enemy6]
enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6]
ground = pygame.Rect(0, 650, 5000, 150)
check_point = pygame.Rect(2650, 450, 30, 200)
platform1 = pygame.Rect(500, 350, 350, 50)
platform2 = pygame.Rect(1200, -200, 500, 450)
platform3 = pygame.Rect(1650, 450, 350, 50)
platform4 = pygame.Rect(2050, 350, 350, 50)
platform5 = pygame.Rect(2850, 500, 800, 50)
platform6 = pygame.Rect(3700, -200, 800, 500)
platform7 = pygame.Rect(4100, 400, 400, 500)
finish_line = pygame.Rect(4950, -200, 800, 850)
platforms = [platform1, platform2, platform3, platform4, platform5, platform6, platform7]


spikes1 = []
x1 = 725
for i in range(6):
    spike = pygame.Rect(x1, ground.top - 30, 60, 30)
    spikes1.append(spike)
    x1 += 60

spikes2 = []
x2 = 1600
for i in range(15):
    spike = pygame.Rect(x2, ground.top - 30, 60, 30)
    spikes2.append(spike)
    x2 += 60

spikes3 = []
x3 = 2900
for i in range(11):
    spike = pygame.Rect(x3, ground.top - 30, 60, 30)
    spikes3.append(spike)
    x3 += 60

spikes_set = [spikes1, spikes2, spikes3]
spikes_set_precheckpoint = [spikes1, spikes2]
spikes_set_postcheckpoint = [spikes3]

camera_x = 0
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player in world coordinates
    player.update()
    enemy1.enemy1_move()
    enemy2.enemy2_3_5_6_move()
    enemy3.enemy2_3_5_6_move()
    enemy5.enemy2_3_5_6_move()
    enemy6.enemy2_3_5_6_move()
    bullet.shoot()

    # Camera tries to keep player centered
    target_camera_x = player.rect.centerx - screen.get_width() // 2

    # Smooth camera
    camera_x += (target_camera_x - camera_x) * 0.1

    # Camera boundaries
    max_camera_x = ground.width - screen.get_width()

    camera_x = max(0, camera_x)
    camera_x = min(camera_x, max_camera_x)

    # Complete Game
    if player.rect.colliderect(finish_line):
        print("Completed the game")
        running = False

    screen.fill((135, 206, 235))

    # Ground position on screen
    ground_rect = ground.copy()
    ground_rect.x -= int(camera_x)

    check_point_rect = check_point.copy()
    check_point_rect.x -= int(camera_x)

    for platform in platforms:
        platform_rect = platform.copy()
        platform_rect.x -= int(camera_x)
        pygame.draw.rect(screen, (0, 255, 0), platform_rect)


    # Player position on screen
    player_rect = player.rect.copy()
    player_rect.x -= int(camera_x)

    bullet_rect = bullet.rect.copy()
    bullet_rect.x -= int(camera_x)

    finish_line_rect = finish_line.copy()
    finish_line_rect.x -= int(camera_x)
    
    # Draw
    pygame.draw.rect(screen, (0, 255, 0), ground_rect)
    pygame.draw.rect(screen, (255, 255, 0), check_point_rect)
    pygame.draw.rect(screen, (135, 206, 235), finish_line_rect)

    for spike_list in spikes_set:
        for spike in spike_list:
            spike_set_screen = spike.copy()
            spike_set_screen.x -= int(camera_x)

            pygame.draw.polygon(screen, (0, 0, 0), [(spike_set_screen.left, spike_set_screen.bottom),(spike_set_screen.centerx, spike_set_screen.top),(spike_set_screen.right, spike_set_screen.bottom)])

    
    screen.blit(player.image, player_rect)
    screen.blit(bullet.image, bullet_rect)
    for enemy in enemies:
        enemy_rect = enemy.rect.copy()
        enemy_rect.x -= int(camera_x)
        screen.blit(enemy.image, enemy_rect)

    pygame.display.flip()

    clock.tick(500)