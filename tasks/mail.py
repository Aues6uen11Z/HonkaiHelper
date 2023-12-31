from zafkiel import Template, logger
from zafkiel.ocr import Keyword
from zafkiel.ui import UI

from tasks.base.page import page_mail, TPL_CONFIRM_BUTTON


class Mail(UI):
    def run(self):
        self.ui_ensure(page_mail)

        while True:
            if self.exists(Template(r"NO_MORE_MAIL.png", (0.386, 0.244), rgb=True)):
                logger.info('领取邮件')
                break

            if self.find_click(Template(r"MAIL_QUICK_CLAIM.png", (0.42, 0.245), Keyword('一键领取'), rgb=True)):
                continue
            if self.find_click(TPL_CONFIRM_BUTTON):
                continue

