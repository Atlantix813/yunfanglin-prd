---
name: prd-change-requirement-writing
description: Use when writing or revising a PRD for an existing feature adjustment, especially when old behavior is being replaced, existing pages are being reused, data writes/history handling must be clarified, or the user asks to make an adjustment-type requirement clearer for developers.
---

# PRD Change Requirement Writing

Use this skill for adjustment-type requirements. These are not new feature introductions; they change how an existing feature works.

## Required Order

Write the PRD section in this order:

1. **Business Flow Adjustment**
   - Start with current behavior: `原逻辑：...`
   - Then write the new situation: `新业务场景：...`
   - Then write the required change: `本期调整：...`
   - End with a short numbered summary of what changes.

2. **Data Write And History Handling**
   - Split into sub-sections:
     - `字段说明`
     - `新提交和调整动作处理`
     - `历史数据处理`
   - When field values matter, use `字段=字段值`.
   - Keep old data and new actions separate.

3. **Page Adjustment Description**
   - Split by actual page or window, such as:
     - `列表页`
     - `办理弹窗`
     - `详情弹窗`
   - Table columns should be `页面区域` and `调整内容`.
   - If using an existing window, explicitly write `沿用现有...，不新增...`.

4. **Acceptance**
   - Match the same areas above.
   - Cover old data, new data, user action, page display, and history records.

## Writing Rules

- Do not start an adjustment requirement with field tables. Explain the old behavior and new business need first.
- Do not mix old behavior, new behavior, data writes, and page changes in one paragraph.
- Do not invent new controls. If an old field/window is reused, write it as reused.
- Avoid tables with vague columns like `调整类型`. Use concrete columns such as `页面区域`, `字段`, `动作`, `写入结果`, `历史状态`.
- Write page changes by real page surface. Example: list page, handle dialog, detail dialog.
- Use UI labels with Chinese brackets: `「办理」`, `「问题状态」`.
- For unchanged behavior, write `沿用现有规则`.
- When the user corrects a business rule, treat it as product fact and update the PRD, prototype, overview, and acceptance together.

## Good Pattern

```markdown
### 1. 业务流程调整

原逻辑：...

新业务场景：...

本期调整：...

#### 简要规则

| 序号 | 调整点 | 说明 |
| --- | --- | --- |
| 1 | ... | ... |

### 2. 数据写入与历史处理

#### 字段说明

| 字段 | 说明 |
| --- | --- |
| 当前处理部门 | ... |

#### 新提交和调整动作处理

| 动作 | 写入结果 |
| --- | --- |
| 新提交 | 当前处理部门=...；问题状态=... |

#### 历史数据处理

| 历史状态 | 写入结果 |
| --- | --- |
| 待处理 | 当前处理部门=... |

### 3. 页面调整说明

#### 办理弹窗

| 页面区域 | 调整内容 |
| --- | --- |
| 弹窗窗口 | 沿用现有「办理」弹窗，不新增独立弹窗 |
```

