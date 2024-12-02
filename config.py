import json
from pathlib import Path
from typing import Literal, List, Union

from pydantic import BaseModel, Field


class Argument(BaseModel):
    """
    Minimum setting
    """
    type: Literal['input', 'select', 'checkbox'] = 'input'
    value: Union[str, bool, float]
    option: List[str] = []
    hide: bool = False


class GroupCustomBase(BaseModel):
    """
    Basic settings for every task
    """
    priority: int = 3
    priority_enabled: bool = True
    command: str = ''
    command_enabled: bool = True


# 以下是实际设置内容
# 任务级别
class TaskGeneral(BaseModel):
    class GroupGeneralBase(BaseModel):
        """
        General settings for the project
        """
        work_dir: str = './examples/HonkaiHelper'
        work_dir_enabled: bool = True
        is_background: bool = False
        is_background_enabled: bool = True
        config_path: str = './examples/HonkaiHelper/config/config.json'
        config_path_enabled: bool = True

    class GroupGame(BaseModel):
        game_path: Argument = Argument(type='input', value='')
        log_retain: Argument = Argument(type='select', value='1week', option=['1day', '3days', '1week', '1month'])

    Base: GroupGeneralBase = Field(GroupGeneralBase(), alias='_Base')
    Game: GroupGame = GroupGame()


class TaskUpdate(BaseModel):
    class GroupUpdateBase(BaseModel):
        """
        Git repository, python virtual environment update settings
        """
        repo_url: str = 'https://gitee.com/aues6uen11z/HonkaiHelper'
        repo_url_enabled: bool = True
        branch: str = 'master'
        branch_enabled: bool = True
        local_path: str = './examples/HonkaiHelper'
        local_path_enabled: bool = True
        template_path: str = 'config'
        template_path_enabled: bool = True
        env_name: str = 'zafkiel'
        pip_mirror: str = 'https://pypi.tuna.tsinghua.edu.cn/simple'

    Base: GroupUpdateBase = Field(GroupUpdateBase(), alias='_Base')


class TaskArmada(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t armada', priority=5
    ), alias='_Base')


class TaskDormBonus(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t dorm_bonus', priority=2
    ), alias='_Base')


class TaskErrand(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t errand', priority=3
    ), alias='_Base')


class TaskExpedition(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t expedition', priority=4
    ), alias='_Base')


class TaskLogin(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t login', priority=0, priority_enabled=False
    ), alias='_Base')


class TaskLogout(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t logout', priority=100, priority_enabled=False
    ), alias='_Base')


class TaskMail(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t mail', priority=7
    ), alias='_Base')


class TaskMission1(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t mission', priority=1, priority_enabled=False
    ), alias='_Base')


class TaskMission2(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t mission', priority=8, priority_enabled=False
    ), alias='_Base')


class TaskSweep(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t sweep', priority=6
    ), alias='_Base')


class TaskWeeklyReward(BaseModel):
    class GroupWeeklyEvent(BaseModel):
        share: Argument = Argument(type='checkbox', value=True)
        share_time: Argument = Argument(type='input', value=0.0, hide=True)

        homo_chest: Argument = Argument(type='checkbox', value=True)
        homo_chest_time: Argument = Argument(type='input', value=0.0, hide=True)

        bp_chest: Argument = Argument(type='checkbox', value=True)
        bp_chest_time: Argument = Argument(type='input', value=0.0, hide=True)

        armada_contribution: Argument = Argument(type='checkbox', value=True)
        armada_contribution_time: Argument = Argument(type='input', value=0.0, hide=True)

    Base: GroupCustomBase = Field(GroupCustomBase(
        command='py main.py -t weekly_reward', priority=9
    ), alias='_Base')
    WeeklyEvent: GroupWeeklyEvent = GroupWeeklyEvent()


# 任务组级别
class MenuProject(BaseModel):
    General: TaskGeneral = TaskGeneral()
    Update: TaskUpdate = TaskUpdate()


class MenuDaily(BaseModel):
    Login: TaskLogin = TaskLogin()
    Logout: TaskLogout = TaskLogout()
    Mission1: TaskMission1 = TaskMission1()
    Mission2: TaskMission2 = TaskMission2()
    Sweep: TaskSweep = TaskSweep()
    Mail: TaskMail = TaskMail()
    DormBonus: TaskDormBonus = TaskDormBonus()
    Expedition: TaskExpedition = TaskExpedition()
    Errand: TaskErrand = TaskErrand()
    Armada: TaskArmada = TaskArmada()


class MenuWeekly(BaseModel):
    WeeklyReward: TaskWeeklyReward = TaskWeeklyReward()


# 项目级别
class UIContent(BaseModel):
    Project: MenuProject = MenuProject()
    Daily: MenuDaily = MenuDaily()
    Weekly: MenuWeekly = MenuWeekly()


def gen_i18n(config: BaseModel, lang: str):
    trans_dict = {
        "Menu": {},
        "Task": {},
    }

    # Check if the file already exists
    file_path = f'./config/i18n/{lang}.json'
    if Path(file_path).exists():
        # Load the existing translations
        with open(file_path, 'r', encoding='utf-8') as f:
            old_trans_dict = json.load(f)
    else:
        old_trans_dict = {}

    for menu, tasks in config.model_dump(by_alias=True).items():
        trans_dict['Menu'][menu] = old_trans_dict.get('Menu', {}).get(menu, {'name': ''})

        for task, groups in tasks.items():
            trans_dict['Task'][task] = old_trans_dict.get('Task', {}).get(task, {'name': ''})

            for group, args in groups.items():
                if group == '_Base':
                    continue
                if group not in trans_dict:
                    trans_dict[group] = {}

                trans_dict[group]['_info'] = old_trans_dict.get(group, {}).get('_info', {'name': '', 'help': ''})
                for arg, info in args.items():
                    trans_dict[group][arg] = old_trans_dict.get(group, {}).get(arg, {'name': '', 'help': ''})
                    if info['type'] == 'select':
                        for option in info['option']:
                            trans_dict[group][arg][option] = old_trans_dict.get(group, {}).get(arg, {}).get(option, '')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(trans_dict, f, ensure_ascii=False, indent=2)


def export() -> None:
    args = UIContent()
    with open('config/args.json', 'w') as f:
        f.write(args.model_dump_json(indent=2, by_alias=True))

    gen_i18n(args, 'zh-CN')


class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        with open('config/args.json', 'r') as f:
            args = json.load(f)
        with open(config_path, 'r') as f:
            self.data = json.load(f)

        # 只是为了校验数据
        for menu, tasks in args.items():
            for task, groups in tasks.items():
                for group, args in groups.items():
                    if group == '_Base':
                        continue
                    for argument, info in args.items():
                        info['value'] = self.data[task][group][argument]
        UIContent.parse_obj(args)

    def update(self, task, group, argument, value):
        self.data[task][group][argument] = value
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    export()
