"""VCC task completion handler. Called by GitHub Actions workflow_dispatch."""
import sys, re, os, subprocess
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
FILES = ["01-dashboard.md", "02-tasks.md"]
TIMELINE = "05-timeline.md"


def find_and_update(filepath, task_name, today_str):
    """Find task by name and mark it done. Returns (changed, task label)."""
    lines = open(filepath, encoding="utf-8").readlines()
    changed = False
    task_label = task_name
    for i, line in enumerate(lines):
        # Match: | ○ | {task_name} | ... |
        m = re.match(r'\| ○ \| (.+?) \|', line)
        if m:
            label = m.group(1).strip()
            if task_name in label or label in task_name:
                task_label = label
                # Replace ○ → ✓, add completion date to progress col if empty
                cols = line.strip().split('|')
                new_cols = []
                for j, c in enumerate(cols):
                    c = c.strip()
                    if j == 0 and c == '○':
                        c = '✓'
                    # Update progress column (index 3 in the table) if empty
                    if j == 3 and (not c or c == ''):
                        c = f'{today_str} 完成'
                    new_cols.append(c)
                lines[i] = '| ' + ' | '.join(new_cols) + ' |\n'
                changed = True
                break
    if changed:
        open(filepath, "w", encoding="utf-8").writelines(lines)
    return changed, task_label


def add_timeline_entry(task_label, completed_by, today_str, today_iso):
    """Prepend completion event to timeline."""
    content = open(TIMELINE, encoding="utf-8").read()
    # Find the first event section after the header
    marker = "## " + today_str.split("-")[0]  # e.g. "## 2026"
    # Insert after the day's date line
    new_entry = (
        f'\n'
        f'| ✅ 任务 | {task_label} 完成（{completed_by}） |\n'
    )
    # Find today's section or create one
    day_header = f'## {today_str}'
    if day_header in content:
        # Insert after the day header's table header row
        content = content.replace(
            day_header + '\n\n| 类型 | 事件 |',
            day_header + '\n\n| 类型 | 事件 |' + new_entry
        )
    else:
        # Create new day section before the 图例 section
        new_section = (
            f'\n## {today_str}\n\n'
            f'| 类型 | 事件 |\n'
            f'|---|---|\n'
            f'{new_entry}'
        )
        content = content.replace('\n## 图例', new_section + '\n\n## 图例')
    open(TIMELINE, "w", encoding="utf-8").writelines(content)


def main():
    task_name = os.environ.get("TASK_NAME", sys.argv[1] if len(sys.argv) > 1 else "")
    completed_by = os.environ.get("COMPLETED_BY", sys.argv[2] if len(sys.argv) > 2 else "未知")
    if not task_name:
        print("Usage: task_complete.py <task_name> [completed_by]")
        sys.exit(1)

    now = datetime.now(TZ)
    today_str = now.strftime("%Y-%m-%d")
    today_iso = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

    updated = False
    task_label = task_name
    for f in FILES:
        changed, label = find_and_update(f, task_name, today_str)
        if changed:
            updated = True
            task_label = label

    if updated:
        add_timeline_entry(task_label, completed_by, today_str, today_iso)
        print(f"Updated: {task_label}")
    else:
        print(f"Task not found: {task_name} (partial match attempted)")
        # Try to list similar tasks
        for f in FILES:
            lines = open(f, encoding="utf-8").readlines()
            for line in lines:
                if '| ○ |' in line:
                    print(f"  Open task: {line.strip()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
