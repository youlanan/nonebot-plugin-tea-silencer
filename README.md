<div align="center">
  <a href="https://github.com/youlanan/nonebot-plugin-tea-silencer"><img src="https://github.com/youlanan/nonebot-plugin-tea-silencer/blob/main/img/nbp_logo1.png" width="180" height="180" alt="nonebot-plugin-tea-silencer"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-tea-silencer
这是一款用于审查bot接收消息文本的插件，它可以自动拦截用户不友好输入，并为用户与其所在群计算屏蔽等级，以使用户们可以享受不同程度的屏蔽待遇和贴心问候。

_✨ 为美好群聊献上屏蔽 ✨_

<img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="python">

</div>

## 🌱 介绍

_高度自定义配置，自动拉黑对bot不友好发言的人员、群聊_

_自带分类回复词库，可以对新人或惯犯予以不同程度回应_

_适用场景：对用户输入信息安全性有要求时，例如开放平台的bot_

_让你的控制台变干净吧 (⑅ōᴗō)۶..._

_该项目仅用于学习交流、维护互联网环境健康和谐_

## 🔧 安装

本项目目前基于nonebot2与onebotv11协议

测试环境为Python3.12

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

## ⚙️ 配置
- 配置概览：
>以下为插件默认配置，如果您觉得不需要修改，可以不添加。
>
>一般您仅需要注意以下两个配置项：
>
>1.设置 silencer_at 为 True 后，需要@bot发送消息才进行审查
>
>2.若无删除屏蔽词必要也可将 superusers_ignore 设为 False，否则不会审查来自超管的消息。
```
'''消音器相关配置'''

superusers_ignore = True    # 为True忽略超管触发（避免删除屏蔽词被阻断）
silencer_off: bool = False    # 消息检查开关 为True时禁用插件
silencer_at: bool = False    # 为True时必须艾特bot对话才触发

    # 为False时仅在框架正常结束时转存黑名单为json 
    # 这将减少触发频繁时性能开销，但意外情况（如程序崩溃）
    # 会丢失本次运行期间新增的黑名单数据
silencer_safe: bool = True

    # 这是一份被格式化为字符串的json，可以通过它来完全自定义任意数值
    # 需要注意：在json中，当键为数值时必须将其写为一个字符串
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
    # 等级规则：20分贝达成墓土等级，奖励180分钟拉黑
    # 词库分贝：触发对应领域屏蔽词时分别为用户和群聊（如果有）累加分贝数值
    # 回复方案：从分贝达到前面数值开始回复选择的词库随机回复
    # 记忆阈值：达到20分贝则不随框架重启而丢失数据，为用户屏蔽之路再续前缘
    # 群缩放：一个群平均4人被屏蔽，便将该群做同样等级屏蔽
```
### 效果图
<img src="https://github.com/youlanan/nonebot-plugin-tea-silencer/blob/main/img/%E5%90%AF%E5%8A%A8.webp" width="300" height="120" alt="效果图">
<img src="https://github.com/youlanan/nonebot-plugin-tea-silencer/blob/main/img/%E6%8B%A6%E6%88%AA.webp" width="300" height="90" alt="效果图">
<img src="https://github.com/youlanan/nonebot_plugin_megumin/blob/main/img/q.jpg" width="300" height="500" alt="茶话会">

## 🚧 未来计划
- [x] 优化性能
- [x] 基础词库填充
- [x] 超管可以批量屏蔽用户或群
- [x] 超管可以自行增删屏蔽词
- [x] 自动优化屏蔽词库
- [ ] 可供其他插件调用方法
- [ ] 提交至nonebot商店 
- [ ] 适配更多适配器（歪比巴卜？）

## ⚡ 项目参考

直接参考：

>[反嘴臭](https://github.com/tkgs0/nonebot-plugin-antiinsult)

>[指令阻断](https://github.com/KarisAya/nonebot_plugin_matcher_block)

>[文i词库](https://github.com/lgc-NB2Dev/nonebot-plugin-kawaii-robot)

违禁词来源：

>[互联网常用敏感词、停止词词库](https://github.com/fwwdn/sensitive-stop-words)

>[反嘴臭、飞马令相关](https://github.com/tkgs0/nonebot-plugin-antiinsult/tree/main/nonebot_plugin_antiinsult)

_（如果感觉代码很乱或者出现各种问题, 欢迎反馈纠错，期待您的创新~）_
