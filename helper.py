import random

import cv2
from airtest.core.api import *


# 随机点击以(x,y)为中心，w为宽，h为高的区域
def random_click(x, y, w, h):
    # sleep(random.uniform(0.1, 1.0))
    rand_x = random.randint(x - int(w / 2), x + int(w / 2))
    rand_y = random.randint(y - int(h / 2), y + int(h / 2))
    touch(rand_x, rand_y)


# 匹配模板图片并在上面随机位置点击
def find_click(template):
    pos = exists(template)
    if pos:
        img = cv2.imread(template.filepath)
        ratio = (device().get_rect().width() - 6) / template.resolution[0]
        # 屏幕对应位置的高宽
        h = img.shape[0] * ratio
        w = img.shape[1] * ratio
        random_click(pos[0], pos[1], w, h)
        return True
    else:
        return False
