<div align="center">
  <a href="https://github.com/youlanan/nonebot-plugin-tea-silencer"><img src="https://github.com/youlanan/nonebot-plugin-tea-silencer/blob/main/img/nbp_logo1.webp" width="135" height="135" alt="nonebot-plugin-tea-silencer"></a>
  <a href="https://v2.nonebot.dev/store"><img src="./img/NoneBotPlugin.png" width="300" alt="logo" /></a>
</div>

<div align="center">
nonebot-plugin-tea-silencer

_✨ 为祖安群聊献上屏蔽 ✨_

<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
</div>

## 🌱 介绍

1.消息审查：阻断含有屏蔽词的文本消息。

2.自动拉黑（黑名单）与回复：可针对不同程度嘴臭配置自动屏蔽、回应规则，支持指令拉黑群或用户。

3.文字狱不存在：它并不能阻止用户说脏话，只是拒绝接收。且本插件具有增删屏蔽词的功能，请善用指令。

如果您的bot对用户输入信息安全性有较高要求（例如使用官方bot），则推荐您使用该插件。使用该插件后，您会发现用户平均素质有所提升。

本项目是以学习交流，维护互联网环境健康和谐为目地开发，不接受任何曲解，任何非法滥用本项目所造成的问题开发者概不负责。

## 🔧 安装

本项目目前基于nonebot2与onebotv11协议

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_tea_silencer

</details>

<details>
<summary>使用 pip 安装</summary>

    pip install nonebot_plugin_tea_silencer

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_tea_silencer"]

</details>

<details>
<summary>下载 仓库源码 安装</summary>

    下载仓库源码后, 将 nonebot_plugin_tea_silencer 丢进
    nb目录下的src/plugin目录下, 确保已正确配置nb可以载入该目录内的插件

</details>

## ⚙️ 配置
### 存储位置

>本插件使用商店的 [plugin-localstore](https://github.com/nonebot/plugin-localstore)
>
>默认存储地址请前往其文档查看。
>
>可以自己配置到机器人主目录，方便后续查看或迁移
```
    localstore_cache_dir=
    localstore_config_dir=
    localstore_data_dir=
```
在这个插件里，你通常只需要配置修改 localstore_data_dir=即可

### 配置概览：
>以下为插件配置的默认值，如果您觉得不需要修改，可以不添加。
>
>一般您仅需要注意以下两个配置项：
>
>1.设置 silencer_at 为 True 后，需要@bot发送消息才进行审查
>
>2.若要正常使用删除屏蔽词功能，请将 superusers_ignore 设为 True，否则超管也一样会被屏蔽。
```

    superusers: Set[str] = []                      # NB的超管配置
    superusers_ignore: bool = False                # 是否忽略对超管发言检查
    silencer_off: bool = False                     # 是否禁用插件
    silencer_at: bool = True                       # 是否需要@对话才触发
    silencer_safe: bool = False                    # 是否频繁同步黑名单到本地文件（默认仅程序正常结束运行时储存）
    silencer_data_path: Optional[str] = None       # 自定义的配置路径

    silencer_config = """
    {
        "等级规则": {
            "20": ["暮土", 180],
            "45": ["禁阁", 1440],
            "70": ["伊甸", 7200],
            "100": ["暴风眼", 10800]
        },
        "词库分贝": {
            "广告": 3,
            "涩涩": 5,
            "侮辱": 8,
            "键政": 8,
            "非法": 10
        },
        "回复方案": {
            "0": "提示",
            "10": "棉花",
            "30": "阴阳",
            "45": "飞马"
        },
        "记忆阈值": 20,
        "群缩放": 4
    }
    """
    # silencer_config 是一份字符串化的 JSON
    # 等级规则：20分贝达成墓土等级，奖励180分钟拉黑
    # 词库分贝：当用户或群触发“广告”领域违禁词时，分别增加3分贝
    # 回复方案：当用户分贝达到10开始，使用“棉花”词库作为回复语，直到大于30时切换
    # 记忆阈值：当用户或群分贝达到20时，其有资格
    # 群缩放：一个群平均4人被屏蔽，便将该群做同样等级屏蔽
```

## ✨ 指令
### 指令表
| 指令 | 权限 | 指令前缀 | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| ban丨消音 | 超管 | 默认 | 群聊私聊 | 批量屏蔽ID到某时，以空格分隔<br />参数 t（Time）g（Group丨可选）u（User丨可选）|
| unban丨解除消音 | 超管 | 默认 | 群聊私聊 | 同上，但不需要t参数，详见指令示例↓ |
| addf丨添加消音词 | 超管 | 默认 | 群聊私聊 | 批量向指定的词库添加屏蔽词|
| delf丨删除消音词 | 超管 | 默认 | 群聊私聊 | 直接从所有词库中删除指定词汇 |
### 指令示例

案例一、要屏蔽两个群和一个用户到2025年末（可自行增加四位数字精确到时分）：

    /ban t 20251231 g 801330543 123456 u 3365919215

案例二、要为一个用户解除屏蔽（如果是群聊则可将u换成g，也可以像案例一那样写多个ID，ID之间以空格分隔）：

    /unban u3365919215

案例三、向一个屏蔽词库添加一些新的屏蔽词，屏蔽词之间用空格分离：
>目前支持的[这里](https://github.com/youlanan/nonebot-plugin-tea-silencer/tree/main/nonebot_plugin_tea_silencer/silencer/filter)有的，直接以文件名作为参数，指向对应词库

    /addf 涩涩 xx xxx

案例四、删除某个屏蔽词（会从所有词库中查询并删除这些词汇，谨慎操作哦~）：

    /delf xxx xx

注：如果给bot配置过指令前缀, 则触发指令为前缀+指令，我这里前缀是默认的“/”，否则参考指令表中格式。

### 效果图
<table>
  <tr>
    <td>
      插件效果概览<br>
      <img src="https://github.com/youlanan/nonebot-plugin-tea-silencer/blob/main/img/%E5%90%AF%E5%8A%A8.webp" width="300" height="120" alt="效果图"><br>
      <img src="https://github.com/youlanan/nonebot-plugin-tea-silencer/blob/main/img/%E6%8B%A6%E6%88%AA.webp" width="300" height="60" alt="效果图"><br>
      <img src="https://github.com/youlanan/nonebot-plugin-tea-silencer/blob/main/img/1.png" width="300" height="210" alt="效果图">
    </td>
    <td>
      加群一起玩耍<br>
      <img src="https://github.com/youlanan/nonebot_plugin_megumin/blob/main/img/q.jpg" width="300" height="500" alt="茶话会">
    </td>
  </tr>
</table>


## 🚧 未来计划
- [x] 优化性能
- [x] 基础词库填充
- [x] 超管可以批量屏蔽用户或群
- [x] 超管可以自行增删屏蔽词
- [x] 自动优化屏蔽词库
- [ ] 可供其他插件调用方法（有空写，如果是为了检查待发送信息，不如用[这个插件](https://github.com/MelodyKnit/nonebot-plugin-blockwords)）
- [ ] 提交至nonebot商店 （延期，去学数据库插件）
- [ ] 具有管理权限时禁言（一千年以后）
- [ ] 适配更多适配器（三千年以后）

## ⚡ 项目参考

直接参考：

>[反嘴臭](https://github.com/tkgs0/nonebot-plugin-antiinsult)

>[指令阻断](https://github.com/KarisAya/nonebot_plugin_matcher_block)

>[文i词库](https://github.com/lgc-NB2Dev/nonebot-plugin-kawaii-robot)

违禁词来源：

>[互联网常用敏感词、停止词词库](https://github.com/fwwdn/sensitive-stop-words)

>[反嘴臭、飞马令相关](https://github.com/tkgs0/nonebot-plugin-antiinsult/tree/main/nonebot_plugin_antiinsult)

_（本人没有系统学习过py，如果感觉代码很乱或者出现各种问题, 欢迎反馈纠错~）_
