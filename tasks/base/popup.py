from zafkiel import API, Template
from zafkiel.decorator import run_until_true
from zafkiel.ocr import Keyword
from zafkiel.utils import is_color_similar, crop

from tasks.base.page import TPL_CONFIRM_BUTTON


class PopupHandler(API):
    # 凭证奖励弹窗
    def handle_bp_reward(self):
        rec_template = Template(r"POPUP_BP_FLAG.png", (-0.137, 0.218), Keyword('升级凭证'))
        touch_template = Template(r"POPUP_BP_CLAIM.png", (0.137, 0.218), Keyword('领取奖励'))
        if self.find_click(rec_template, timeout=0, touch_template=touch_template):
            return self.find_click(TPL_CONFIRM_BUTTON)

    # 活动通知弹窗
    def handle_login_event(self):
        rec_template = Template(r"POPUP_EVENT_FLAG.png", (0.0, 0.24))
        touch_template = Template(r"POPUP_MARGIN.png", (0.467, -0.252))
        return self.find_click(rec_template, timeout=0, touch_template=touch_template, blind=True)

    # 不定时的七日登录奖励
    @run_until_true
    def handle_7day_reward(self):
        if self.find_click(Template(r"7DAY_REWARD_CLAIM.png", (0.084, 0.234)), timeout=0):
            if self.find_click(Template(r"7DAY_REWARD_CONFIRM.png", (-0.001, 0.145))):
                return True

        return False

    # 每日签到奖励
    @run_until_true
    def handle_signin_reward(self):
        if self.find_click(Template(r"SIGNIN_REWARD_CLAIM.png", (0.083, 0.248)),
                           timeout=0):
            if self.find_click(Template(r"SIGNIN_REWARD_CONFIRM.png", (-0.001, 0.134))):
                return True

        return False

    # 游戏公告，最近好像不弹了
    # @run_until_true
    # def handle_notice(self):
    #     rec_template = Template(r"assets/NOTICE_FLAG.png", record_pos=(-0.391, -0.194), resolution=(1280, 720),
    #                             rgb=True)
    #     touch_template = Template(r"assets/NOTICE_CLOSE.png", record_pos=(0.431, -0.22), resolution=(1280, 720))
    #     return self.find_click(rec_template, timeout=0.5, touch_template=touch_template)

    # 深渊结算弹窗
    @run_until_true
    def handle_abyss_settle(self):
        rec_template = Template(r"ABYSS_SETTLE.png", (-0.384, -0.005))
        if is_color_similar(rec_template.image, crop(self.screenshot(), rec_template.area)):
            self.touch(Template(r"POPUP_MARGIN.png", (0.467, -0.252)), blind=True)
            return True
        return False


popup_handler = PopupHandler()
popup_list = [popup_handler.handle_login_event, popup_handler.handle_7day_reward, popup_handler.handle_signin_reward,
              popup_handler.handle_abyss_settle]

# Template(r"NEW_ITEM_POPUP.png", (0.289, -0.01))