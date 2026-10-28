# 风格切换器 · Style Switcher

面向 Codex 与 WorkBuddy 的纯文本娱乐风格 Skill。包含王家卫、周星驰、姜文、冯小刚、古龙、金庸、琼瑶、鲁迅、赵本山、莎士比亚十种风格灵感。

支持单次改写、当前对话常驻、轻/标准/浓三档、风格菜单、状态查询和恢复正常。例句均为原创示意，不代表人物本人发言或现成作品原文。

## 安装包

| 平台 | 文件 | 安装方式 |
| --- | --- | --- |
| WorkBuddy | [style-switcher-workbuddy.zip](dist/style-switcher-workbuddy.zip) | 专家·技能·连接器 → 技能 → 添加技能 → 上传技能，选择此 ZIP |
| Codex | [style-switcher-codex.zip](dist/style-switcher-codex.zip) | 解压，将 `style-switcher` 文件夹放入 `~/.agents/skills/`；仅项目使用则放入 `.agents/skills/` |

Codex 也可复制已生成的 `dist/codex/style-switcher/`。Windows 用户级路径为 `%USERPROFILE%\.agents\skills\style-switcher\`。安装后刷新技能列表；未出现时重启客户端并确认没有安装同名重复副本。

两包的正文与十份风格资料完全相同，元数据按平台分别生成：

- WorkBuddy 包保留官方要求的中英文名称、介绍、版本、作者及案例。
- Codex 包使用标准 `name`、`description`、`metadata`，并包含 `agents/openai.yaml`。
- WorkBuddy 源文件的 `author` 已填写为 GitHub 账号 `zzl92105`；可按投稿署名要求修改后重新打包。

## 使用

安装后，两平台均可直接使用自然语言。Codex 也可显式输入 `$style-switcher`。

```text
列出可选风格。

切换王家卫风格，接下来这段对话都这样说。

用周星驰风格改写这句：我下班了。只改这一次。

这句临时用古龙，之后继续之前的风格：周五18:30上线，预算800元。

切换琼瑶风格，轻一点。

现在是什么风格？

恢复正常。
```

仅提到某个人名、介绍作品或引用文字不会自动切换风格。没有选风格时，Skill 会先请你选择。常驻只指当前对话，不自动保存到其他聊天或全局配置。

本 Skill 不提供自定义斜杠命令注册；如果客户端技能菜单能找到“风格切换器”，也可以从菜单调用。

## 运行条件与边界

- 使用宿主已有文本模型，不需要额外 API、Key、Python、Node、MCP、插件或在线资源。
- 模型需要能读取技能包内的 Markdown 资料；默认每次只读取当前风格的一份资料。
- 本身不调用语音、图像生成，也不写文件保存人设；宿主模型的正常积分或 Token 消耗仍存在。
- 改写保留原意、数字、单位、链接和承诺程度；不为了风格伪造经历、事实或人物名言。
- 代码、命令和机器格式优先保持正确。常驻口吻不会自动改写正式成稿或代码注释。
- 单纯要求“高冷”“话唠”等不属于这十种风格时，不自动猜测对应人物，需用户选定。

## 维护与校验

唯一维护源是 `style-switcher/`。`dist/` 为生成产物；修改源文件后重新运行以下命令。只有开发打包与校验需要 Python 和 PyYAML，安装后的 Skill 不需要这些依赖。

```bash
uv run --with pyyaml python scripts/package_skill.py
uv run --with pyyaml python -m unittest discover -s tests -v
```

没有 uv 时，也可在已安装 PyYAML 的 Python 环境中执行上述两个 Python 命令。无需配置任何模型 API Key。

格式校验与行为检查分别记录：自动测试检查 ZIP 路径、引用完整性、平台字段与正文一致性；模型场景检查记录在 [tests/behavior-check.md](tests/behavior-check.md)。两者不能替代客户端安装测试或长对话稳定性测试。

## 对照规范

- [WorkBuddy 技能规范](https://open.workbuddy.cn/docs/skill)：中文与英文展示字段、案例、版本、作者、目录和 ZIP。
- [OpenAI 官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)：Codex 本地目录、显式调用及 UI 元数据。
- [Agent Skills 规范](https://agentskills.io/specification)：命名、frontmatter、相对资源路径。
