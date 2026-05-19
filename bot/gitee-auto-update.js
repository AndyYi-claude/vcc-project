/**
 * VCC 任务完成自动更新 — 企微机器人代码工具版
 * 直接通过 Gitee API 更新 Markdown 文件，无需 GitHub。
 *
 * 使用方式：机器人接收到 "完成了XX" 消息后，调用此函数。
 * 参数：taskName (任务名), completedBy (完成人)
 *
 * 前置条件：机器人平台需支持 fetch / HTTP 请求。
 */

const GITEE_TOKEN = "cb417d388c32efed5b88d14ee9060365";
const REPO = "AndyYi98/vcc-project";
const API = "https://gitee.com/api/v5/repos/" + REPO + "/contents";
const FILES = ["01-dashboard.md", "02-tasks.md"];
const TIMELINE = "05-timeline.md";

// 获取今天的日期字符串
function todayStr() {
  const d = new Date();
  const pad = n => String(n).padStart(2, '0');
  return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
}

// 从 Gitee API 读取文件
async function readFile(path) {
  const url = API + '/' + path + '?access_token=' + GITEE_TOKEN;
  const res = await fetch(url);
  if (!res.ok) throw new Error('读取失败: ' + path + ' HTTP ' + res.status);
  const json = await res.json();
  return {
    content: atob(json.content),  // base64 解码
    sha: json.sha
  };
}

// 写回 Gitee（base64 编码 + SHA）
async function writeFile(path, content, sha, message) {
  const body = new URLSearchParams();
  body.append('access_token', GITEE_TOKEN);
  body.append('content', btoa(unescape(encodeURIComponent(content))));  // UTF-8 safe base64
  body.append('sha', sha);
  body.append('message', message);

  const res = await fetch(API + '/' + path, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  });
  if (!res.ok) throw new Error('写入失败: ' + path + ' HTTP ' + res.status);
  return await res.json();
}

// 在 Markdown 表格中标记任务完成
function markTaskDone(md, taskName, date) {
  const lines = md.split('\n');
  let found = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.includes('| ○ |') && line.includes(taskName)) {
      // ○ → ✓，填充进展列
      const cols = line.split('|').map(c => c.trim());
      cols[1] = '✓';
      if (cols[3] === '' || cols[3] === undefined) cols[3] = date + ' 完成';
      lines[i] = '| ' + cols.slice(1).join(' | ') + ' |';
      found = true;
      break;
    }
  }
  // 从 DDL 预警中移除
  const newLines = [];
  let inDDL = false;
  for (const line of lines) {
    if (line.includes('DDL 预警') || line.includes('## DDL')) inDDL = true;
    if (inDDL && line.startsWith('|---')) { inDDL = false; newLines.push(line); continue; }
    if (inDDL && line.includes(taskName)) continue; // 跳过已完成任务的 DDL 行
    newLines.push(line);
  }
  return { md: newLines.join('\n'), found };
}

// 更新时间线
function addTimeline(md, taskName, completedBy, date) {
  const entry = '| ✅ 任务 | ' + taskName + ' 完成（' + completedBy + '） |\n';
  const dayHeader = '## ' + date;
  if (md.includes(dayHeader)) {
    // 在当天分区插入
    const pattern = dayHeader + '\n\n| 类型 | 事件 |\n|---|---|';
    return md.replace(pattern, pattern + '\n' + entry);
  } else {
    // 新建当天分区（在图例前插入）
    const section = dayHeader + '\n\n| 类型 | 事件 |\n|---|---|\n' + entry;
    return md.replace('\n## 图例', '\n' + section + '\n## 图例');
  }
}

// 主流程
async function onTaskComplete(taskName, completedBy) {
  const date = todayStr();
  const results = [];

  // 1. 更新看板和任务表
  for (const file of FILES) {
    const { content, sha } = await readFile(file);
    const { md, found } = markTaskDone(content, taskName, date);
    if (found) {
      await writeFile(file, md, sha, '自动：' + completedBy + ' 完成「' + taskName + '」');
      results.push(file);
    }
  }

  if (results.length === 0) {
    // 列出所有未完成任务
    const { content } = await readFile('02-tasks.md');
    const open = content.split('\n').filter(l => l.includes('| ○ |'));
    return {
      success: false,
      message: '未找到匹配任务：「' + taskName + '」。当前未完成任务：\n' + open.map(l => '  · ' + l.split('|')[2].trim()).join('\n')
    };
  }

  // 2. 更新时间线
  const { content: tlMd, sha: tlSha } = await readFile(TIMELINE);
  const newTl = addTimeline(tlMd, taskName, completedBy, date);
  await writeFile(TIMELINE, newTl, tlSha, '时间线：' + completedBy + ' 完成「' + taskName + '」');

  return {
    success: true,
    message: '✅ 已记录：' + completedBy + ' 完成「' + taskName + '」\n看板已更新：https://gitee.com/AndyYi98/vcc-project/blob/main/01-dashboard.md',
    updatedFiles: results
  };
}

// 导出（机器人平台按需调用）
if (typeof module !== 'undefined') module.exports = { onTaskComplete };
