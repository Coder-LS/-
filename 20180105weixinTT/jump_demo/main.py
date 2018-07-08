#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : LS
# @File    : main.py
# @Software: PyCharm

import os
import PIL,numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation #刷新图片
import time

need_update = True

def get_screen_img():
    # 利用adb操控安卓手机截取图片到手机储存的根目录(获取当前界面手机截图)
    os.system('adb shell screencap -p /sdcard/screen.png')
    # 从安卓手机里拿出这张图片到此文件夹下(下载当前这个截图到当前电脑文件夹下)
    os.system('adb pull /sdcard/screen.png')
    JieTu = PIL.Image.open('screen.png')
    return numpy.array(JieTu)

def jump_to_next(point1,point2):
    # 起点与终点的坐标
    x1,y1 = point1; x2,y2 = point2
    #勾股定理,计算距离
    distance = ((x2-x1)**2 +(y2-y1)**2)**0.5
    # adb执行 前四个参数是起跳点的横纵坐标(抓包知道320 410) 后是按压时间(一个像素点要按压1.35s,抓包)
    os.system('adb shell input swipe 320 410 320 410 {}'.format(int(distance*1.35)))

#鼠标点击
#绑定鼠标单击
def on_calck(event,coor = []): #[(x,y),(x2,y2)]
    need_update = True
    #添加跳的起始点横纵坐标
    coor.append((event.xdata,event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(),coor.pop())
     need_update = True

def update_screen(frame):#更新图片
    global need_update
    if need_update:
        time.sleep(2)
        axes_image.set_array(get_screen_img())
        need_update=False
    return axes_image,




# 创建一个空白的图片对象/创建一张图片
figure = plt.figure()
#把获取的图片画在坐标轴上
axes_image = plt.imshow(get_screen_img(),animated = True )

figure.canvas.mpl_connect('button_press_event',on_calck)

FuncAnimation(figure,update_screen,interval=50 ,blit=True)

plt.show()
