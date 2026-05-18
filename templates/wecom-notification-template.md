# 企业微信通知模板

> **状态：暂未启用**（企业微信机器人当前不可用，待后续配置后启用）
>
> 启用后用于 Claude Code 生成通知内容，PM 审阅后通过 PowerShell 推送到企业微信群机器人

---

## 群机器人 Webhook 信息

- Webhook URL：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={你的key}`
- 发送方式：PowerShell `Invoke-RestMethod`

---

## 模板 1：DDL 预警（单条）

```markdown
## ⚠️ DDL 预警
> 事项：**{事项名称}**
> DDL：**{日期}**（剩余 {N} 天）
> 负责人：<@{负责人}>
> 状态：{🟡/🔴}
> 备注：{补充说明}
```

---

## 模板 2：DDL 预警（多条汇总）

```markdown
## ⚠️ 本周 DDL 预警（{日期范围}）

| DDL | 事项 | 负责人 | 剩余 |
|-----|------|--------|------|
| {日期} | {事项} | @{人} | {N}天 |
| {日期} | {事项} | @{人} | {N}天 |

> 详细进度见[项目看板]({gitee_url})
```

---

## 模板 3：周报推送

```markdown
## 📊 VCC 项目周报（{日期范围}）

### 本周完成
- ✅ {事项1}
- ✅ {事项2}

### 下周计划
- 📋 {事项1}（DDL: {日期}）
- 📋 {事项2}（DDL: {日期}）

### 需要关注
- {风险/阻塞事项}

---
> PM：Andy | 完整周报见[项目看板]({gitee_url})
```

---

## 模板 4：里程碑完成通知

```markdown
## ✅ 里程碑达成
> **{里程碑名称}** 已完成！
> 负责人：<@{负责人}>
> 下一阶段：{下一里程碑}
> 预计时间：{日期}

> 进度概览：已完成 {N}/{总数} 个里程碑
```

---

## 模板 5：紧急升级通知

```markdown
## 🔴 紧急升级
> **{问题描述}**
> 影响：{影响范围}
> 需决策人：<@{决策人}>
> 建议期限：{日期}

> 详情见[风险与问题]({gitee_url})
```

---

## PowerShell 发送脚本

```powershell
$webhookUrl = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={你的key}"

$body = @{
    msgtype = "markdown"
    markdown = @{
        content = @"
## ⚠️ DDL 预警
> 事项：**JPM托管户KYC启动**
> DDL：**2026-05-25**（剩余 3 天）
> 负责人：<@Kevin>
> 状态：🟡
"@
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $body -ContentType "application/json; charset=utf-8"
```
