import random

import cv2
from airtest.core.api import *


# 获取随机坐标
def random_coordinate(x, y, w, h):
    rand_x = random.randint(x - int(w / 2 - 5), x + int(w / 2 - 5))
    rand_y = random.randint(y - int(h / 2 - 5), y + int(h / 2 - 5))
    return rand_x, rand_y


# 随机点击以(x,y)为中心，w为宽，h为高的区域
def random_click(x, y, w, h, times=1):
    touch(random_coordinate(x, y, w, h), times=times)


# 匹配模板图片并在上面随机位置点击
def find_click(template, timeout=3):
    try:
        pos = wait(template, timeout=timeout)
    except TargetNotFoundError:
        return False

    img = cv2.imread(template.filepath)
    ratio = (device().get_rect().width() - 6) / template.resolution[0]
    # 屏幕对应位置的高宽
    h = img.shape[0] * ratio
    w = img.shape[1] * ratio
    random_click(pos[0], pos[1], w, h)
    return True
