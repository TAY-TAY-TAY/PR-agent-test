from settings import *
from blocks import *


def is_game_over(block_board):
    if "X" in block_board[0]:
        return True
    
    
def add_speed(score):
    speed_level = [("1", 0.5, 0, 20), 
                   ("2", 0.4, 21, 50), 
                   ("3", 0.3, 51, 100), 
                   ("4", 0.2, 101, 200), 
                   ("5", 0.1, 201, float("inf"))]
    for speed_info, speed, score_start, score_stop in speed_level:
        if score_stop and score_start <= score <= score_stop:
            return speed_info, speed


def del_lines(block_board):
    """
    判断是否存在满方格的行，如果有则消除
    """
    # 记录刚刚消除的行数
    move_row_list = list()
    # 消除满格的行
    for row, line in enumerate(block_board):
        if "." not in line:
            block_board[row] = ['.' for _ in range(len(line))]
            move_row_list.append(row)

    # 如果没有满格的行，则结束此函数
    if not move_row_list:
        return 0

    # 移动剩余的行到下一行
    for row in move_row_list:
        block_board.pop(row)
        block_board.insert(0, ['.' for _ in range(len(line))])

    return len(move_row_list) * 10


def add_to_block_board(block_board, current_block, current_block_start_row, current_block_start_col):
    """
    将当前已经停止移动的block添加到block_board中
    """
    for row, line in enumerate(current_block):
        for col, block in enumerate(line):
            if block != '.':
                block_board[current_block_start_row + row][current_block_start_col + col] = "X"


def change_block(current_block):
    """
    改变图形的样式
    """
    # 计算出，当前图形样式属于哪个图形
    current_block_style_list = None
    for block_style_list in [block_s, block_i, block_j, block_l, block_o, block_t, block_z]:
        if current_block in block_style_list:
            current_block_style_list = block_style_list

    # 得到当前正在用的图形的索引（下标）
    index = current_block_style_list.index(current_block)
    # 它的下一个图形的索引
    index += 1
    # 防止越界
    index = index % len(current_block_style_list)
    # 返回下一个图形
    return current_block_style_list[index]


def is_move_right(current_block, current_block_start_row, current_block_start_col, block_board):
    """
    判断是否可以向右移动
    """
    # 得到其它图形所有的坐标
    stop_all_block_position = list()
    for row, line in enumerate(block_board):
        for col, block in enumerate(line):
            if block != ".":
                stop_all_block_position.append((row, col))

    # 判断碰撞
    for col in range(len(current_block[0]) - 1, -1, -1):
        col_list = [line[col] for line in current_block]
        if 'X' in col_list and current_block_start_col + col >= BLOCK_COL_NUM:
            return False
        for row, block in enumerate(col_list):
            if block != "." and (current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                return False
    return True


def is_move_left(current_block, current_block_start_row, current_block_start_col, block_board):
    """
    判断是否可以向左移动
    """
    stop_all_block_position = list()
    for row, line in enumerate(block_board):
        for col, block in enumerate(line):
            if block != ".":
                stop_all_block_position.append((row, col))

    # 判断碰撞
    for col in range(len(current_block[0])):
        col_list = [line[col] for line in current_block]
        if 'X' in col_list and current_block_start_col + col < 0:
            return False
        for row, block in enumerate(col_list):
            if block != "." and (current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                return False
    return True


def is_move_down(current_block, current_block_start_row, current_block_start_col, block_board):
    """
    判断是否碰撞到其它图形或者底边界
    """
    stop_all_block_position = list()
    for row, line in enumerate(block_board):
        for col, block in enumerate(line):
            if block != ".":
                stop_all_block_position.append((row, col))

    # 判断碰撞
    for row, line in enumerate(current_block):
        if 'X' in line and current_block_start_row + row >= BLOCK_ROW_NUM:
            return False
        for col, block in enumerate(line):
            if block != "." and (current_block_start_row + row, current_block_start_col + col) in stop_all_block_position:
                return False

    return True