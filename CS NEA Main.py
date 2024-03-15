# Modules
import pygame
import time
import sys
import os
import hashlib
import random
#import sqlite3

from login_system import LoginScreen
from main_menu import MainMenu


# Subroutines
def DrawText(text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    window.blit(img, (x, y))

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window, camera_x):
        pygame.draw.rect(window, PLATFORM_COLOUR, (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

class Bullet:
    def __init__(self, x, y, width, height, direction, damage):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction
        self.speed = 12
        self.damage = damage

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def draw(self, window, camera_x):
        pygame.draw.rect(window, GREEN, (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

class Gun:
    def __init__(self):
        self.bullets = []
        self.last_shot_time = 0
        self.cooldown = 0.25 # Cooldown time in seconds
        self.bullet_damage = 8  # Default bullet damage

    def shoot(self, player):
        current_time = time.time()
        if current_time - self.last_shot_time > self.cooldown:
            if player.facing_right:
                bullet = Bullet(player.rect.x + player.rect.width - 16, player.rect.y + player.rect.height / 2 - 2, 16, 8, "right", self.bullet_damage)
            else:
                bullet = Bullet(player.rect.x, player.rect.y + player.rect.height / 2 - 2, 16, 8, "left", self.bullet_damage)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def draw_bullets(self, window, camera_x):
        for bullet in self.bullets:
            bullet.draw(window, camera_x)

    def apply_damage_upgrade(self):
        self.bullet_damage *= 1.1
        # Update the damage of all bullets
        for bullet in self.bullets:
            bullet.damage = self.bullet_damage

    def apply_attack_upgrade(self, attack_speed):
        self.cooldown *= attack_speed

class Sword:
    def __init__(self):
        self.damage = 20
        self.last_swing_time = 0
        self.cooldown = 0.8 # Cooldown time in seconds

    def swing(self, player, enemies, window, camera_x):
        current_time = time.time()
        if current_time - self.last_swing_time > self.cooldown:
            # Creates hitboxes for facing right or left
            if player.facing_right:
                hitbox = pygame.Rect(player.rect.x + player.rect.width - 10, player.rect.y + player.rect.height / 2 - 15, 100, 30)
            else:
                hitbox = pygame.Rect(player.rect.x - (2 * player.rect.width) + 10, player.rect.y + player.rect.height / 2 - 15, 100, 30)
            # Creates hitboxes for facing up or down
            if player.facing_up:
                hitbox = pygame.Rect(player.rect.x + 10, player.rect.y - (2 * player.rect.height) + 10, 30, 100)
            elif player.facing_down:
                hitbox = pygame.Rect(player.rect.x + 10, player.rect.y + player.rect.height - 10, 30, 100)
            # Checks if an enemy collides with the hitbox and if so, damages the enemy
            for enemy in enemies:
                if hitbox.colliderect(enemy.rect):
                    enemy.take_damage(self.damage, enemies)
                    self.last_swing_time = current_time
                    print("sword attack")

            # Draw damage hitbox
            pygame.draw.rect(window, GREEN, (hitbox.x - camera_x, hitbox.y, hitbox.width, hitbox.height))  # Draw the hitbox as a green rectangle
            pygame.display.flip()
            #time.sleep(1)

    def apply_damage_upgrade(self):
        self.damage *= 1.1

    def apply_attack_upgrade(self, attack_speed):
        self.cooldown *= attack_speed

# Class for enemies
class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        if enemy_type == 1:
            self.width = 50
            self.height = 40
            self.speed = 2.5
            self.health = 45
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        elif enemy_type == 2:
            self.width = 30
            self.height = 80
            self.speed = 2.1
            self.health = 75
            self.rect = pygame.Rect(self.x, self.y-40, self.width, self.height)
        else:
            self.width = 80
            self.height = 90
            self.speed = 1.7
            self.health = 120
            self.rect = pygame.Rect(self.x, self.y-50, self.width, self.height)

    def move(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

    def draw(self, window, camera_x):
        pygame.draw.rect(window, (230, 60, 60), (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

    def take_damage(self, damage, enemies):
        self.health -= damage
        if self.health <= 0:
            enemies.remove(self)
            if random.randint(1, 3) == 1:
                # Create an upgrade box
                if self.enemy_type == 1:
                    upgrade_box = UpgradeBox(self.rect.x, self.rect.y-10)
                elif self.enemy_type == 2:
                    upgrade_box = UpgradeBox(self.rect.x, self.rect.y+30)
                else:
                    upgrade_box = UpgradeBox(self.rect.x, self.rect.y+40)
                upgrade_boxes.append(upgrade_box)

class ProjectileBullet(Bullet):
    def __init__(self, x, y, width, height, direction, damage):
        super().__init__(x, y, width, height, direction, damage)
        self.initial_x = x
        self.range = 500  # Set the range for the projectile

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        # Check if the bullet has reached its range
        if abs(self.rect.x - self.initial_x) >= self.range:
            self.destroy()  # Remove the bullet if it exceeds the range

    def destroy(self):
        if self in self.boss.bullets:
            self.boss.bullets.remove(self)

class Boss:
    def __init__(self, x, y, boss_type):
        self.x = x
        self.y = y
        self.boss_type = boss_type
        if boss_type == 1:
            self.width = 100
            self.height = 80
            self.speed = 2.8
            self.health = 45
            self.rect = pygame.Rect(self.x, self.y+20, self.width, self.height)
        elif boss_type == 2:
            self.width = 60
            self.height = 160
            self.speed = 2.2
            self.health = 75
            self.rect = pygame.Rect(self.x, self.y+40, self.width, self.height)
        else:
            self.width = 160
            self.height = 180
            self.speed = 1.7
            self.health = 120
            self.rect = pygame.Rect(self.x, self.y-80, self.width, self.height)
        self.bullets = []
        self.last_attack_time = 0
        self.min_attack_interval = 2.0  # Minimum time interval between attacks
        self.max_attack_interval = 5.0  # Maximum time interval between attacks
        self.attack_interval = random.uniform(self.min_attack_interval, self.max_attack_interval)
        self.attack_range = 400  # Range within which the boss will start attacking
        self.last_movement_time = 0
        self.move_duration = random.uniform(1.5, 2.5)  # Duration for random movement
        self.move_end_time = 0  # Time when the current movement should end

    def move(self, player):
        current_time = time.time()
        # Check if the current time is within the movement duration
        if current_time < self.move_end_time:
            # Randomly choose a direction to move
            movement_direction = random.choice(["left", "right"])
            # Move towards the player if within attack range
            if abs(player.rect.centerx - self.rect.centerx) <= self.attack_range:
                if player.rect.centerx < self.rect.centerx:
                    movement_direction = "left"
                else:
                    movement_direction = "right"
            # Update boss position based on movement direction
            if movement_direction == "left":
                self.rect.x -= self.speed
            elif movement_direction == "right":
                self.rect.x += self.speed
        else:
            # Generate new end time for the next movement
            self.move_end_time = current_time + self.move_duration

    def draw(self, window, camera_x):
        pygame.draw.rect(window, (230, 60, 60), (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

    def take_damage(self, damage, enemies):
        self.health -= damage
        if self.health <= 0:
            enemies.remove(self)
            # Create an upgrade box
            if self.boss_type == 1:
                upgrade_box = UpgradeBox(self.rect.x, self.rect.y-20)
            elif self.boss_type == 2:
                upgrade_box = UpgradeBox(self.rect.x, self.rect.y+60)
            else:
                upgrade_box = UpgradeBox(self.rect.x, self.rect.y+80)
            upgrade_boxes.append(upgrade_box)

    def attack(self, player, camera_x):
        current_time = time.time()
        if current_time - self.last_attack_time > self.attack_interval:
            if self.boss_type == 1:
                self.attack_type1(player, camera_x)
            elif self.boss_type == 2:
                self.attack_type2(player)
            else:
                self.attack_type3(player)
            self.last_attack_time = current_time
            # Update the attack interval for the next attack
            self.attack_interval = random.uniform(self.min_attack_interval, self.max_attack_interval)

    def attack_type1(self, player, camera_x):
        # Sword slash attack
        # Create hitbox for the sword slash
        if self.rect.right < player.rect.left:
            # Boss is to the left of the player
            hitbox = pygame.Rect(self.rect.right, self.rect.centery - 15, 100, 30)
        else:
            # Boss is to the right of the player
            hitbox = pygame.Rect(self.rect.left - 100, self.rect.centery - 15, 100, 30)
        
        # Check if player collides with the hitbox and if so, damages the player
        if hitbox.colliderect(player.rect):
            player.take_damage(random.randint(18, 23))
        
        # Draw the hitbox
        pygame.draw.rect(window, GREEN, (hitbox.x - camera_x, hitbox.y, hitbox.width, hitbox.height))

    def attack_type2(self, player):
        # Large gun blast attack
        # Create projectile bullet and add it to the boss's bullets list
        if self.boss_type == 1:
            bullet = ProjectileBullet(self.rect.x, self.rect.y + self.rect.height / 2 - 4, 64, 32, "right", 15)
        elif self.boss_type == 2:
            bullet = ProjectileBullet(self.rect.x, self.rect.y + self.rect.height / 2 - 4, 64, 32, "left", 15)
        else:
            bullet = ProjectileBullet(self.rect.x, self.rect.y + self.rect.height / 2 - 4, 64, 32, "right", 15)
        bullet.boss = self  # Assign the boss object to the bullet
        self.bullets.append(bullet)

    def attack_type3(self, player):
        # Charging attack
        # Check if player collides with the boss and if so, damages the player
        if self.rect.colliderect(player.rect):
            player.take_damage(random.randint(24, 28))

class UpgradeBox:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)  # Adjust the size as needed
        self.color = (255, 215, 0)  # Gold color

    def draw(self, window, camera_x):
        pygame.draw.rect(window, self.color, (self.rect.x - camera_x, self.rect.y+20, self.rect.width, self.rect.height))


# Set up the main character
class Player:
    def __init__(self, x, y, width, height, health=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.x_speed = 0
        self.y_speed = 0
        self.jump_force = -12
        self.gravity = 0.55
        self.attack_speed = 1
        self.damage_resistance = 0
        self.attacking = False  # Flag to track if the player is currently attacking
        self.last_damage_time = 0
        self.damage_cooldown = 1.5  # Cooldown time in seconds
        self.facing_right = True  # Initially facing right
        self.facing_up = False
        self.facing_down = False
        self.gun = Gun()
        self.sword = Sword()
        self.dashing = False
        self.last_dash_time = 0
        self.dash_duration = 0.2
        self.dash_cooldown = 1
        self.can_dash = True

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    def move(self, keys):
        if self.dashing == False:
            if keys[pygame.K_a]:
                self.x_speed = -5
                self.facing_right = False  # Set facing direction to left
            elif keys[pygame.K_d]:
                self.x_speed = 5
                self.facing_right = True  # Set facing direction to right
            else:
                self.x_speed = 0
        # Checks if player is also facing up or down
        if keys[pygame.K_w]:
            self.facing_up = True
            self.facing_down = False
        elif keys[pygame.K_s]:
            self.facing_down = True
            self.facing_up = False
        else:
            self.facing_up = False
            self.facing_down = False
        # Checks if player presses the dash button
        if keys[pygame.K_LSHIFT] and self.can_dash == True:
            self.dashing = True
            self.last_dash_time = time.time()
            self.can_dash = False

    def dash(self):
        current_time = time.time()
        if self.dashing == True:
            if current_time - self.last_dash_time <= self.dash_duration:
                self.y_speed = 0
                if self.facing_right == True:
                    self.x_speed = 22
                else:
                    self.x_speed = -22
                return self.x_speed
            else:
                self.dashing = False
        elif current_time - self.last_dash_time > self.dash_cooldown:
            self.dashing = False
            self.can_dash = True

    def jump(self):
        if self.dashing == False:
            if self.on_surface():
                self.y_speed = self.jump_force

    def on_surface(self):
        if self.y_speed == 0:
            return True
        return False

    def apply_gravity(self):
        if self.dashing == False:
            self.y_speed += self.gravity

    def update_position(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def draw(self, window, camera_x):
        pygame.draw.rect(window, (60, 100, 230), (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

    def attack(self, enemies, key, window, camera_x):
        if key == pygame.K_j:  # Gun attack
            if not self.attacking:
                self.gun.shoot(self)
                self.attacking = True
        elif key == pygame.K_k:  # Sword attack
            if not self.attacking:
                self.sword.swing(self, enemies, window, camera_x)
                self.attacking = True

    def take_damage(self, damage):
        self.speed_modifier = 1
        current_time = time.time()
        if current_time - self.last_damage_time > self.damage_cooldown:
            if damage > 0:
                self.health -= damage
                self.speed_modifier = 0.7
                self.last_damage_time = current_time
            else:
                self.health -= 1
                self.speed_modifier = 0.7
                self.last_damage_time = current_time

    def apply_upgrade(self, upgrade):
        # Apply the selected upgrade
        if upgrade == "weapon damage":
            self.sword.apply_damage_upgrade()
            self.gun.apply_damage_upgrade()
        elif upgrade == "damage resistance":
            self.damage_resistance += 2
        elif upgrade == "attack speed":
            self.attack_speed *= 0.9
            self.sword.apply_attack_upgrade(self.attack_speed)
            self.gun.apply_attack_upgrade(self.attack_speed)

    def heal(self, amount):
        self.health += amount

    def is_alive(self):
        return self.health > 0

def HandleUpgrade():
    upgrade = ""
    big_font = pygame.font.Font(None, 64)

    while True:
        # Draw difficulty buttons and get their rects
        upgrade1_rect = pygame.draw.rect(window, DARK_GREY, (440, 280, 400, 70), 4)
        upgrade2_rect = pygame.draw.rect(window, DARK_GREY, (440, 430, 400, 70), 4)
        upgrade3_rect = pygame.draw.rect(window, DARK_GREY, (440, 580, 400, 70), 4)

        # Draw text for the upgrade buttons
        DrawText("Weapon Damage +10%", base_font, LIGHT_GREY, 450, 300)
        DrawText("Damage Resistance +2", base_font, LIGHT_GREY, 450, 450)
        DrawText("Attack Speed +10%", base_font, LIGHT_GREY, 450, 600)
        DrawText("Select Upgrade", big_font, LIGHT_GREY, 480, 150)

        if upgrade1_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, upgrade1_rect, 4)
        if upgrade2_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, upgrade2_rect, 4)
        if upgrade3_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, upgrade3_rect, 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if upgrade1_rect.collidepoint(event.pos):
                    upgrade = "weapon damage"
                    print(upgrade)
                    return upgrade
                elif upgrade2_rect.collidepoint(event.pos):
                    upgrade = "damage resistance"
                    print(upgrade)
                    return upgrade
                elif upgrade3_rect.collidepoint(event.pos):
                    upgrade = "attack speed"
                    print(upgrade)
                    return upgrade

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def GameplayLoop():
    # Player creation
    player = Player(500, 50, 50, 50)

    # Camera properties
    camera_x = 0
    camera_speed = 5

    current_time = time.time()

    # Load platforms from file
    platforms = []
    with open('level_1_platforms.txt', 'r') as f:
        for line in f:
            coords = line.strip().split(',')
            platforms.append(Platform(int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])))

    # Load enemies from file
    enemies = []
    '''
    with open('level_1_enemies.txt', 'r') as f:
        for line in f:
            coords = line.strip().split(',')
            enemies.append(Enemy(int(coords[0]), int(coords[1]), int(coords[2])))
            '''

    # Create boss instances
    bosses = []
    boss1 = Boss(700, 400, 1)
    boss2 = Boss(1000, 300, 2)
    boss3 = Boss(1300, 400, 3)
    bosses.extend([boss1, boss2, boss3])

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Handle keyboard events
                player.attack(enemies, event.key, window, camera_x)  # Call attack method with window and camera_x parameters
                # Check if the player pressed 'e' to interact with upgrade boxes
                if event.key == pygame.K_e:
                    for upgrade_box in upgrade_boxes:
                        if player.rect.colliderect(upgrade_box.rect):
                            upgrade = HandleUpgrade()
                            player.apply_upgrade(upgrade)
                            upgrade_boxes.remove(upgrade_box)  # Remove the upgrade box after interaction

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Check for player jump
        if keys[pygame.K_SPACE]:
            player.jump()

        # Check for player dash
        dash_speed = player.dash()
        if dash_speed == 22 or dash_speed == -22:
            camera_speed = 22
        else:
            camera_speed = 5

        # Apply gravity
        player.apply_gravity()

        # Continuous shooting while 'j' is held down
        if keys[pygame.K_j]:
            player.gun.shoot(player)

        # Reset attack flag when attack animation ends
        if not any(keys[key] for key in (pygame.K_j, pygame.K_k)):
            player.attacking = False

        # Update bullets
        player.gun.update_bullets()

        # Check for bullet-enemy collisions
        for bullet in player.gun.bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(bullet.damage, enemies)
                    player.gun.bullets.remove(bullet)
                    break  # Exit inner loop once bullet hits enemy

        # Camera movement
        if player.x - camera_x > 500:
            camera_x += camera_speed
        elif player.x - camera_x < 500:
            camera_x -= camera_speed

        # Move enemies
        for enemy in enemies:
            enemy.move(player)

        # Player and enemy collision detection
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                player.take_damage(10 - player.damage_resistance)  # Player takes 10 damage upon collision with an enemy

        # Move bosses
        for boss in bosses:
            boss.move(player)
            boss.attack(player, camera_x)

        # Player and boss collision detection
        for boss in bosses:
            if player.rect.colliderect(boss.rect):
                player.take_damage(15 - player.damage_resistance)  # Player takes 10 damage upon collision with an enemy

        # Update projectile bullets
        for boss in bosses:
            for bullet in boss.bullets:
                bullet.update()

        # Check for collision between projectile bullets and player
        for boss in bosses:
            for bullet in boss.bullets:
                if bullet.rect.colliderect(player.rect):
                    player.take_damage(bullet.damage)
                    bullet.destroy()         

        # Check for collision with platforms
        for platform in platforms:
            if player.rect.colliderect(platform.rect) and player.rect.left != platform.rect.right and player.rect.right != platform.rect.left:
                # Collision on the y-axis
                if player.y_speed > 0:
                    player.rect.bottom = platform.rect.top
                    player.y_speed = 0  # Stop falling
                elif player.y_speed < 0:
                    player.rect.top = platform.rect.bottom
                    player.y_speed = 0  # Stop jumping
            # Collision on the x-axis
            elif ((player.rect.left == platform.rect.right and keys[pygame.K_d] == False) or (player.rect.right == platform.rect.left and keys[pygame.K_a] == False)) and (player.y > platform.rect.top - 50 and player.y < platform.rect.bottom):
                player.x_speed = 0

        # Draw background
        window.fill(GAME_BG)

        # Draw platforms
        for platform in platforms:
            platform.draw(window, camera_x)

        # Draw player
        player.draw(window, camera_x)

        # Draw bullets
        player.gun.draw_bullets(window, camera_x)

        # Update player position
        player.update_position()

        # Draw enemies
        for enemy in enemies:
            enemy.draw(window, camera_x)

        # Draw bosses
        for boss in bosses:
            boss.draw(window, camera_x)

        # Draw projectile bullets
        for boss in bosses:
            for bullet in boss.bullets:
                bullet.draw(window, camera_x)

        # Draw upgrade boxes
        for upgrade_box in upgrade_boxes:
            upgrade_box.draw(window, camera_x)

        # Check player health
        if player.health <= 0:
            option = GameOver()
            if option == "menu":
                return
            elif option == "game stats":
                # ViewGameStats()
                return

        print(player.health)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


def GameOver():
    big_font = pygame.font.Font(None, 64)

    while True:
        # Draw option buttons and get their rects
        menu_button_rect = pygame.draw.rect(window, DARK_GREY, (440, 280, 400, 70), 4)
        game_stats_button_rect = pygame.draw.rect(window, DARK_GREY, (440, 430, 400, 70), 4)

        # Draw text for the option buttons
        DrawText("Game Over", big_font, RED, 510, 150)
        DrawText("Back To Menu", base_font, LIGHT_GREY, 450, 300)
        DrawText("View Game Stats", base_font, LIGHT_GREY, 450, 450)

        if menu_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, menu_button_rect, 4)
        if game_stats_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, game_stats_button_rect, 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(event.pos):
                    option = "menu"
                    print(option)
                    return option
                elif game_stats_button_rect.collidepoint(event.pos):
                    option = "game stats"
                    print(option)
                    return option

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


def ViewGameStats():
    pass


# Constants
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Basic Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Custom Colours
MENU_BG = (113, 72, 181)
LIGHT_GREY = (10, 18, 58)
DARK_GREY = (0, 17, 39)
LAVENDER = (136, 148, 255)
LIGHT_BLUE = (99, 155, 201)
GAME_BG = (187, 159, 255)
PLATFORM_COLOUR = (126, 132, 247)
WALL_COLOUR = (200, 200, 200)

# Initialize Pygame
pygame.init()

# Other Global Variables
menu_bg_image = pygame.image.load('nea_menu_background.jpg')
base_font = pygame.font.Font(None, 48)
upgrade_boxes = []

# Sets the window size and displays it as a rectangluar window
window = pygame.display.set_mode((WIDTH, HEIGHT))


# Main Program
def Main():
    pygame.display.set_caption("Revision Platformer Game")

    done = False
    logged_in = False
    in_menu = True
    in_game = False

    # Main Game Loop
    while done == False:
        # Stops the game loop if user clicks the close button on the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #while logged_in == False:
            #logged_in = LoginScreen()
            #in_menu = True

        while in_menu == True:
            MainMenu()
            in_menu = False
            in_game = True

        while in_game == True:
            GameplayLoop()
            in_game = False
            in_menu = True

    # Close Pygame
    pygame.quit()


# Run the main program
if __name__ == "__main__":
    Main()
