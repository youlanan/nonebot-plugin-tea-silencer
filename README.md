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

## ⚙️ 配置
- 配置说明：还在开发，不确定能不能正确解析

## ✨ 指令
### 指令表
| 指令 | 权限 | 指令前缀 | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| ban、消音 | 超管 | 默认 | 群聊私聊 | 批量屏蔽到某时<br />参数t（Time）g（Group）u（User）<br />例如 /ban t20251231 g801330543 u3365919215 |
| uban、解除消音 | 超管 | 默认 | 群聊私聊 | 同上，但只有g、u，在字母后附ID即可，输错有示例 |
| - | - | - | - | ... |

注：如果给bot配置过指令前缀, 则触发指令为前缀+指令, 例如 /爆裂魔法
### 效果图
暂无

## 🚧 当前计划
- [x] 优化性能
- [x] 基础词库填充
- [x] 超管可以批量屏蔽用户或群
- [ ] 超管可以自行增删屏蔽词
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
