from zafkiel import Template, logger
from zafkiel.ocr import Digit
from zafkiel.ui import UI

from tasks.base.page import page_missions, TPL_CONFIRM_BUTTON
from tasks.base.popup import popup_list
from tasks.base.switch import TPL_BP_MISSIONS_TAB, TPL_BP_REWARDS_TAB


class Missions(UI):
    def claim_bp_rewards(self):
        self.ui_goto(page_missions, TPL_BP_REWARDS_TAB)
        # # 领每周箱子，todo:写进配置，每周领过一次后不再识别；改逻辑
        # while True:
        #     if self.find_click(Template(r"BP_CHEST.png", record_pos=(0.334, 0.203))):
        #         self.find_click(Template(r"BP_CHEST_CLAIM.png", record_pos=(-0.134, 0.12), keyword=Keyword('领取')),
        #                         timeout=0)
        #         self.find_click(TPL_CONFIRM, times=2)
        #     popup_handler.handle_bp_reward()
        #     self.ui_additional()
        # 领凭证奖励
        screen = self.screenshot()
        ocr_current_level = Digit(Template(r"CURRENT_BP_LEVEL.png", (-0.29, -0.178)))
        current_level = ocr_current_level.ocr_single_line(screen)
        ocr_reward_level = Digit(Template(r"REWARD_BP_LEVEL.png", (-0.182, -0.13)))
        reward_level = ocr_reward_level.ocr_single_line(screen)
        if current_level >= reward_level:
            if self.touch(Template(r"BP_REWARD.png", (-0.179, -0.054)), blind=True):
                logger.info('领取凭证奖励')
                self.find_click(Template(r"BP_REWARD_CONFIRM.png", (0.141, 0.173)))

    def claim_daily_rewards(self):
        self.ui_goto(page_missions, TPL_BP_MISSIONS_TAB)
        if self.find_click(Template(r"QUICK_CLAIM.png", (0.418, -0.187), rgb=True)):
            logger.info('领取每日奖励')
            self.find_click(TPL_CONFIRM_BUTTON)

        ocr = Digit(Template(r"DAILY_BP.png", (-0.274, 0.23)))
        daily_bp = ocr.ocr_single_line(self.screenshot())
        click = False
        if daily_bp >= 600:
            click = self.find_click(Template(r"DAILY_REWARD_600.png", (0.449, 0.241)))
        elif daily_bp >= 450:
            click = self.find_click(Template(r"DAILY_REWARD_450.png", (0.312, 0.241)))
        elif daily_bp >= 300:
            click = self.find_click(Template(r"DAILY_REWARD_300.png", (0.175, 0.241)))
        elif daily_bp >= 200:
            click = self.find_click(Template(r"DAILY_REWARD_200.png", (0.037, 0.241)))
        elif daily_bp >= 100:
            click = self.find_click(Template(r"DAILY_REWARD_100.png", (-0.1, 0.241)))
        if click:
            self.find_click(TPL_CONFIRM_BUTTON)

    def run(self):
        self.ui_ensure(page_missions)
        self.claim_daily_rewards()
        self.claim_bp_rewards()
