from typing import Dict

from zafkiel import Template, logger, screenshot, touch, find_click
from zafkiel.ocr import Digit, Keyword
from zafkiel.ui import UI

from tasks.base.page import page_missions, TPL_CONFIRM_BUTTON
from tasks.base.popup import popup_list, popup_handler
from tasks.base.switch import TPL_BP_MISSIONS_TAB, TPL_BP_REWARDS_TAB


class Missions(UI):
    def __init__(self, config: Dict = None):
        self.config = config

    def claim_bp_rewards(self):
        self.ui_goto(page_missions, TPL_BP_REWARDS_TAB)
        # # 领每周箱子，todo:写进配置，每周领过一次后不再识别；改逻辑
        # if self.find_click(Template(r"BP_CHEST.png", (0.334, 0.203))):
        #     while True:
        #         if self.find_click(Template(r"BP_CHEST_CLAIM.png", (-0.134, 0.12), Keyword('领取')), timeout=0):
        #             self.sleep(2)
        #         self.find_click(TPL_CONFIRM_BUTTON)
        #         popup_handler.handle_bp_reward()
        #
        # self.ui_additional()

        # 领凭证奖励
        screen = screenshot()
        ocr_current_level = Digit(Template(r"CURRENT_BP_LEVEL.png", (-0.29, -0.178)))
        current_level = ocr_current_level.ocr_single_line(screen)
        logger.info(f'Current BP level: {current_level}')

        ocr_reward_level = Digit(Template(r"REWARD_BP_LEVEL.png", (-0.182, -0.13)))
        reward_level = ocr_reward_level.ocr_single_line(screen)
        logger.info(f'BP reward level: {reward_level}')

        # TODO:65级以后右端顶到头，领取位置变了
        if current_level >= reward_level:
            if touch(Template(r"BP_REWARD.png", (-0.179, -0.054)), blind=True):
                popup_handler.handle_bp_reward()
                find_click(Template(r"BP_REWARD_CONFIRM.png", (0.141, 0.173)))
                logger.info('BP rewards claim completed')

    def claim_daily_rewards(self):
        self.ui_goto(page_missions, TPL_BP_MISSIONS_TAB)
        if find_click(Template(r"QUICK_CLAIM.png", (0.418, -0.187), Keyword('一键领取'), rgb=True), ocr_mode=1):
            find_click(TPL_CONFIRM_BUTTON)
            logger.info('Daily rewards claim completed')

        ocr = Digit(Template(r"DAILY_BP.png", (-0.273, 0.231)))
        daily_bp = ocr.ocr_single_line(screenshot())
        logger.info(f'Daily BP: {daily_bp}')
        click = False
        if daily_bp >= 600:
            click = find_click(Template(r"DAILY_REWARD_600.png", (0.449, 0.241)))
        elif daily_bp >= 450:
            click = find_click(Template(r"DAILY_REWARD_450.png", (0.312, 0.241)))
        elif daily_bp >= 300:
            click = find_click(Template(r"DAILY_REWARD_300.png", (0.175, 0.241)))
        elif daily_bp >= 200:
            click = find_click(Template(r"DAILY_REWARD_200.png", (0.037, 0.241)))
        elif daily_bp >= 100:
            click = find_click(Template(r"DAILY_REWARD_100.png", (-0.1, 0.241)))
        if click:
            find_click(TPL_CONFIRM_BUTTON)

    def run(self):
        # self.get_popup_list(popup_list)
        self.ui_ensure(page_missions)
        self.claim_daily_rewards()
        self.claim_bp_rewards()
