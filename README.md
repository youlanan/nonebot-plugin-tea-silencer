<div align="center">

# nonebot-plugin-tea-silencer
自动化、高自定义的违禁词检测、升级屏蔽级别插件

_✨ 为美好群聊献上屏蔽 ✨_

<img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="python">

</div>

## 🌱 介绍

_高度自定义配置，自动拉黑对着bot不友好人员、群聊_

_自带分类回复词库，可以对新人或惯犯予以不同程度回应_

_从此控制台变得干净又清澈(⑅ōᴗō)۶..._

_该项目仅用于学习交流、维护互联网环境健康和谐_

## 🔧 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    还在开发，没有上传

</details>

<details>
<summary>pip</summary>

    还在开发，没有上传

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["还在开发，没有上传"]

</details>

<details>
<summary>下载源码安装</summary>

    下载仓库源码后, 将 还在开发，没有上传 丢进nb目录下的src/plugin目录下, 确保已正确配置nb可以载入该目录内的插件

</details>

## ✨ 指令
### 指令表
| 指令 | 权限 | 指令前缀 | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| ban、消音 | 超管 | 默认 | 群聊私聊 | 批量屏蔽ID到某时，以空格分隔<br />参数t（Time）g（Group丨可选）u（User丨可选）|
| unban、解除消音 | 超管 | 默认 | 群聊私聊 | 同上，但只有g、u，在字母后附ID即可，输错有示例 |
| - | - | - | - | ... |
### 指令示例

案例一、要屏蔽两个群和一个用户到2025年末（可自行增加四位数字精确到时分）：

    /ban t 20251231 g 801330543 123456 u 3365919215

案例二、要为一个用户解除屏蔽（如果是群聊则可将u换成g，也可以像案例一那样写多个ID，ID之间以空格分隔）：

    /unban u3365919215

案例三、

注：如果给bot配置过指令前缀, 则触发指令为前缀+指令，我这里前缀是默认的“/”，否则参考指令表中格式。

## ⚙️ 配置
- 配置概览：
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

```
### 效果图
暂无

## 🚧 当前计划
- [x] 优化性能
- [x] 基础词库填充
- [x] 超管可以批量屏蔽用户或群
- [x] 超管可以自行增删屏蔽词
- [x] 自动优化屏蔽词库
- [ ] 可供其他插件调用方法
- [ ] 提交至nonebot商店 

## ⚡ 项目参考

直接参考：

>[反嘴臭](https://github.com/tkgs0/nonebot-plugin-antiinsult)

>[指令阻断](https://github.com/KarisAya/nonebot_plugin_matcher_block)

>[文i词库](https://github.com/lgc-NB2Dev/nonebot-plugin-kawaii-robot)

违禁词来源：

>[互联网常用敏感词、停止词词库](https://github.com/fwwdn/sensitive-stop-words)

>[反嘴臭、飞马令相关](https://github.com/tkgs0/nonebot-plugin-antiinsult/tree/main/nonebot_plugin_antiinsult)

_（如果感觉代码很乱或者出现各种问题, 欢迎反馈纠错，期待您的创新~）_
