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
			hashed_file.write(f"{username},{hashed_password}\n")

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

# Function to load level from image file
def load_level_from_image(image_path):
        level_data = []

        # Load image
        level_image = pygame.image.load(image_path)
        level_image.convert()  # Convert image to display format for better performance

        # Get level dimensions
        level_width = level_image.get_width()
        level_height = level_image.get_height()

        # Parse image data
        for y in range(level_height):
                row_data = []
                for x in range(level_width):
                        pixel_color = level_image.get_at((x, y))
                        # Example: check if pixel color represents a platform (use RGB values)
                        if pixel_color == (0, 0, 0):  # Black color represents platform
                                row_data.append(True)  # Add platform element to row data
                        else:
                                row_data.append(False)  # Add empty space element to row data
                level_data.append(row_data)

        return level_data

# Function to render level elements
def render_level(window, level_data):
        # Example: render platforms based on level data
        for y, row in enumerate(level_data):
                for x, tile in enumerate(row):
                        if tile:  # If tile is True (platform)
                                pygame.draw.rect(window, (0, 0, 255), (x * 20, y * 20, 20, 20))  # Example: render blue platform


# Class for enemies and other entities
class Entity:
	pass


# Set up the main character
class Player:
	def __init__(self, x, y, width, height, health=100):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.health = health
		self.x_speed = 0
		self.y_speed = 0
		self.jump_force = -12
		self.gravity = 0.55

	def move(self, keys):
		if keys[pygame.K_a]:
			self.x_speed = -5
		elif keys[pygame.K_d]:
			self.x_speed = 5
		else:
			self.x_speed = 0

	def jump(self):
		if self.on_surface():  # Check if player is on any surface
			self.y_speed = self.jump_force

	def on_surface(self):
		# Check if player is on any surface or platform
		if self.y_speed == 0:
			return True
		return False

	def apply_gravity(self):
		self.y_speed += self.gravity

	def update_position(self):
		self.x += self.x_speed
		self.y += self.y_speed

	def draw(self, window, camera_x):
		pygame.draw.rect(window, (255, 0, 0), (self.x - camera_x, self.y, self.width, self.height))

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

	# Load level from image
        #level_data = load_level_from_image("level_image.png")

	# Platform properties
	platforms = [(20, 500, 200, 20), (300, 400, 200, 20), (500, 300, 200, 20), (600, 500, 1500, 20)]  # Example platform positions (x, y, width, height)

	# Main game loop
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

                # Render level elements
                #render_level(window, level_data)

		# Player movement
		keys = pygame.key.get_pressed()
		player.move(keys)

		# Check for player jump
		if keys[pygame.K_SPACE]:
			player.jump()

		# Apply gravity
		player.apply_gravity()

		# Update player position
		player.update_position()

		# Camera movement
		if player.x - camera_x > 500:
			camera_x += camera_speed
		elif player.x - camera_x < 100:
			camera_x -= camera_speed

		# Check for collisions with platforms
		for platform in platforms:
			platform_rect = pygame.Rect(platform[0] - camera_x, platform[1], platform[2], platform[3])
			player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
			if player_rect.colliderect(platform_rect):
				# Resolve collision (adjust player position)
				if player.y_speed > 0:
					player.y = platform[1] - player.height
					player.y_speed = 0
				elif player.y_speed < 0:
					player.y = platform[1] + platform[3]
					player.y_speed = 0

		# Draw background
		window.fill((255, 255, 255))  # White background

		# Draw platforms
		for platform in platforms:
			pygame.draw.rect(window, (0, 0, 255), (platform[0] - camera_x, platform[1], platform[2], platform[3]))  # Blue platforms

		# Draw player
		player.draw(window, camera_x)

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
GAME_BG = ()

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
	in_menu = False
	in_game = False

	# Main Game Loop
	while done == False:
		# Stops the game loop if user clicks the close button on the window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		while logged_in == False:
			logged_in = LoginScreen()
			in_menu = True

		if in_menu == True:
			MainMenu()


		GameplayLoop()


		pygame.display.flip()
		pygame.time.Clock().tick(FPS)

	# Closes the game if the game loop is no longer running
	pygame.quit()
	sys.exit()


Main()
