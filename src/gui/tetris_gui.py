import pygame
from game.tetris import Tetris
from gui.pygame_gui.pygame_gui import TetrisGUI
from settings import *


def main():
    # 创建俄罗斯方块游戏对象
    tetris = Tetris()
    # 俄罗斯方块的GUI
    gui = TetrisGUI(SCREEN_WIDTH, SCREEN_HEIGHT, tetris)

    # 创建计时器（防止while循环过快，占用太多CPU的问题）
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            tetris.process_event(event)
        tetris.update()
        gui.update()
        # FPS（每秒钟显示画面的次数）
        clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次
