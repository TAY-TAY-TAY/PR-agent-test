import secrets
from .shapes import *

def get_random_block():
    """
    创建一个图形
    """
    block_style_list = secrets.choice([block_s, block_i, block_j, block_l, block_o, block_t, block_z])
    return secrets.choice(block_style_list)
