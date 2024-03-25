from zafkiel import Template, logger
from zafkiel.decorator import run_until_true
from zafkiel.ocr import DigitCounter, Keyword
from zafkiel.ui import UI

from tasks.base.page import page_armada, page_commission, page_armada_rewards, TPL_CONFIRM_BUTTON


class Armada(UI):
    def claim_rewards(self):
        logger.info('Start claiming armada rewards')
        while True:
            if not self.exists(Template(r"ARMADA_REWARD_TAB.png", (0.38, -0.128))):
                logger.info('Armada reward claim completed')
                break

            self.ui_goto(page_armada_rewards)
            self.find_click(Template(r"ARMADA_REWARD_CLAIM.png", (0.212, 0.225), Keyword('领取')))
            self.find_click(TPL_CONFIRM_BUTTON)

    def _handel_lack(self):
        logger.info('Handling lack of commission materials')
        while True:
            if self.exists(Template(r"COMMISSION_SUBMIT.png", (0.237, 0.224), Keyword('提交'), rgb=True)):
                break

            if self.find_click(Template(r"COMMISSION_MAX.png", (0.002, 0.161), Keyword('最大'))):
                self.find_click(Template(r"COMMISSION_BUY.png", (0.275, 0.162), Keyword('购买')), times=2)
                continue

            self.touch(Template(r"COMMISSION_LACK.png", (-0.398, -0.103)), blind=True)

    @run_until_true
    def _apply_new(self):
        logger.info('Applying for new commission')
        ocr = DigitCounter(Template(r"COMMISSION_REQUEST.png", (-0.36, 0.225)))
        if ocr.ocr_single_line(self.screenshot())[0] == 0:
            self.find_click(Template(r"COMMISSION_REQUEST.png", (-0.36, 0.225)), blind=True)
            self.find_click(Template(r"COMMISSION_REQUEST_FLAG.png", (-0.384, -0.184), Keyword('申请新委托')),
                            Template(r"COMMISSION_ACCEPT.png", (0.375, -0.079), Keyword('接受')),
                            times=2)
            logger.info('New commission request completed')
            return True
        return False

    def commission(self):
        logger.info('Start commission process')
        self.ui_goto(page_commission)
        ocr = DigitCounter(Template(r"COMMISSION_COUNT.png", (0.43, 0.242)))

        while True:
            if ocr.ocr_single_line(self.screenshot())[0] == 0:
                logger.info('Commissions submit completed')
                break

            if self._apply_new():
                continue

            if self.find_click(Template(r"COMMISSION_SUBMIT.png", (0.237, 0.224), Keyword('提交'), rgb=True),
                               timeout=0):
                continue
            if self.exists(Template(r"COMMISSION_SUBMIT_LACK.png", (0.237, 0.225), Keyword('提交'), rgb=True)):
                logger.info('Insufficient commission materials, suggest to buy in advance to speed up')
                self._handel_lack()
            self.find_click(Template(r"COMMISSION_SUBMIT_CONFIRM.png", (0.135, 0.159), Keyword('提交委托')),
                            timeout=0)
            self.find_click(Template(r"COMMISSION_PUT.png", (0.0, 0.137), Keyword('放入舰团奖励池')),
                            times=2, timeout=0)

    def run(self):
        self.ui_ensure(page_armada)
        self.commission()
        self.claim_rewards()

