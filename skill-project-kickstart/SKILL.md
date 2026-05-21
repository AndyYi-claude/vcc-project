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

### Step 1: Gather project information

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

1. `git init && git checkout -b main`
2. `git add -A && git commit -m "project kickstart"`
3. Create GitHub repo (public) via API or gh CLI
4. `git remote add origin https://github.com/USER/REPO.git`
5. `git push -u origin main`
6. Output: `https://USER.github.io/REPO/dashboard.html`

### Step 5: Handover

Tell the user:
- GitHub Pages URL (interactive dashboard, requires no VPN for Singapore colleagues)
- How to update: "in Claude Code, tell the PM to update tasks and push"
- Optionally create a Gitee mirror for China access

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
