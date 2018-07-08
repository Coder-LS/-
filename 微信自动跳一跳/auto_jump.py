# -*- coding:utf-8 -*-
import time
import random
import os
import json
import subprocess    #subprocess通过子进程来执行外部指令，并通过input/output/error管道，获取子进程的执行的返回信息。
import re
from PIL import Image


def get_screen_size():
    """获取手机屏幕分辨率"""
    # 1920x1080
    size_str = os.popen('adb shell wm size').read()        #执行adb  shell 命令获取手机分辨率（1920x1080）
    if not size_str:
        print('请安装adb 及驱动并配置环境变量')
        exit()
    m = re.search(r'(\d+)x(\d+)', size_str)                    #用正则表达式匹配和提取 分辨率 字符
    if m:
        return "%sx%s" % (m.group(2), m.group(1))


def init():
    """初始化,获取配置,检查环境"""
    # 获取分辨率
    screen_size = get_screen_size()
    # 配置文件路径
    config_file_path = 'config/%s/config.json' % screen_size       #获取相应的分配率配置文件
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as f:
            print('Load config file from %s' % config_file_path)       #用json模块中的loads转换json
            return json.loads(f.read())
    else:
        with open('config/default.json', 'r') as f:
            print('Load default config')
            return json.loads(f.read())


def get_screenshot():
    """获取截图"""
    """auto.png"""
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()
    screenshot = screenshot.replace(b'\r\r\n', b'\n')
    with open('auto.png', 'wb') as f:
        f.write(screenshot)

def find_piece_board(img, config):
    """根据图片和配置文件找到棋盘棋子坐标"""
    # 获取图片的宽和高
    w, h = img.size
    # 扫描起始y坐标
    scan_start_y = 0
    # 棋子的最大y坐标
    piece_y_max = 0
    # 图片的像素矩阵
    img_pixel = img.load()
    # 以50px 为步长 扫描,测试出最高点
    for i in range(h//3, h*2//3, 50):
        first_pixel = img_pixel[0, i]
        for j in range(1, w):
            pixel = img_pixel[j, i]
            # 如果不是纯色的 跳出,说明找到了y轴的最大值
            if first_pixel[:-1] != pixel[:-1]:
                scan_start_y = i - 50
                break
        if scan_start_y:
            break
    # 开始扫描棋子
    left = 0
    right = 0
    for i in range(scan_start_y, h*2//3):
        flag = True
        for j in range(w//8, w*7//8): # 切掉左右1/8
            pixel = img_pixel[j, i]
            # 根据棋子的颜色判断,找到最后一行的点的起始后末尾
            if (50 < pixel[0] < 60) and (53 < pixel[1] < 63) and (95 < pixel[2] < 110):
                if flag:
                    left = j
                    flag = False
                right = j
                piece_y_max = max(i, piece_y_max)
    piece_x = (left+right)//2
    piece_y = piece_y_max - config['piece_base_height_1_2']
    print(piece_x, piece_y)
def jump(distance, param):
    """跳一段距离"""
    pass

def test_piece():
    config = init()
    img = Image.open('auto.png')
    find_piece_board(img, config)
def run():
    """主函数"""
    # 获取配置,检查检查环境
    config = init()
    # print(config)
    # 循环操作
    while True:
        # 获取截图
        get_screenshot()
        # 生成图片对象
        img = Image.open('auto.png')
        # 获取棋子, 棋盘坐标
        piece_x, piece_y, board_x, board_y = find_piece_board(img, config)
        # 计算距离
        distance = ((piece_x-board_x)**2 + (piece_y-board_y)**2)**0.5
        # 跳
        jump(distance, config['press_ratio'])
        # 随机间隔时间
        time.sleep(1+random.random()*2)
if __name__ == '__main__':
    #run()
    test_piece()