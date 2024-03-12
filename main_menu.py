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

# Initialize Pygame
pygame.init()

# Other Global Variables
menu_bg_image = pygame.image.load('nea_menu_background.jpg')
base_font = pygame.font.Font(None, 48)

# Sets the window size and displays it as a rectangluar window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Subroutines
def DrawText(text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    window.blit(img, (x, y))

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
