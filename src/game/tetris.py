import pygame
import time
import sys
from blocks import get_random_block
from settings import *
from game.game import *


class Tetris:
    def __init__(self) -> None:
        self.current_block = get_random_block()  # 当前图形
        self.current_block_start_row = -2  # 当前图片从哪一行开始显示图形
        self.current_block_start_col = 4  # 当前图形从哪一列开始显示
        self.next_block = get_random_block()  # 下一个图形
        self.last_time = time.time()
        self.speed = 0.5  # 降落的速度
        self.speed_info = '1'  # 显示的速度等级
        # 定义一个列表，用来存储所有的已经停止移动的形状
        self.block_board = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]
        # 得分
        self.score = 0
        # 标记游戏是否结束
        self.game_over = False
    
    def process_event(self, event: pygame.event):
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if is_move_left(self.current_block, self.current_block_start_row, 
                                   self.current_block_start_col - 1, self.block_board):
                    self.current_block_start_col -= 1
            elif event.key == pygame.K_RIGHT:
                if is_move_right(self.current_block, self.current_block_start_row, 
                                    self.current_block_start_col + 1, self.block_board):
                    self.current_block_start_col += 1
            elif event.key == pygame.K_UP:
                current_block_next_style = change_block(self.current_block)
                if is_move_left(current_block_next_style, self.current_block_start_row, self.current_block_start_col, self.block_board) and \
                        is_move_right(current_block_next_style, self.current_block_start_row, self.current_block_start_col, self.block_board) and \
                        is_move_down(current_block_next_style, self.current_block_start_row, self.current_block_start_col, self.block_board):
                    # 判断新的样式没有越界
                    self.current_block = current_block_next_style
            elif event.key == pygame.K_DOWN:
                # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
                if is_move_down(self.current_block, self.current_block_start_row + 1, self.current_block_start_col, self.block_board):
                    self.current_block_start_row += 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
            if self.game_over:
                # 重置游戏用到的变量
                self.current_block = get_random_block()  # 当前图形
                self.current_block_start_row = -2  # 当前图片从哪一行开始显示图形
                self.current_block_start_col = 4  # 当前图形从哪一列开始显示
                self.next_block = get_random_block()  # 下一个图形
                self.block_board = [['.' for i in range(BLOCK_COL_NUM)] for j in range(BLOCK_ROW_NUM)]
                self.score = 0
                self.game_over = False
    
    def update(self):
        # 判断是否修改当前图形显示的起始行
        if not self.game_over and time.time() - self.last_time > self.speed:
            self.last_time = time.time()
            # 判断是否可以向下移动，如果碰到底部或者其它的图形就不能移动了
            if is_move_down(self.current_block, self.current_block_start_row + 1, 
                               self.current_block_start_col, self.block_board):
                self.current_block_start_row += 1
            else:
                # 将这个图形存储到统一的列表中，这样便于判断是否成为一行
                add_to_block_board(self.block_board, self.current_block, 
                                           self.current_block_start_row, self.current_block_start_col)
                # 判断是否有同一行的，如果有就消除，且加上分数
                self.score += del_lines(self.block_board)
                self.game_over = is_game_over(self.block_board)
                # 调整速度
                self.speed_info, self.speed = add_speed(self.score)
                # 创建新的图形
                self.current_block = self.next_block
                self.next_block = get_random_block()
                # 重置数据
                self.current_block_start_col = secrets.randint(1, BLOCK_COL_NUM - 4)
                self.current_block_start_row = -2