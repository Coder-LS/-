# -*- coding: utf-8 -*-
"""
跳一跳手动版（先点起点再点终点）
根据numpy和 matplotlib库来分析棋子和棋盘坐标并显示动态截图，用鼠标点击实现跳跃
"""
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation   #刷新手机截图图片（跳之前和其后的截图，动态的）
from PIL import Image


def pull_screenshot():
    # 利用adb操控安卓手机截取图片到手机储存的根目录(获取当前界面手机截图)
    os.system('adb shell screencap -p /sdcard/autojump.png')
    # 从安卓手机里拿出这张图片到此文件夹下(下载当前这个截图到当前电脑文件夹下)
    os.system('adb pull /sdcard/autojump.png .')


def jump(distance):
    press_time = distance * 1.35
    press_time = int(press_time)
    # # adb执行 前四个参数是起跳点的横纵坐标(抓包知道320 410) 后是按压时间(一个像素点要按压1.35s,抓包)
    cmd = 'adb shell input swipe 320 410 320 410 ' + str(press_time)
    print(cmd)
    os.system(cmd)

# 创建一个空白的图片对象/创建一张图片
fig = plt.figure()
pull_screenshot()
img = np.array(Image.open('autojump.png'))
#把获取的图片画在坐标轴上
im = plt.imshow(img, animated=True)

update = True
click_count = 0
cor = []


def update_data(): #更新图片
    return np.array(Image.open('autojump.png'))


def updatefig(*args): #更新图片
    global update
    if update:
        time.sleep(1.5)
        pull_screenshot()
        im.set_array(update_data())
        update = False
    return im,

#鼠标点击
#绑定鼠标单击
def on_click(event):
    global update
    global ix, iy # 起点与终点的坐标
    global click_count
    global cor

    # 添加跳的起始点横纵坐标
    ix, iy = event.xdata, event.ydata
    coords = [(ix, iy)]
    print('now = ', coords)
    cor.append(coords)

    click_count += 1
    if click_count > 1:
        click_count = 0
        cor1 = cor.pop()
        cor2 = cor.pop()

        distance = (cor1[0][0] - cor2[0][0])**2 + (cor1[0][1] - cor2[0][1])**2  ##勾股定理,计算距离
        distance = distance ** 0.5
        print('distance = ', distance)
        jump(distance)
        update = True


fig.canvas.mpl_connect('button_press_event', on_click)
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
