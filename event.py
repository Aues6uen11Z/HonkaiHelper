from anti_detection import *
from config import *


# 登录前有可能要更新数据
def check_update():
    pass


# 回到主界面
def back_to_main():
    while not exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        device().key_press("`")
        device().key_release("`")
        sleep(random.uniform(0.3, 1.0))


# 刚上线的一系列操作
def login():
    # 点击登录
    wait(Template(r"img/tpl1645854935043.png", record_pos=(0.407, 0.234), resolution=(1280, 720)), timeout=120,
         interval=3,
         intervalfunc=check_update)
    random_click(590, 300, 1160, 540, times=3)
    # 签到
    if find_click(Template(r"img/tpl1645853249505.png", record_pos=(0.083, 0.248), resolution=(1280, 720)), timeout=10):
        find_click(Template(r"img/tpl1645854410174.png", record_pos=(-0.001, 0.134), resolution=(1280, 720)))
    sleep(5)
    # 关闭公告和活动
    back_to_main()


# 领金币
def gold():
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645878953544.png", record_pos=(-0.195, -0.062), resolution=(1280, 720)))


# 远征
def expedition():
    # 打开远征界面
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645856952234.png", record_pos=(0.17, 0.245), resolution=(1280, 720)))
    assert_exists(Template(r"img/tpl1645857039829.png", record_pos=(-0.34, -0.22), resolution=(1280, 720)),
                  "打开远征界面发生错误")

    # 领前一天远征奖励
    if find_click(Template(r"img/tpl1645857277604.png", record_pos=(0.237, -0.089), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645857505405.png", record_pos=(-0.001, 0.145), resolution=(1280, 720)))

    # 挂远征
    for _ in range(expedition_times):
        if not exists(Template(r"img/tpl1645857908239.png", record_pos=(0.237, -0.091), resolution=(1280, 720))):
            # 滑动远征列表
            p1 = random_coordinate(540, 640, 960, 100)
            p2 = random_coordinate(540, 300, 960, 100)
            swipe(p1, p2)
        if find_click(Template(r"img/tpl1645857908239.png", record_pos=(0.237, -0.091), resolution=(1280, 720))):
            find_click(
                Template(r"img/tpl1645857954430.png", rgb=True, record_pos=(0.118, 0.228), resolution=(1280, 720)))
            find_click(
                Template(r"img/tpl1645857986323.png", rgb=True, record_pos=(0.362, 0.227), resolution=(1280, 720)))

    # 返回家园界面
    sleep(3)
    device().key_press("`")
    device().key_release("`")
    assert_exists(Template(r"img/tpl1645865800963.png", record_pos=(-0.068, -0.117), resolution=(1280, 720)),
                  "返回家园界面发生错误")


# 打工
def work():
    # 打开打工界面
    if exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645856299732.png", record_pos=(0.325, 0.248), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645865941303.png", record_pos=(0.295, 0.25), resolution=(1280, 720)))
    assert_exists(Template(r"img/tpl1645865995991.png", record_pos=(-0.374, -0.241), resolution=(1280, 720)),
                  "打开打工界面发生错误")

    if exists(Template(r"img/tpl1645866078753.png", record_pos=(0.483, 0.0), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645866078753.png", record_pos=(0.483, 0.0), resolution=(1280, 720)))

    # 领打工奖励
    random_click(wx, wy, ww, wh, 15)

    # 打工派遣
    for _ in range(6):
        find_click(Template(r"img/tpl1645868275668.png", rgb=True, record_pos=(0.181, 0.246), resolution=(1280, 720)))
        find_click(Template(r"img/tpl1645868302799.png", rgb=True, record_pos=(0.388, 0.246), resolution=(1280, 720)))
        random_click(wx, wy, ww, wh)

    # 返回家园界面
    find_click(Template(r"img/tpl1645868275668.png", rgb=True, record_pos=(0.181, 0.246), resolution=(1280, 720)))
    for _ in range(2):
        device().key_press("`")
        device().key_release("`")
        sleep(1)
    assert_exists(Template(r"img/tpl1645865800963.png", record_pos=(-0.068, -0.117), resolution=(1280, 720)),
                  "返回家园界面发生错误")


# 每日活跃
def daily(last=False):
    # 打开每日界面
    back_to_main()
    find_click(Template(r"img/tpl1645871324073.png", record_pos=(-0.46, -0.186), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645879474251.png", record_pos=(-0.421, -0.123), resolution=(1280, 720)), timeout=1)
    assert_exists(Template(r"img/tpl1645871536979.png", record_pos=(-0.248, 0.248), resolution=(1280, 720)),
                  "打开每日界面发生错误")

    while exists(Template(r"img/tpl1645871935779.png", record_pos=(0.399, -0.132), resolution=(1280, 720))):
        random_click(dx, dy, dw, dh, 2)

    # 第一次领体力，第二次才全领完
    if last:
        for _ in range(5):
            find_click(
                Template(r"img/tpl1645873810361.png", rgb=True, record_pos=(0.039, 0.208), resolution=(1280, 720)))
            find_click(Template(r"img/tpl1645873777133.png", record_pos=(-0.001, 0.145), resolution=(1280, 720)))

    # 返回主界面
    device().key_press("`")
    device().key_release("`")
    assert_exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720)), '返回主界面发生错误')


# 一键减负
def sweep():
    # 打开材料活动界面
    back_to_main()
    find_click(Template(r"img/tpl1645872912915.png", record_pos=(0.36, -0.147), resolution=(1280, 720)))
    if exists(Template(r"img/tpl1645872988411.png", rgb=True, record_pos=(-0.451, -0.121), resolution=(1280, 720))):
        find_click(Template(r"img/tpl1645872988411.png", rgb=True, record_pos=(-0.451, -0.121), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645873106705.png", record_pos=(0.348, 0.119), resolution=(1280, 720)))
    assert_exists(Template(r"img/tpl1645873135683.png", record_pos=(-0.12, -0.023), resolution=(1280, 720)),
                  "打开材料活动界面发生错误")

    # 材料活动一键减负
    find_click(Template(r"img/tpl1645873175982.png", record_pos=(0.452, 0.241), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645873249602.png", record_pos=(-0.001, 0.131), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645873276874.png", record_pos=(-0.001, 0.145), resolution=(1280, 720)))

    # 返回主界面
    for _ in range(2):
        device().key_press("`")
        device().key_release("`")
        sleep(1)
    assert_exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720)), '返回主界面发生错误')


# 领凭证奖励
def bp():
    # 打开凭证界面
    back_to_main()
    find_click(Template(r"img/tpl1645871324073.png", record_pos=(-0.46, -0.186), resolution=(1280, 720)))
    find_click(Template(r"img/tpl1645875049434.png", record_pos=(-0.42, -0.052), resolution=(1280, 720)), timeout=1)
    assert_exists(Template(r"img/tpl1645875169213.png", record_pos=(0.265, 0.237), resolution=(1280, 720)),
                  "打开凭证界面出现错误")

    # 领每周箱子
    if find_click(Template(r"img/tpl1645874581457.png", record_pos=(-0.42, 0.216), resolution=(1280, 720)), timeout=1):
        find_click(Template(r"img/tpl1645874627052.png", record_pos=(0.0, 0.144), resolution=(1280, 720)))

    # 领奖励
    random_click(px, py, pw, ph)
    if not find_click(Template(r"img/tpl1645875473026.png", record_pos=(0.14, 0.172), resolution=(1280, 720))):
        device().key_press("`")
        device().key_release("`")

    # 返回主界面
    sleep(1)
    device().key_press("`")
    device().key_release("`")
    assert_exists(Template(r"img/tpl1645854690653.png", record_pos=(0.23, 0.076), resolution=(1280, 720)), '返回主界面发生错误')
