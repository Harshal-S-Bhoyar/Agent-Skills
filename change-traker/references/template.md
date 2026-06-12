---
description: >-
  Standard Markdown entry template for recording code changes using `change-traker`.
metadata:
  tags: [template, markdown, changelog]
  source: internal
---

# `change-traker` Entry Template

Use the following template for every entry added to the changelog. Copy, fill out, and append or prepend this format exactly.

```markdown
## [YYYY-MM-DD HH:MM:SS TZ] - Task/Issue Title or ID

> [!NOTE]
> **Change Type:** [Feature | Bug Fix | Refactor | Test | Hybrid]
> **Status:** [Complete | Partial | Uncertain]
> **Target Files:**
> - `relative/path/to/file_one.ext`
> - `relative/path/to/file_two.ext`

### 🔍 Context & Objective
* **Why this change?** [Brief explanation of the rationale and motivation]
* **What problem is solved?** [Clear explanation of the problem, error, or gap being addressed]

### 🛠️ Implementation Summary
- [ ] [Concise, action-oriented bullet point describing the change]
- [ ] [Concise, action-oriented bullet point describing the change]

### 🔄 Code Differences (Before vs After)

#### 📄 `relative/path/to/file_one.ext`
```diff
- [Old code line 1]
- [Old code line 2]
+ [New code line 1]
+ [New code line 2]
```

#### 📄 `relative/path/to/file_two.ext`
```diff
- [Old code line 1]
+ [New code line 1]
```

---
```
