# project-kickstart

Generate a complete project management dashboard from a simple config. Produces a GitHub Pages-hosted interactive dashboard with TODO tracking, progress overview, process flow, timeline, and team management.

## How to invoke

```
/project-kickstart
```

Or with a pre-written config:

```
/project-kickstart --config path/to/config.yaml
```

## Workflow

### Step 0: Choose deployment mode

Ask the user FIRST:

> "看板生成后，你想怎么分享给同事？"

| 选项 | 适用场景 | 需要什么 |
|---|---|---|
| **A · Gitee 托管**（推荐国内） | 国内团队、免翻墙、免费 | Gitee 账号（1分钟注册） |
| **B · GitHub Pages** | 新加坡/海外团队 | GitHub 账号 |
| **C · 纯本地** | 仅自己看、或发文件给同事 | 什么都不需要 |

根据选择调整后续步骤：
- 选 A：部署到 Gitee，提供 Gitee blob URL + 本地 dashboard.html
- 选 B：部署到 GitHub Pages，提供在线交互版链接
- 选 C：只生成本地文件，dashboard.html 浏览器直接打开即可用

Ask the user these questions interactively (one at a time or in groups):

1. **Project basics**: name, subtitle (one-line description), PM name, start date
2. **Team**: for each member — name, role, short avatar label (1-2 chars), responsibilities
3. **Priorities**: ordered list of what's urgent right now (e.g. "银行开户 > 结构设计 > 文件起草")
4. **Tasks**: for each person — what they're doing, status (todo/wip/done), DDL, priority (red/yellow/green/blue)
5. **Phases**: P0-P6 phases, each with steps (status + name + owner)
6. **Key decisions**: list of decisions made
7. **Progress sections**: named sections with table rows (for the right panel overview)
8. **GitHub username**: for Pages URL generation

### Step 2: Generate config file

Save a `project-config.yaml` in the project directory so the setup can be reproduced.

### Step 3: Generate project files

Create this structure under the project directory:

```
project/
├── dashboard.html          # Interactive dashboard
├── README.md               # Entry guide
├── 01-dashboard.md         # Markdown dashboard
├── 02-tasks.md             # Markdown task list
├── 03-communications.md    # Communication log template
├── 04-risks.md             # Risk tracking template
├── 05-timeline.md          # Timeline template
└── .github/workflows/
    └── pages.yml           # Auto-deploy to GitHub Pages
```

Use the HTML template in `templates/dashboard.html`. Replace all `{{PLACEHOLDER}}` values with user-provided data.

### Step 4: Deploy

#### Option A · Gitee（推荐国内）

1. 帮用户注册 Gitee（如未注册）：gitee.com/signup
2. 在 Gitee 上创建**公开**仓库
3. `git init && git checkout -b main`
4. `git add -A && git commit -m "project kickstart"`
5. `git remote add origin https://gitee.com/USER/REPO.git`
6. `git push -u origin main`
7. 输出 Markdown 看板链接：`https://gitee.com/USER/REPO/blob/main/01-dashboard.md`
8. 提醒：dashboard.html 需下载到本地用浏览器打开（Gitee 不托管 HTML Pages）

#### Option B · GitHub Pages

1. `git init && git checkout -b main`
2. `git add -A && git commit -m "project kickstart"`
3. 创建 GitHub 公开仓库
4. `git remote add origin https://github.com/USER/REPO.git`
5. `git push -u origin main`
6. 输出：`https://USER.github.io/REPO/dashboard.html`
7. GitHub Pages 自动部署（等待约30秒）

#### Option C · 纯本地

1. 不初始化 Git，文件直接生成在项目目录
2. 告诉用户：双击 `dashboard.html` 即可在浏览器打开
3. 分享方式：把整个文件夹压缩发同事，或放到共享网盘

### Step 5: Handover

根据部署方式告诉用户：
- **看板链接**（A 为 Gitee blob URL，B 为 GitHub Pages URL，C 为本地文件路径）
- **如何更新**：「在 Claude Code 中告诉 PM 更新任务，Claude 会改文件并 push（A/B）/ 保存本地（C）」
- 后续可选：加企业微信机器人自动更新、加 Gitee 镜像

## Dashboard features

The generated dashboard includes:
- Tab switcher (Dashboard / Architecture diagram)
- DDL warning cards at top
- Left: TODO list by person, with checkboxes and status indicators
- Right: Progress overview sections
- Below: 6-phase process flow with progress bars
- Timeline section
- Key decisions section
- Responsive design (mobile-friendly)
- Architecture tab (user can replace the placeholder iframe with their own diagram)

## Important notes

- Keep generated dashboard content in sync with markdown files
- All user data must be properly escaped for HTML
- The GitHub repo must be PUBLIC for GitHub Pages to work on free tier
- Remind users they can later add: enterprise WeChat bot automation, Gitee mirror for China access
