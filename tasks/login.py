import datetime
import shutil
import time
from pathlib import Path
import subprocess
from typing import Dict

from zafkiel import Template, logger
from zafkiel.ocr import Keyword
from zafkiel.ui import UI

from tasks.base.popup import popup_list, popup_handler
from tasks.base.page import page_main


class Login(UI):
    def __init__(self, config: Dict):
        self.config = config

    def manage_log(self):
        log_retain_map = {
            '1day': 1,
            '3days': 3,
            '1week': 7,
            '1month': 30,
        }
        retain_days = log_retain_map.get(self.config['General']['Game']['log_retain'], 7)

        current_time = time.time()
        log_path = Path('./log')

        for log_dir in log_path.iterdir():
            create_time = log_dir.stat().st_ctime
            age_in_days = (current_time - create_time) / (24 * 3600)

            if age_in_days > retain_days:
                try:
                    logger.info(f'Deleting old log directory: {log_dir}')
                    shutil.rmtree(log_dir)
                except Exception as e:
                    logger.error(f'Failed to delete {log_dir}: {e}')

    def handle_app_login(self):

        self.wait(Template(r"LOGIN_FLAG.png", (0.406, 0.233), rgb=True),
                  timeout=1200, interval=3, interval_func=self.check_update)
        self.touch(Template(r"LOGIN_CLICK.png", (-0.002, -0.031)),
                   times=2, blind=True)

        while True:
            if self.ui_additional():
                continue
            if popup_handler.handle_abyss_settle():
                continue
            if self.ui_page_appear(page_main):
                self.sleep(3)
                if not self.ui_ensure(page_main):
                    logger.info('Game login successful')
                    break

        return True

    def app_stop(self):
        self.stop_app()

    def app_start(self):
        subprocess.Popen([self.config['General']['Game']['game_path']])
        # date = datetime.datetime.now().strftime("%Y-%m-%d")
        # self.auto_setup(str(Path.cwd()), logdir=f'./log/{date}/report', devices=["WindowsPlatform:///?title=崩坏3", ])
        self.auto_setup(str(Path.cwd()), devices=["WindowsPlatform:///?title=崩坏3", ])
        self.manage_log()
        self.get_popup_list(popup_list)  # TODO: Move to program start instead of game start

        self.sleep(15)
        self.handle_app_login()

    def app_restart(self):
        self.app_stop()
        self.app_start()
        self.handle_app_login()

    def check_update(self):
        if self.exists(Template(r"LOGIN_UPDATE.png", (0.002, -0.129))):
            self.find_click(Template(r"DOWNLOAD_CONFIRM.png", (0.0, 0.116)))
            logger.info('Game updating')
            if self.find_click(Template(r"DOWNLOAD_DONE.png", (0.0, 0.048), Keyword('确定')), timeout=1200):
                logger.info('Game update completed')
