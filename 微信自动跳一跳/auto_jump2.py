# -*- coding: utf-8 -*-
"""
Project:20180111微信自动跳一跳  
Date:2018/1/11
QQ:1217750958
"""
__author__ = 'LS'

from  PIL import Image
import time
import random

def init():
    """初始化,获取配置,检查环境"""
    return

def get_screenshot():
    """获取截图"""
    """auto.png"""
    pass

def find_piece_board(img,config):
    pass



def run():
    config = init()
    while True:
        get_screenshot()
        image = Image.open('auto.png')
        piece_x,piece_y,board_x,board_x,board_y = find_piece_board(img,config)
