# project-kickstart

一键生成项目管理看板。从 VCC 项目管理体系提炼。

## 使用方式

### 方法 A：Claude Code 交互式

```
/project-kickstart
```

Claude 会逐一问你项目信息，你回答就行。

### 方法 B：配置文件

```bash
# 1. 复制模板
cp templates/project-config.yaml my-project.yaml

# 2. 编辑填写你的项目信息
# 3. 执行
/project-kickstart --config my-project.yaml
```

## 生成的产物

| 文件 | 说明 |
|---|---|
| `dashboard.html` | 交互仪表盘——待办、进展总览、流程进度、时间线、关键决策 |
| `01-dashboard.md` | Markdown 看板（国内 Gitee 可读） |
| `02-tasks.md` | 任务分配表 |
| `03-communications.md` | 沟通日志 |
| `04-risks.md` | 风险追踪 |
| `05-timeline.md` | 时间线 |
| `README.md` | 项目入口说明 |
| `.github/workflows/pages.yml` | 自动部署到 GitHub Pages |

## 仪表盘功能

- **标签切换**：看板 / 架构图
- **DDL 预警**：顶部紧急事项提醒
- **待办列表**：按人分组，可勾选标记完成
- **进展总览**：右栏多模块状态追踪
- **流程进度**：6 阶段进度条
- **时间线**：项目历史事件记录
- **响应式**：手机/电脑均可

## 配置模板说明

见 `templates/project-config.yaml`。只需填写：

1. `project` — 项目名、PM、日期
2. `team` — 团队成员
3. `tasks` — 每人待办
4. `phases` — 6 个阶段的步骤
5. `decisions` — 关键决策
6. `progress_sections` — 右栏进展区块
7. `github` — GitHub 用户名和仓库名

## 来源

本 skill 提炼自诺亚新加坡 VCC 设立项目的实战管理经验。
