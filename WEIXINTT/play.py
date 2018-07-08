import os
import cv2
import numpy as np
import time
import random


# ʹ�õ�Python�⼰��Ӧ�汾��
# python 3.6
# opencv-python 3.3.0
# numpy 1.13.3
# �õ���opencv���е�ģ��ƥ��ͱ�Ե��⹦��


def get_screenshot(id):
    os.system('adb shell screencap -p /sdcard/%s.png' % str(id))
    os.system('adb pull /sdcard/%s.png .' % str(id))


def jump(distance):
    # �����������Ҫ�����Ļ�ֱ��ʽ����Ż�
    press_time = int(distance * 1.35)

    # ��������ֻ���Ļģ�ⴥ����
    # ģ�ⴥ�������ÿ�ζ���ͬһλ�ã��ɼ��ϴ������޷�ͨ����֤
    rand = random.randint(0, 9) * 10
    cmd = ('adb shell input swipe %i %i %i %i ' + str(press_time)) \
          % (320 + rand, 410 + rand, 320 + rand, 410 + rand)
    os.system(cmd)
    print(cmd)


def get_center(img_canny, ):
    # ���ñ�Ե���Ľ��Ѱ���������غ�����
    # ���������������ĵ�
    y_top = np.nonzero([max(row) for row in img_canny[400:]])[0][0] + 400
    x_top = int(np.mean(np.nonzero(canny_img[y_top])))

    y_bottom = y_top + 50
    for row in range(y_bottom, H):
        if canny_img[row, x_top] != 0:
            y_bottom = row
            break

    x_center, y_center = x_top, (y_top + y_bottom) // 2
    return img_canny, x_center, y_center


# ��һ����Ծ�ľ����ǹ̶���
jump(530)
time.sleep(1)

# ƥ��С�����ģ��
temp1 = cv2.imread('temp_player.jpg', 0)
w1, h1 = temp1.shape[::-1]
# ƥ����Ϸ���������ģ��
temp_end = cv2.imread('temp_end.jpg', 0)
# ƥ������СԲ���ģ��
temp_white_circle = cv2.imread('temp_white_circle.jpg', 0)
w2, h2 = temp_white_circle.shape[::-1]

# ѭ��ֱ����Ϸʧ�ܽ���
for i in range(10000):
    get_screenshot(0)
    img_rgb = cv2.imread('%s.png' % 0, 0)

    # �������Ϸ��ͼ��ƥ�䵽��"����һ��"������ģ�壬��ѭ����ֹ
    res_end = cv2.matchTemplate(img_rgb, temp_end, cv2.TM_CCOEFF_NORMED)
    if cv2.minMaxLoc(res_end)[1] > 0.95:
        print('Game over!')
        break

    # ģ��ƥ���ͼ��С�����λ��
    res1 = cv2.matchTemplate(img_rgb, temp1, cv2.TM_CCOEFF_NORMED)
    min_val1, max_val1, min_loc1, max_loc1 = cv2.minMaxLoc(res1)
    center1_loc = (max_loc1[0] + 39, max_loc1[1] + 189)

    # �ȳ���ƥ���ͼ�е�����ԭ�㣬
    # ���ƥ��ֵû�дﵽ0.95����ʹ�ñ�Ե���ƥ���������
    res2 = cv2.matchTemplate(img_rgb, temp_white_circle, cv2.TM_CCOEFF_NORMED)
    min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(res2)
    if max_val2 > 0.95:
        print('found white circle!')
        x_center, y_center = max_loc2[0] + w2 // 2, max_loc2[1] + h2 // 2
    else:
        # ��Ե���
        img_rgb = cv2.GaussianBlur(img_rgb, (5, 5), 0)
        canny_img = cv2.Canny(img_rgb, 1, 10)
        H, W = canny_img.shape

        # ��ȥС���������Ա�Ե������ĸ���
        for k in range(max_loc1[1] - 10, max_loc1[1] + 189):
            for b in range(max_loc1[0] - 10, max_loc1[0] + 100):
                canny_img[k][b] = 0

        img_rgb, x_center, y_center = get_center(canny_img)

    # ��ͼƬ����Թ�����
    img_rgb = cv2.circle(img_rgb, (x_center, y_center), 10, 255, -1)
    # cv2.rectangle(canny_img, max_loc1, center1_loc, 255, 2)
    cv2.imwrite('last.png', img_rgb)

    distance = (center1_loc[0] - x_center) ** 2 + (center1_loc[1] - y_center) ** 2
    distance = distance ** 0.5
    jump(distance)
    time.sleep(1.3)