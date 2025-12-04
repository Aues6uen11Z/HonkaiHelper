import json
from pathlib import Path
from typing import Literal, List, Union

from pydantic import BaseModel, Field


class Item(BaseModel):
    """
    Minimum setting
    """
    type: Literal['input', 'select', 'checkbox', 'folder', 'file', 'priority'] = 'input'
    value: Union[str, bool, float]
    option: List[str] = []
    hidden: bool = False
    help: str = ''
    disabled: bool = False

    model_config = {
        'populate_by_name': True,
    }

    def __init__(self, value=None, **data):
        if value is not None and not isinstance(value, dict):
            data['value'] = value
        super().__init__(**data)


class GroupCustomBase(BaseModel):
    """
    Basic settings for every task
    """
    # active: Item = Item(type='checkbox', value=True)
    priority: Item = Item(type='priority', value=0)
    command: Item = Item('')


# 以下是实际设置内容
# 任务级别
class TaskGeneral(BaseModel):
    class GroupGeneralBase(BaseModel):
        """
        General settings for the project
        """
        language: Item = Item('中文')
        work_dir: Item = Item('./repos/HonkaiHelper', disabled=True)
        background: Item = Item(value=False, disabled=True)
        config_path: Item = Item('./repos/HonkaiHelper/config/config.json', disabled=True)
        log_path: Item = Item('./log', disabled=True)

    class GroupGame(BaseModel):
        game_path: Item = Item(type='file', value='')
        log_retain: Item = Item(type='select', value='1week', option=['1day', '3days', '1week', '1month'])
        keep_foreground: Item = Item(type='checkbox', value=False)

    Base: GroupGeneralBase = Field(GroupGeneralBase(), alias='_Base')
    Game: GroupGame = GroupGame()


class TaskUpdate(BaseModel):
    class GroupUpdatelBase(BaseModel):
        """
        General settings for the project
        """
        env_name: Item = Item('zafkiel')
        python_version: Item = Item('3.11')

    Base: GroupUpdatelBase = Field(GroupUpdatelBase(), alias='_Base')


class TaskArmada(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t armada', disabled=True), priority=Item(4)
    ), alias='_Base')


class TaskDormBonus(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t dorm_bonus', disabled=True), priority=Item(5)
    ), alias='_Base')


class TaskErrand(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t errand', disabled=True), priority=Item(5)
    ), alias='_Base')


class TaskExpedition(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t expedition', disabled=True), priority=Item(5)
    ), alias='_Base')


class TaskLogin(BaseModel):
    class GroupLogin(BaseModel):
        confirm_time: Item = Item(type='input', value=3)
    
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t login', disabled=True), priority=Item(value=31, disabled=True)
    ), alias='_Base')
    Login: GroupLogin = GroupLogin()


class TaskLogout(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t logout', disabled=True), priority=Item(value=0, disabled=True)
    ), alias='_Base')


class TaskMail(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t mail', disabled=True), priority=Item(value=4)
    ), alias='_Base')


class TaskMission1(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t mission', disabled=True), priority=Item(value=6, disabled=True)
    ), alias='_Base')


class TaskMission2(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t mission', disabled=True), priority=Item(value=2, disabled=True)
    ), alias='_Base')


class TaskSweep(BaseModel):
    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t sweep', disabled=True), priority=Item(3)
    ), alias='_Base')


class TaskWeeklyReward(BaseModel):
    class GroupWeeklyEvent(BaseModel):
        share: Item = Item(type='checkbox', value=True)
        share_time: Item = Item(type='input', value=0.0, hidden=True)

        homo_chest: Item = Item(type='checkbox', value=True)
        homo_chest_time: Item = Item(type='input', value=0.0, hidden=True)

        bp_chest: Item = Item(type='checkbox', value=True)
        bp_chest_time: Item = Item(type='input', value=0.0, hidden=True)

        armada_contribution: Item = Item(type='checkbox', value=True)
        armada_contribution_time: Item = Item(type='input', value=0.0, hidden=True)

    Base: GroupCustomBase = Field(GroupCustomBase(
        command=Item('py main.py -t weekly_reward', disabled=True), priority=Item(1)
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


def gen_i18n(lang: str):
    import anyconfig
    
    trans_path = f"./config/i18n/{lang}.json"
    template_path = "./config/template.json"

    trans = {
        "Project": {
            "tasks": {
                "General": {
                    "groups": {}
                }
            }
        }
    }
    with open(template_path, 'r', encoding='utf-8') as f:
        tpl = anyconfig.load(f)

    for menu_name, menu_conf in tpl.items():
        if menu_name == "Project":
            if "General" in menu_conf.keys():

                group_trans = trans["Project"]["tasks"]["General"]["groups"]
                for group_name, group_conf in menu_conf["General"].items():
                    if group_name == "_Base":
                        continue
                    group_trans[group_name] = {
                            "name": group_name,
                            "help": group_conf.get("_help", {}).get("value", ""),
                            "items": {}
                        }
                    
                    item_trans = group_trans[group_name]["items"]
                    for item_name, item_conf in group_conf.items():
                        if item_name == "_help":
                            continue
                        item_trans[item_name] = {
                                "name": item_name,
                                "help": item_conf.get("help", ""),
                            }
                        for option_name in item_conf.get("option", []):
                            item_trans[item_name].setdefault("options", {})[option_name] = option_name
        else:
            trans[menu_name] = {
                "name": menu_name,
                "tasks": {}
            }

            task_trans = trans[menu_name]["tasks"]
            for task_name, task_conf in menu_conf.items():
                task_trans[task_name] = {
                    "name": task_name,
                    "groups": {}
                }

                group_trans = task_trans[task_name]["groups"]
                for group_name, group_conf in task_conf.items():
                    if group_name == "_Base":
                        continue
                    group_trans[group_name] = {
                        "name": group_name,
                        "help": group_conf.get("_help", {}).get("value", ""),
                        "items": {}
                    }

                    item_trans = group_trans[group_name]["items"]
                    for item_name, item_conf in group_conf.items():
                        if item_name == "_help":
                            continue
                        item_trans[item_name] = {
                            "name": item_name,
                            "help": item_conf.get("help", "")
                        }
                        for option_name in item_conf.get("option", []):
                            item_trans[item_name].setdefault("options", {})[option_name] = option_name

    if Path(trans_path).exists():
        with open(trans_path, 'r', encoding='utf-8') as f:
            old_trans = anyconfig.load(f)
        anyconfig.merge(trans, old_trans)

    with open(trans_path, 'w', encoding='utf-8') as f:
        anyconfig.dump(trans, f, ensure_ascii=False, indent=2, allow_unicode=True)



def export() -> None:
    args = UIContent()
    with open('config/template.json', 'w', encoding='utf-8') as f:
        f.write(args.model_dump_json(indent=2, by_alias=True))


class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        with open('config/template.json', 'r', encoding='utf-8') as f:
            args = json.load(f)
        with open(config_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # 只是为了校验数据
        for menu, tasks in args.items():
            for task, groups in tasks.items():
                for group, items in groups.items():
                    if group == '_Base':
                        continue
                    for item, info in items.items():
                        info['value'] = self.data[menu][task][group][item]
        UIContent.model_validate(args)

    def update(self, menu, task, group, item, value):
        self.data[menu][task][group][item] = value
        with open(self.config_path, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    export()
    gen_i18n('中文')
