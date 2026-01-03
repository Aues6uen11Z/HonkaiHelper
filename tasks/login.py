import datetime
import shutil
import time
from pathlib import Path
import subprocess

from zafkiel import (
    Template,
    logger,
    wait,
    touch,
    stop_app,
    auto_setup,
    sleep,
    exists,
    find_click,
    Timer,
)
from zafkiel.exception import LoopError
from zafkiel.ocr import Keyword
from zafkiel.ui import UI

from config import Config
from tasks.base.popup import popup_list, popup_handler
from tasks.base.page import TPL_CONFIRM_BUTTON, page_main


class Login(UI):
    def __init__(self, config: Config):
        self.config = config

    def manage_log(self):
        log_retain_map = {
            "1day": 1,
            "3days": 3,
            "1week": 7,
            "1month": 30,
        }
        retain_days = log_retain_map.get(
            self.config.data["Project"]["General"]["Game"]["log_retain"], 7
        )

        current_time = time.time()
        log_path = Path("./log")

        for log_dir in log_path.iterdir():
            create_time = log_dir.stat().st_ctime
            age_in_days = (current_time - create_time) / (24 * 3600)

            if age_in_days > retain_days:
                try:
                    logger.info(f"Deleting old log directory: {log_dir}")
                    shutil.rmtree(log_dir)
                except Exception as e:
                    logger.error(f"Failed to delete {log_dir}: {e}")

    def handle_app_login(self):
        wait(
            Template(r"LOGIN_FLAG.png", (0.406, 0.233), rgb=True),
            timeout=1200,
            interval=3,
            interval_func=self.check_update,
        )
        touch(Template(r"LOGIN_CLICK.png", (-0.002, -0.031)), times=2, blind=True)

        try:
            confirm_time = float(
                self.config.data["Daily"]["Login"]["Login"]["confirm_time"]
            )
            if confirm_time < 3.0:
                confirm_time = 3.0
                logger.warning(
                    "Confirm time was less than 3.0, setting to minimum value of 3.0"
                )
        except:
            confirm_time = 3.0
            logger.warning("Invalid confirm_time in config, using default value of 3.0")

        loop_timer = Timer(120).start()
        while True:
            if loop_timer.reached():
                raise LoopError("The operation has looped too many times")

            if self.ui_additional():
                continue
            if find_click(TPL_CONFIRM_BUTTON):
                continue
            if popup_handler.handle_abyss_settle():
                continue
            if self.ui_page_appear(page_main):
                sleep(confirm_time)
                if not self.ui_ensure(page_main):
                    logger.info("Game login successful")
                    break

        return True

    def app_stop(self):
        stop_app()

    def app_start(self):
        subprocess.Popen([self.config.data["Project"]["General"]["Game"]["game_path"]])
        sleep(15)

        date = datetime.datetime.now().strftime("%Y-%m-%d")
        auto_setup(
            str(Path.cwd()),
            logdir=f"./log/{date}/report",
            devices=[
                "WindowsPlatform:///?title=崩坏3",
            ],
        )
        self.manage_log()
        self.get_popup_list(popup_list)
        self.handle_app_login()

    def app_restart(self):
        self.app_stop()
        self.app_start()
        self.handle_app_login()

    @staticmethod
    def check_update():
        if exists(Template(r"LOGIN_UPDATE.png", (0.002, -0.129))):
            find_click(Template(r"DOWNLOAD_CONFIRM.png", (0.0, 0.116)))
            logger.info("Game updating")
            if find_click(
                Template(r"DOWNLOAD_DONE.png", (0.0, 0.048), Keyword("确定")),
                timeout=1200,
            ):
                logger.info("Game update completed")
