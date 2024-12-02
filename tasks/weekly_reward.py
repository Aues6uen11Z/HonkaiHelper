import datetime
import time

from zafkiel import Template, exists, find_click, touch, logger
from zafkiel.ocr import Keyword
from zafkiel.ui import UI

from config import Config
from tasks.base.page import TPL_RETURN_BUTTON, page_missions, TPL_CONFIRM_BUTTON, page_main, TPL_NEW_ITEM, \
    page_armada_contribution
from tasks.base.popup import popup_handler
from tasks.base.switch import TPL_BP_MISSIONS_TAB, TPL_BP_REWARDS_TAB


class WeeklyReward(UI):
    def __init__(self, config: Config):
        self.config = config

        now = datetime.datetime.now()
        monday = now - datetime.timedelta(days=now.weekday())
        self.monday_4am = monday.replace(hour=4, minute=0, second=0, microsecond=0).timestamp()

    def share(self):
        if not self.config.data['WeeklyReward']['WeeklyEvent']['share']:
            return

        if self.config.data['WeeklyReward']['WeeklyEvent']['share_time'] > self.monday_4am:
            logger.info('Weekly sharing already completed')
            return

        self.ui_ensure(page_missions, TPL_BP_MISSIONS_TAB)
        if exists(Template(r"WEEKLY_SHARE.png", (-0.196, -0.134), Keyword('每周分享'))):
            find_click(Template(r"GOTO_SHARE.png", (0.013, -0.083), Keyword('前往')))
            touch(Template(r"SHARE_ITEM.png", (-0.199, -0.095)), blind=True)
            find_click(Template(r"SHARE_BUTTON.png", (-0.35, 0.222)), times=2)
            find_click(TPL_RETURN_BUTTON)
            logger.info('Weekly sharing completed')
        else:
            # 若已经手动完成
            logger.info('Weekly sharing already completed')
        self.config.update('WeeklyReward', 'WeeklyEvent', 'share_time', time.time())

    def homo_chest(self):
        if not self.config.data['WeeklyReward']['WeeklyEvent']['homo_chest']:
            return

        if self.config.data['WeeklyReward']['WeeklyEvent']['homo_chest_time'] > self.monday_4am:
            logger.info('Weekly homo chest already claimed')
            return

        self.ui_ensure(page_main)
        find_click(Template(r"MAIN_GOTO_MALL.png", (-0.423, 0.076)))
        find_click(Template(r"GOTO_GIFT.png", (-0.355, -0.123), Keyword('礼包')))
        find_click(Template(r"GOTO_WEEKLY_GIFT.png", (-0.355, -0.005), Keyword('周期')))
        if find_click(Template(r"BUY_HOMO_CHEST.png", (-0.207, 0.041), Keyword('免费'))):
            find_click(Template(r"HOMO_CHEST_CONFIRM.png", (-0.002, 0.18), Keyword('免费')))
            find_click(TPL_CONFIRM_BUTTON)
            logger.info('Weekly homo chest claim completed')
        else:
            logger.info('Weekly homo chest already claimed')
        self.config.update('WeeklyReward', 'WeeklyEvent', 'homo_chest_time', time.time())
        find_click(TPL_RETURN_BUTTON)

    def bp_chest(self):
        if not self.config.data['WeeklyReward']['WeeklyEvent']['bp_chest']:
            return

        if self.config.data['WeeklyReward']['WeeklyEvent']['bp_chest_time'] > self.monday_4am:
            logger.info('Weekly bp chest already claimed')
            return

        self.ui_ensure(page_missions, TPL_BP_REWARDS_TAB)
        if find_click(Template(r"BP_CHEST.png", (0.334, 0.203))):
            find_click(TPL_NEW_ITEM, timeout=2)
            find_click(TPL_CONFIRM_BUTTON)
            popup_handler.handle_bp_reward()
            logger.info('Weekly bp chest claim completed')
        else:
            logger.info('Weekly bp chest already claimed')
        self.config.update('WeeklyReward', 'WeeklyEvent', 'bp_chest_time', time.time())

    def armada_contribution_reward(self):
        if not self.config.data['WeeklyReward']['WeeklyEvent']['armada_contribution']:
            return

        if self.config.data['WeeklyReward']['WeeklyEvent']['armada_contribution_time'] > self.monday_4am:
            logger.info('Armada contribution reward already claimed')
            return

        self.ui_ensure(page_armada_contribution)
        if exists(Template(r"CONTRIBUTION_FULL.png", (-0.325, -0.123))):
            find_click(Template(r"CONTRIBUTION_REWARD.png", (-0.442, -0.122)))
            find_click(TPL_CONFIRM_BUTTON)
            self.config.update('WeeklyReward', 'WeeklyEvent', 'armada_contribution_time', time.time())
            logger.info('Armada contribution reward claim completed')
        elif exists(Template(r"CONTRIBUTION_CLAIMED.png", (-0.324, -0.122))):
            self.config.update('WeeklyReward', 'WeeklyEvent', 'armada_contribution_time', time.time())
            logger.info('Armada contribution reward already claimed')
        else:
            logger.info('Armada contribution reward not available')

    def run(self):
        self.share()
        self.homo_chest()
        self.bp_chest()
        self.armada_contribution_reward()


