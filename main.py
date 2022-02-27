# -*- encoding=utf8 -*-
__author__ = "Aues6uen11Z"

from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report

from event import *

if __name__ == '__main__':
    # 启动游戏
    os.system(game_path)
    sleep(5)

    # 连接游戏
    if not cli_setup():
        auto_setup(__file__, logdir=True, devices=["Windows:///?title=崩坏3", ])

    # 做日常
    login()
    daily(False)
    random_events = [gold, expedition, work, sweep]
    random.shuffle(random_events)
    for i in range(4):
        random_events[i]()
    daily(True)
    bp()

    # 结束游戏进程
    device().kill()

    # 生成报告
    simple_report(__file__, output='log/log.html')
