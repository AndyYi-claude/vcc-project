"""VCC task completion handler. Called by GitHub Actions workflow_dispatch."""
import sys, re, os
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
FILES = ["01-dashboard.md", "02-tasks.md"]
TIMELINE = "05-timeline.md"


def find_and_update(filepath, task_name, today_str):
    """Mark task as done in table rows. Returns (changed, task_label)."""
    lines = open(filepath, encoding="utf-8").readlines()
    changed = False
    task_label = task_name
    for i, line in enumerate(lines):
        m = re.match(r'\| ○ \| (.+?) \|', line)
        if m:
            label = m.group(1).strip()
            if task_name in label or label in task_name:
                task_label = label
                cols = [c.strip() for c in line.strip().split('|')]
                # cols[0] is empty (leading |), cols[1] is ○
                cols[1] = '✓'
                # Fill progress column (index 3) if empty
                if len(cols) > 3 and (cols[3] == '' or cols[3] == ' '):
                    cols[3] = f'{today_str} 完成'
                lines[i] = '| ' + ' | '.join(cols) + ' |\n'
                changed = True
                break
    if changed:
        # Also remove from DDL section if present
        lines = remove_from_ddl(lines, task_label)
        open(filepath, "w", encoding="utf-8").writelines(lines)
    return changed, task_label


def remove_from_ddl(lines, task_label):
    """Remove completed task from DDL预警 section."""
    result = []
    skip = False
    for line in lines:
        if task_label in line and ('DDL' in ''.join(result[-10:]) or '预警' in ''.join(result[-10:])):
            if re.match(r'\|.*\|.*\|.*\|', line):  # DDL table row
                skip = True
                continue
        result.append(line)
    return result


def add_timeline_entry(task_label, completed_by, today_str):
    """Add completion event to timeline."""
    content = open(TIMELINE, encoding="utf-8").read()
    day_header = f'## {today_str}'
    new_row = f'| ✅ 任务 | {task_label} 完成（{completed_by}） |\n'

    if day_header in content:
        # Insert new row right after the table header row (which has |---|---|)
        pattern = day_header + '\n\n| 类型 | 事件 |\n|---|---|'
        replacement = day_header + '\n\n| 类型 | 事件 |\n|---|---|\n' + new_row
        content = content.replace(pattern, replacement)
    else:
        new_section = (
            f'\n{day_header}\n\n'
            f'| 类型 | 事件 |\n'
            f'|---|---|\n'
            f'{new_row}'
        )
        content = content.replace('\n## 图例', new_section + '\n## 图例')
    open(TIMELINE, "w", encoding="utf-8").writelines(content)


def main():
    task_name = os.environ.get("TASK_NAME", sys.argv[1] if len(sys.argv) > 1 else "")
    completed_by = os.environ.get("COMPLETED_BY", sys.argv[2] if len(sys.argv) > 2 else "未知")
    if not task_name:
        print("Usage: task_complete.py <task_name> [completed_by]")
        sys.exit(1)

    now = datetime.now(TZ)
    today_str = now.strftime("%Y-%m-%d")

    updated = False
    task_label = task_name
    for f in FILES:
        changed, label = find_and_update(f, task_name, today_str)
        if changed:
            updated = True
            task_label = label

    if updated:
        add_timeline_entry(task_label, completed_by, today_str)
        print(f"Updated: {task_label}")
    else:
        print(f"Task not found: {task_name}")
        for f in FILES:
            for line in open(f, encoding="utf-8"):
                if '| ○ |' in line:
                    print(f"  Open: {line.strip()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
