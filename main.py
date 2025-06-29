import argparse
import ctypes
import datetime
import sys
from pathlib import Path

from loguru import logger
from zafkiel import simple_report, auto_setup
from zafkiel.ui import UI

from config import Config
from tasks.armada import Armada
from tasks.base.popup import popup_list
from tasks.dorm_bonus import DormBonus
from tasks.errand import Errand
from tasks.expedition import Expeditions
from tasks.login import Login
from tasks.mail import Mail
from tasks.mission import Missions
from tasks.sweep import Sweep
from tasks.weekly_reward import WeeklyReward

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <7}</level> | "
    "<level>{message}</level>",
)
date = datetime.datetime.now().strftime("%Y-%m-%d")
logger.add(
    f"./log/{date}/{date}.log",
    level="DEBUG",
    format="<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <7}</level> | "
    "<level>{message}</level>",
)


def all_tasks(config):
    try:
        # 日常
        Login(config).app_start()
        Missions(config).run()
        DormBonus(config).claim_stamina()
        DormBonus(config).claim_gold()
        Errand(config).run()
        Expeditions(config).run()
        Armada(config).run()
        Sweep(config).run()
        Missions(config).run()
        Mail(config).run()
        WeeklyReward(config).run()

        # 结束游戏进程
        Login(config).app_stop()

    except Exception as e:
        logger.exception(e)
        raise

    finally:
        simple_report(
            __file__,
            log_path=Path(f"./log/{date}/report").resolve(),
            output=f"./log/{date}/report.html",
        )


def single_task(config, task):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            if task != "login":
                auto_setup(
                    str(Path.cwd()),
                    logdir=f"./log/{date}/report",
                    devices=[
                        "WindowsPlatform:///?title=崩坏3",
                    ],
                )
                UI().get_popup_list(popup_list)

            if task == "armada":
                Armada(config).run()
            elif task == "dorm_bonus":
                DormBonus(config).run()
            elif task == "errand":
                Errand(config).run()
            elif task == "expedition":
                Expeditions(config).run()
            elif task == "login":
                Login(config).app_start()
            elif task == "logout":
                Login(config).app_stop()
                simple_report(
                    __file__,
                    log_path=Path(f"./log/{date}/report").resolve(),
                    output=f"./log/{date}/report.html",
                )
            elif task == "mail":
                Mail(config).run()
            elif task == "mission":
                Missions(config).run()
            elif task == "sweep":
                Sweep(config).run()
            elif task == "weekly_reward":
                WeeklyReward(config).run()
            
            break
            
        except Exception as e:
            if "!_src.empty()" in str(e):
                retry_count += 1
                logger.warning(f"Screen capture failed (attempt {retry_count}/{max_retries}), retrying...")
                if retry_count >= max_retries:
                    logger.error(f"Failed to execute task '{task}' after {max_retries} attempts due to screen capture issues")
                    simple_report(
                        __file__,
                        log_path=Path(f"./log/{date}/report").resolve(),
                        output=f"./log/{date}/report.html",
                    )
                    raise
            else:
                simple_report(
                    __file__,
                    log_path=Path(f"./log/{date}/report").resolve(),
                    output=f"./log/{date}/report.html",
                )
                logger.error(e)
                raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        "-t",
        choices=[
            "armada",
            "dorm_bonus",
            "errand",
            "expedition",
            "login",
            "logout",
            "mail",
            "mission",
            "sweep",
            "weekly_reward",
        ],
        help='Task name, one of "armada, dorm_bonus, errand, expedition, login, logout, mail, '
        'mission, sweep, weekly_reward"',
    )
    parser.add_argument("--config_path", "-c", default="./config/config.json")
    args = parser.parse_args()

    if args.task:
        config_path = Path(args.config_path).resolve()
        if not config_path.exists():
            logger.error(f"{config_path} not found")
            return
        config = Config(config_path)
        single_task(config, args.task)
    else:
        config = Config("./config/default.json")
        all_tasks(config)


if __name__ == "__main__":
    # 以管理员身份运行
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
