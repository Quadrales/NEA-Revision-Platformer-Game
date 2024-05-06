# Modules
import pygame
import time
import sys
import os
import hashlib
import random

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
GAME_TITLE_COLOUR = (29, 25, 91)

# Initialize Pygame
pygame.init()

# Other Global Variables
menu_bg_image = pygame.image.load('nea_menu_background.jpg')
base_font = pygame.font.Font(None, 48)
controls = ["j", "k"]

# Sets the window size and displays it as a rectangluar window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Subroutines
def DrawText(text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    window.blit(img, (x, y))

def MainMenu():
    big_font = pygame.font.Font(None, 80)
    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button is clicked
                if start_button_rect.collidepoint(event.pos):
                    difficulty = DifficultySelect()
                    return difficulty
                elif settings_button_rect.collidepoint(event.pos):
                    controls = Settings()
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw background
        window.blit(menu_bg_image, (0, 0))

        # Draw buttons and get their rects
        start_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 240, 250, 50), 4)
        settings_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 340, 250, 50), 4)
        quit_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 440, 250, 50), 4)

        # Check if mouse is hovering over each button and change color accordingly
        for rect in (start_button_rect, settings_button_rect, quit_button_rect):
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window, LIGHT_BLUE, rect, 4)

        # Display text on buttons and game title
        DrawText("Roguelike Revision Platformer", big_font, GAME_TITLE_COLOUR, 240, 80)
        DrawText("Start Game", base_font, LIGHT_GREY, 540, 250)
        DrawText("Settings", base_font, LIGHT_GREY, 540, 350)
        DrawText("Quit Game", base_font, LIGHT_GREY, 540, 450)

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
        DrawText("Normal", base_font, LIGHT_GREY, 540, 300)
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
                    difficulty = "Normal"
                    print(difficulty)
                    return difficulty
                elif hard_button_rect.collidepoint(event.pos):
                    difficulty = "Hard"
                    print(difficulty)
                    return difficulty

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def Settings():
    big_font = pygame.font.Font(None, 64)
    volume = 0.5

    while True:
        # Draw background
        window.blit(menu_bg_image, (0, 0))

        # Draw control buttons and get their rects
        shoot_rect = pygame.draw.rect(window, DARK_GREY, (300, 240, 250, 50), 4)
        sword_rect = pygame.draw.rect(window, DARK_GREY, (300, 340, 250, 50), 4)
        back_button_rect = pygame.draw.rect(window, DARK_GREY, (530, 10, 250, 50), 4)

        # Draw volume slider
        slider_rect = pygame.draw.rect(window, DARK_GREY, (780, 250, 250, 30))  # Slider background
        slider_handle_rect = pygame.Rect(780 + volume * 250 - 5, 250, 10, 30)  # Slider handle
        pygame.draw.rect(window, LAVENDER, slider_handle_rect)

        # Draw text for the control buttons
        DrawText("Controls", big_font, LIGHT_GREY, 300, 150)
        DrawText("Volume", big_font, LIGHT_GREY, 820, 150)
        DrawText("Shoot: " + controls[0], base_font, LIGHT_GREY, 310, 250)
        DrawText("Sword: " + controls[1], base_font, LIGHT_GREY, 310, 350)
        DrawText("Back", base_font, LIGHT_GREY, 540, 20)

        # Handle key presses for each control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Convert key to its corresponding character
                key_char = pygame.key.name(event.key)
                if shoot_rect.collidepoint(pygame.mouse.get_pos()):
                    controls[0] = key_char
                elif sword_rect.collidepoint(pygame.mouse.get_pos()):
                    controls[1] = key_char
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return controls
                elif slider_rect.collidepoint(event.pos):
                    # Check if the mouse click is within the slider area
                    # Update volume based on the mouse position
                    volume = (event.pos[0] - slider_rect.left) / slider_rect.width
                    # Set the music volume
                    pygame.mixer.music.set_volume(volume)

        # Update slider handle position
        slider_handle_rect.x = 300 + volume * 250 - 5

        # Highlight buttons when hovered
        for rect in (shoot_rect, sword_rect, back_button_rect):
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window, LIGHT_BLUE, rect, 4)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
