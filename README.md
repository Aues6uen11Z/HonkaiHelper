# HonkaiHelper
基于图色识别和OCR的PC端崩坏3自动化脚本，先别退坑，刷刷日常凑登录天数吧~

## 功能

> 旧版本功能在新版尚未完全实现，会慢慢补充，目前完成每日活跃任务还是够的

- 挂远征、家园打工
- ~~肝万象虚境锻造材料~~
- 材料活动一键减负
- 领家园金币、凭证奖励、邮件、每日活跃奖励
- ~~戳老婆~~
- ~~买商店每天金币碎片~~
- ~~领每周一次舰团贡献奖励、时序票、吼姆秘宝~~
- 提交舰团委托、领舰团奖励

## 使用方法

### 一键包

尝鲜版图形化一键包现已发布，无需配置python环境，但可能有各种奇妙bug，欢迎[下载体验](https://github.com/Aues6uen11Z/HonkaiHelper/releases)。所用的图形化界面[DaCapo](https://github.com/Aues6uen11Z/DaCapo)与本项目完全独立，是一个通用脚本管理器，如果你有其他脚本想放上来，可以自行查看README了解用法。

解压后点击DaCapo.exe启动程序，进入“总览”修改游戏路径，然后回到主页点击按钮即可开始。

![](./docs/guide.png)

### 从源码构建

1. 克隆本项目或直接下载压缩包并解压
```shell
git clone https://github.com/Aues6uen11Z/HonkaiHelper.git 
```

2. 准备Python环境，建议使用conda的新虚拟环境

```shell
# 安装完anaconda或miniconda后进入shell
# 理论上支持3.6以上任意版本，但目前只测试了3.9
conda create -n zafkiel python==3.9.18
conda activate zafkiel
```

3. 在该环境内安装依赖包

```shell
pip install zafkiel pydantic
```

4. 到项目根目录下的config/config.json修改游戏启动路径
5. 在项目根目录运行main.py

```shell
cd 你的存储路径/HonkaiHelper
python main.py
```

## 注意事项

1. 项目更新有时会涉及到依赖更新，使用时请确保你的zafkiel版本是最新的

   ```shell
   # 在你的虚拟环境内
   pip install --upgrade zafkiel
   ```

2. 理论上可以在任意16:9的分辨率运行，但我目前开发测试都在1280×720窗口模式，求稳请使用720P。

3. 目前新版本尚未开发完全，不能保证在每一个人的电脑上都完美运行，出现问题可以在issue中提出，记得附上日志（网页报告暂时不用，还没有整理，有很多无用信息）

## Todo

- [ ] 常用功能
- [x] 图形化界面
- [ ] 安卓模拟器支持
- [ ] 改进日志和网页报告

## 开发

新版本使用了[Zafkiel](https://github.com/Aues6uen11Z/Zafkiel)库，结合了[Airtest](https://github.com/AirtestProject/Airtest)和[StarRailCopilot](https://github.com/LmeSzinc/StarRailCopilot)的一些优点，目前还有很多地方需要完善，文档后面有时间了会慢慢补上，有兴趣可以先自行阅读源码。
