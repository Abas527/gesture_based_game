import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from subway import run_game
import pygame
from opencv.fist_based_gesture import create_conn
from opencv.conn import shared
import time

def main():

    pygame.init()

    WIDTH, HEIGHT = 800, 600
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    is_start=False
    running=True
    font = pygame.font.SysFont(None, 40)
    BLUE = (50, 50, 255)
    BLACK=(0,0,0)
    BROWN = (139, 69, 19)

    while running:
        clock.tick(60)
        screen.fill(BROWN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_start=True
                    running=False
        enter_text = font.render(f"Press Enter!!", True, BLACK)
        screen.blit(enter_text, (300, 300))
        pygame.display.update()
    if(is_start):
        running = False
        create_conn()
        time.sleep(10)
        run_game()
main()