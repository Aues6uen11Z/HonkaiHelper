from typing import Dict

from zafkiel import Template, logger, Timer
from zafkiel.exception import LoopError
from zafkiel.ocr import Keyword
from zafkiel.ui import UI

from tasks.base.page import page_mail, TPL_CONFIRM_BUTTON


class Mail(UI):
    def __init__(self, config: Dict = None):
        self.config = config

    def run(self):
        self.ui_ensure(page_mail)

        loop_timer = Timer(0, 10).start()
        while True:
            if loop_timer.reached():
                raise LoopError('The operation has looped too many times')

            if self.exists(Template(r"NO_MORE_MAIL.png", (-0.449, -0.154), Keyword('已读'))):
                logger.info('Mail claim completed')
                break

            if self.find_click(Template(r"MAIL_QUICK_CLAIM.png", (0.42, 0.245), Keyword('一键领取'), rgb=True)):
                continue
            if self.find_click(TPL_CONFIRM_BUTTON):
                continue

