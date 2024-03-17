import pygame

# initialize the pygame
pygame.init()

# set window size and name
screen_width, screen_height = 800, 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("UserName-蛇吃豆-UserID")

# draw snake
pygame.draw.rect(surface=screen, color=(255, 255, 255), rect=(400, 400, 20, 10))
pygame.display.update()
