# -*- encoding=utf8 -*-
__author__ = "Aues6uen11Z"

import shutil

from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report

from event import *

if __name__ == '__main__':
    # 清除上一次的报告
    if os.path.exists('log'):
        shutil.rmtree('log')

    # 启动游戏
    os.system('start ' + game_path)
    sleep(10)

    # 连接游戏
    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=["Windows:///?title=崩坏3", ])

    # 做日常
    login()
    daily(False)
    random_events_1 = [gold, expedition, work, shop, strength]
    random_events_2 = [sweep, bp, mail, lsp]
    random.shuffle(random_events_1)
    random.shuffle(random_events_2)
    for i in range(5):
        random_events_1[i]()
    for i in range(4):
        random_events_2[i]()
    daily(True)
    if datetime.today().weekday() == 0:
        armada()

    # 结束游戏进程
    device().kill()

    # 生成报告
    simple_report(__file__, output='log/log.html')
