# Modules
import pygame
import sqlite3
import sys


# Subroutines
def DrawText(text, font, textCol, x, y, window):
	img = font.render(text, True, textCol)
	window.blit(img, (x, y))


def LoginScreen(window):
	base_font = pygame.font.Font(None,48)
	username_text = ""
	password_text = ""
	username_active = False
	password_active = False
	valid = False
	# Create 2 text boxes for the username and password to be entered into
	username_input_rect = pygame.Rect(340, 280, 600, 80)
	password_input_rect = pygame.Rect(340, 420, 600, 80)
	login_rect = pygame.Rect(490, 550, 300, 80)

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
				else:
					username_active = False
					password_active = False

			# Depending on which text box the user has selected, the outputted text
			# for that box will update with what the user types
			if event.type == pygame.KEYDOWN:
				if username_active == True:
					if event.key == pygame.K_BACKSPACE:
						username_text = username_text[:-1]
					elif event.key == pygame.K_RETURN:
						username = username_text
						password = password_text
						# Checks if the username and password are valid
						valid = LoginValidation(username, password)
						if valid == True:
							return username, password
					else:
						username_text += event.unicode
				elif password_active == True:
					if event.key == pygame.K_BACKSPACE:
						password_text = password_text[:-1]
					elif event.key == pygame.K_RETURN:
						username = username_text
						password = password_text
						# Checks if the username and password are valid
						valid = LoginValidation(username, password)
						if valid == True:
							return username, password
					else:
						password_text += event.unicode

		window.fill(LOGIN_BG)

		pygame.draw.rect(window, DARK_GREY, username_input_rect, 4)
		pygame.draw.rect(window, DARK_GREY, password_input_rect, 4)
		pygame.draw.rect(window, DARK_GREY, login_rect, 4)

		# Displays text saying "Username" and "Password" above their respective text boxes
		# and "Login" for the login box
		DrawText("Username", base_font, (LIGHT_GREY), 340, 240, window)
		DrawText("Password", base_font, (LIGHT_GREY), 340, 380, window)
		DrawText("Login", base_font, (LIGHT_GREY), 590, 570, window)

		# Outputs the user's inputted text into it's respective text box
		text_surface = base_font.render(username_text,True,(255,255,255))
		window.blit(text_surface,(username_input_rect.x + 5, username_input_rect.y + 5))

		text_surface = base_font.render(password_text,True,(255,255,255))
		window.blit(text_surface,(password_input_rect.x + 5, password_input_rect.y + 5))

		pygame.display.flip()
		pygame.time.Clock().tick(FPS)


def LoginValidation(username, password):
	#Connect to the database
	#conn = sqlite3.connect("users.db")
	#c = conn.cursor()
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


#def PlayerProperties(username, password):
	#player_width = 50
	#player_height = 50
	#player_x = WIDTH // 2 - player_width // 2
	#player_y = HEIGHT - player_height - 50
	#player_speed = 5
	#is_jumping = False

#class Player:
	#pass

class Entity:
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
LOGIN_BG = (26, 6, 124)
LIGHT_GREY = (10, 18, 58)
DARK_GREY = (0, 17, 39)

# Main Program
def main():
	# Initialize Pygame
	pygame.init()
	# Sets the window size and displays it as a rectangluar window
	window = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Revision Platformer Game")

	done = False

	# Main Game Loop
	while not done:
		# Stops the game loop if user clicks the close button on the window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		LoginScreen(window)

		pygame.display.flip()
		pygame.time.Clock().tick(FPS)

	# Closes the game if the game loop is no longer running
	pygame.quit()
	sys.exit()


main() 
