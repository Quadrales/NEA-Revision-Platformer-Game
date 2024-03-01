# Modules
import pygame
import time
import sys
import os
import hashlib
#import sqlite3


# Subroutines
def DrawText(text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    window.blit(img, (x, y))

def LoginScreen():
    username_text = ""
    password_text = ""
    username_active = False
    password_active = False
    valid = False
    error_font = pygame.font.Font(None, 32)
    # Create 2 text boxes for the username and password to be entered into
    # and 2 boxes for the create account and login buttons
    username_input_rect = pygame.Rect(340, 280, 600, 80)
    password_input_rect = pygame.Rect(340, 420, 600, 80)
    create_account_rect = pygame.Rect(340, 550, 280, 80)
    login_rect = pygame.Rect(660, 550, 280, 80)

    while valid == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_input_rect.collidepoint(event.pos):
                    username_active = True
                    password_active = False
                elif password_input_rect.collidepoint(event.pos):
                    password_active = True
                    username_active = False
                elif create_account_rect.collidepoint(event.pos):
                    username = username_text
                    password = password_text
                    # Checks if the username and password are valid
                    valid_account = LoginValidation(username, password)
                    # Creates a new user with the current value of username and password
                    if valid_account == True:
                        CreateAccount(username, password)
                    username_text = ""
                    password_text = ""
                elif login_rect.collidepoint(event.pos):
                    username = username_text
                    password = password_text
                    # Checks if the username and password are in the users.txt file
                    valid_login = LoginCheck(username, password)
                    if valid_login == True:
                        return valid_login
                    else:
                        DrawText("Login not found. Please try again", error_font, (LAVENDER), 590, 600)
                        time.sleep(2.5)

                else:
                    username_active = False
                    password_active = False

            # Depending on which text box the user has selected, the outputted text
            # for that box will update with what the user types
            if event.type == pygame.KEYDOWN:
                if username_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        username_text = username_text[:-1]
                    else:
                        username_text += event.unicode
                elif password_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]
                    else:
                        password_text += event.unicode

        # Draw background
        window.blit(menu_bg_image, (0, 0))

        # Draw buttons using their respective rect variables
        pygame.draw.rect(window, DARK_GREY, username_input_rect, 4)
        pygame.draw.rect(window, DARK_GREY, password_input_rect, 4)
        pygame.draw.rect(window, DARK_GREY, login_rect, 4)
        pygame.draw.rect(window, DARK_GREY, create_account_rect, 4)

        # Check if mouse is hovering over each button and change color accordingly
        if username_input_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, username_input_rect, 4)
        if password_input_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, password_input_rect, 4)
        if login_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, login_rect, 4)
        if create_account_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, create_account_rect, 4)

        # Displays text saying "Username" and "Password" above their respective text boxes
        # and "Login" and "Create Account" inside their respective boxes
        DrawText("Username", base_font, (LIGHT_GREY), 340, 240)
        DrawText("Password", base_font, (LIGHT_GREY), 340, 380)
        DrawText("Create Account", base_font, (LIGHT_GREY), 355, 570)
        DrawText("Login", base_font, (LIGHT_GREY), 750, 570)

        # Outputs the user's inputted text into it's respective text box
        text_surface = base_font.render(username_text,True, LIGHT_GREY)
        window.blit(text_surface,(username_input_rect.x + 5, username_input_rect.y + 5))

        text_surface = base_font.render(password_text,True, LIGHT_GREY)
        window.blit(text_surface,(password_input_rect.x + 5, password_input_rect.y + 5))

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


def LoginValidation(username, password):
    valid_username = False
    valid_password = False
    valid_login = False
    uppercase_letters = 0
    numbers_or_symbols = 0

    # Loops until the user enters valid login information
    while valid_login == False:
        # Checks if the username is an appropriate length
        if len(username) > 2 and len(username) < 17:
            valid_username = True
        else:
            valid_username = False
            return valid_login

        # Checks if the password is an appropriate length
        if len(password) > 5 and len(password) < 17:
            # Counts how many uppercase letters are in the password
            for character in password:
                if character.isalpha() == True:
                    if character == character.upper():
                        uppercase_letters += 1
            # Checks if the password has at least 1 uppercase letter
            if uppercase_letters > 0:
                for character in password:
                    if character.isalpha() == False:
                        numbers_or_symbols += 1
                if numbers_or_symbols > 0:
                    valid_password = True

        if valid_username == True and valid_password == True:
            valid_login = True
            return valid_login
        else:
            valid_login = False
            return valid_login


def CreateAccount(username, password):
    users_file = open("users.txt", "a")
    user = username + ", " + password
    users_file.write(os.linesep)
    users_file.write(user)
    users_file.close()

def LoginCheck(username, password):
    valid_login = False
    user = username + ", " + password

    while valid_login == False:
        users_file = open("users.txt", "r")
        for line in users_file:
            line = line.rstrip()
            if line == user:
                valid_login = True
                return valid_login
        if valid_login == False:
            return valid_login

    users_file.close()

def HashPassword(password):
    # Read user login details from file
    with open("users.txt", "r") as file:
        lines = file.readlines()

    # Create a new file to store hashed passwords
    with open("hashed_users", "w") as hashed_file:
        for line in lines:
            username, password = line.strip().split(",")  # Assuming username and password are separated by comma
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            #hashed_file.write(f"{username},{hashed_password}\n")

            print("Passwords hashed and saved to 'hashed_users.txt'.")


def MainMenu():
    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button is clicked
                if start_button_rect.collidepoint(event.pos):
                    print("Start Game")
                    difficulty = DifficultySelect()
                    return difficulty
                elif settings_button_rect.collidepoint(event.pos):
                    print("Settings")
                # Add code to go to settings
                elif stats_button_rect.collidepoint(event.pos):
                    print("Player Statistics")
                # Add code to check player statistics
                elif leaderboard_button_rect.collidepoint(event.pos):
                    print("Player Leaderboard")
                # Add code to open player leaderboard
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw background
        window.blit(menu_bg_image, (0, 0))

        # Draw buttons and get their rects
        start_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 190, 250, 50), 4)
        settings_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 290, 250, 50), 4)
        stats_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 390, 250, 50), 4)
        leaderboard_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 490, 250, 50), 4)
        quit_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 590, 250, 50), 4)

        # Check if mouse is hovering over each button and change color accordingly
        if start_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, start_button_rect, 4)
        if settings_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, settings_button_rect, 4)
        if stats_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, stats_button_rect, 4)
        if leaderboard_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, leaderboard_button_rect, 4)
        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, quit_button_rect, 4)

        # Display text on buttons
        DrawText("Start Game", base_font, LIGHT_GREY, 540, 200)
        DrawText("Settings", base_font, LIGHT_GREY, 540, 300)
        DrawText("Statistics", base_font, LIGHT_GREY, 540, 400)
        DrawText("Leaderboard", base_font, LIGHT_GREY, 540, 500)
        DrawText("Quit Game", base_font, LIGHT_GREY, 540, 600)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


def DifficultySelect():
    difficulty = ""
    big_font = pygame.font.Font(None, 64)

    while True:
        # Draw background
        window.blit(menu_bg_image, (0, 0))

        # Draw difficulty buttons and get their rects
        easy_button_rect = pygame.draw.rect(window, DARK_GREY, (230, 290, 250, 50), 4)
        medium_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 290, 250, 50), 4)
        hard_button_rect = pygame.draw.rect(window, DARK_GREY, (830, 290, 250, 50), 4)

        # Draw text for the difficulty buttons
        DrawText("Easy", base_font, LIGHT_GREY, 240, 300)
        DrawText("Medium", base_font, LIGHT_GREY, 540, 300)
        DrawText("Hard", base_font, LIGHT_GREY, 840, 300)
        DrawText("Select Difficulty", big_font, LIGHT_GREY, 480, 150)

        if easy_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, easy_button_rect, 4)
        if medium_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, medium_button_rect, 4)
        if hard_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window, LIGHT_BLUE, hard_button_rect, 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    difficulty = "Easy"
                    print(difficulty)
                    return difficulty
                elif medium_button_rect.collidepoint(event.pos):
                    difficulty = "Medium"
                    print(difficulty)
                    return difficulty
                elif hard_button_rect.collidepoint(event.pos):
                    difficulty = "Hard"
                    print(difficulty)
                    return difficulty

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window, camera_x):
        pygame.draw.rect(window, PLATFORM_COLOUR, (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.direction = direction
        self.speed = 10  # Adjust bullet speed as needed
        self.damage = 10  # Adjust bullet damage as needed

    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def draw(self, window, camera_x):
        pygame.draw.rect(window, GREEN, (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))


class Gun:
    def __init__(self):
        self.damage = 10  # Adjust damage as needed
        self.bullets = []

    def shoot(self, player):
        if player.facing_right:
            bullet = Bullet(player.rect.x + player.rect.width, player.rect.y + player.rect.height / 2 - 2, "right")
        else:
            bullet = Bullet(player.rect.x, player.rect.y + player.rect.height / 2 - 2, "left")
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def draw_bullets(self, window, camera_x):
        for bullet in self.bullets:
            bullet.draw(window, camera_x)

class Sword:
    def __init__(self):
        self.damage = 20  # Adjust damage as needed

    def swing(self, player, enemies, window, camera_x):
        if player.facing_right:
            hitbox = pygame.Rect(player.rect.x + player.rect.width, player.rect.y + player.rect.height / 2 - 15, 100, 30)
        else:
            hitbox = pygame.Rect(player.rect.x - 100, player.rect.y + player.rect.height / 2 - 15, 100, 30)

        for enemy in enemies:
            if hitbox.colliderect(enemy.rect):
                enemy.take_damage(self.damage, enemies)
                print("sword attack")

        # Draw damage hitbox
        pygame.draw.rect(window, GREEN, (hitbox.x - camera_x, hitbox.y, hitbox.width, hitbox.height))  # Draw the hitbox as a green rectangle
        pygame.display.flip()  # Update display
        time.sleep(1)  # Display hitbox for 1 second

# Class for enemies
class Enemy:
    def __init__(self, x, y, width, height, speed, health=50):  # Adjust default health as needed
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.health = health

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

# Set up the main character
class Player:
    def __init__(self, x, y, width, height, health=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.x_speed = 0
        self.y_speed = 0
        self.jump_force = -12
        self.gravity = 0.55
        self.gun = Gun()
        self.sword = Sword()
        self.attacking = False  # Flag to track if the player is currently attacking
        self.facing_right = True  # Initially facing right

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    def move(self, keys):
        if keys[pygame.K_a]:
            self.x_speed = -5
            self.facing_right = False  # Set facing direction to left
        elif keys[pygame.K_d]:
            self.x_speed = 5
            self.facing_right = True  # Set facing direction to right
        else:
            self.x_speed = 0

    def jump(self):
        if self.on_surface():
            self.y_speed = self.jump_force

    def on_surface(self):
        if self.y_speed == 0:
            return True
        return False

    def apply_gravity(self):
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
        self.health -= damage

    def heal(self, amount):
        self.health += amount

    def is_alive(self):
        return self.health > 0

def GameplayLoop():
    # Player creation
    player = Player(50, 50, 50, 50)

    # Camera properties
    camera_x = 0
    camera_speed = 5

    # Create some platforms
    platforms = [
        Platform(50, 500, 200, 50),
        Platform(300, 400, 200, 50),
        Platform(500, 300, 200, 50),
        Platform(600, 500, 1500, 50),
        Platform(0, 0, 50, 1000)
    ]

    # Create enemies
    enemies = [
        Enemy(600, 450, 50, 50, 2),
        Enemy(800, 250, 50, 50, 1),
        Enemy(1000, 450, 50, 50, 3)
    ]

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Handle keyboard events
                player.attack(enemies, event.key, window, camera_x)  # Call attack method with window and camera_x parameters

        # Update player position
        player.update_position()
        
        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Check for player jump
        if keys[pygame.K_SPACE]:
            player.jump()

        # Apply gravity
        player.apply_gravity()

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
        elif player.x - camera_x < 100:
            camera_x -= camera_speed

        # Move enemies
        for enemy in enemies:
            enemy.move(player)        

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

        # Draw enemies
        for enemy in enemies:
            enemy.draw(window, camera_x)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


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
            #in_menu == True:

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
