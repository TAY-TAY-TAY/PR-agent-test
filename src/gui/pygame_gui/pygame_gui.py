import pygame
import time
from settings import *
from game.tetris import Tetris


class TetrisGUI:
    def __init__(self, width: int, height: int, game: Tetris, caption: str = '俄罗斯方块'):
        self.width = width
        self.height = height
        self.game = game
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        # 字体
        self.font = pygame.font.Font("幼圆.ttf", size=24)  # 黑体24
        self.game_over_font = pygame.font.Font("幼圆.ttf", size=72)
        self.game_over_font_width, self.game_over_font_height = self.game_over_font.size('GAME OVER')
        self.game_again_font_width, self.game_again_font_height = self.font.size('鼠标点击任意位置，再来一局')
    
    def update(self):
        # 画背景（填充背景色）
        self.screen.fill(BG_COLOR)
        # 画游戏区域分隔线
        pygame.draw.line(self.screen, (100, 40, 200), (SIZE * BLOCK_COL_NUM, 0), (SIZE * BLOCK_COL_NUM, SCREEN_HEIGHT), BORDER_WIDTH)
        self.display_current_block()
        self.display_stop_block()
        self.display_grid()
        self.display_score_speed()
        self.display_next_block()
        self.display_over()
        # 刷新显示（此时窗口才会真正的显示）
        pygame.display.update()

    def display_current_block(self):
        # 显示当前图形
        for row, line in enumerate(self.game.current_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(self.screen, BLOCK_COLOR, 
                                     ((self.game.current_block_start_col + col) * SIZE, 
                                      (self.game.current_block_start_row + row) * SIZE, SIZE, SIZE), 0)

    def display_stop_block(self):
        # 显示所有停止移动的图形
        for row, line in enumerate(self.game.block_board):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(self.screen, BLOCK_COLOR, (col * SIZE, row * SIZE, SIZE, SIZE), 0)

    def display_grid(self):
        # 画网格线 竖线
        for x in range(BLOCK_COL_NUM):
            pygame.draw.line(self.screen, LINE_COLOR, (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
        # 画网格线 横线
        for y in range(BLOCK_ROW_NUM):
            pygame.draw.line(self.screen, LINE_COLOR, (0, y * SIZE), (BLOCK_COL_NUM * SIZE, y * SIZE), 1)

    def display_score_speed(self):
        # 显示右侧（得分、速度、下一行图形）
        # 得分
        score_show_msg = self.font.render('得分: ', True, FONT_COLOR)
        self.screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 10))
        score_show_msg = self.font.render(str(self.game.score), True, FONT_COLOR)
        self.screen.blit(score_show_msg, (BLOCK_COL_NUM * SIZE + 10, 50))
        # 速度
        speed_show_msg = self.font.render('速度: ', True, FONT_COLOR)
        self.screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 100))
        speed_show_msg = self.font.render(self.game.speed_info, True, FONT_COLOR)
        self.screen.blit(speed_show_msg, (BLOCK_COL_NUM * SIZE + 10, 150))
    
    def display_next_block(self):
        # 下一个图形（文字提示）
        next_style_msg = self.font.render('下一个: ', True, FONT_COLOR)
        self.screen.blit(next_style_msg, (BLOCK_COL_NUM * SIZE + 10, 200))
        # 下一个图形（图形）
        for row, line in enumerate(self.game.next_block):
            for col, block in enumerate(line):
                if block != '.':
                    pygame.draw.rect(self.screen, BLOCK_COLOR, (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE, SIZE, SIZE), 0)
                    # 显示这个方格的4个边的颜色
                    # 左
                    pygame.draw.line(self.screen, LINE_COLOR, (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                    # 上
                    pygame.draw.line(self.screen, LINE_COLOR, (320 + SIZE * col, (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), 1)
                    # 下
                    pygame.draw.line(self.screen, LINE_COLOR, (320 + SIZE * col, (BLOCK_COL_NUM + row + 1) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)
                    # 右
                    pygame.draw.line(self.screen, LINE_COLOR, (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row) * SIZE), (320 + SIZE * (col + 1), (BLOCK_COL_NUM + row + 1) * SIZE), 1)

    def display_over(self):
        # 显示游戏结束画面
        if self.game.game_over:
            game_over_tips = self.game_over_font.render('GAME OVER', True, RED)
            self.screen.blit(game_over_tips, ((SCREEN_WIDTH - self.game_over_font_width) // 2, 
                                              (SCREEN_HEIGHT - self.game_over_font_height) // 2))
            # 显示"鼠标点击任意位置，再来一局"
            game_again = self.font.render('鼠标点击任意位置，再来一局', True, RED)
            self.screen.blit(game_again, ((SCREEN_WIDTH - self.game_again_font_width) // 2, 
                                          (SCREEN_HEIGHT - self.game_again_font_height) // 2 + 80))

        
