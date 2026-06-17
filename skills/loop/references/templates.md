# @loop File Templates

Copy these templates exactly when creating state files. Do not deviate from the format — consistency enables cross-session resume.

---

## .loop/.gitignore

Create this at `.loop/.gitignore` on the very first loop run in any project.

```
# Loop state files — development artifacts, not committed
*
!.gitignore
```

---

## Manifest Template

**File**: `.loop/<task-slug>/manifest.md`

```markdown
# Loop Task: <task-slug>

- **Task**: <verbatim user request or clean summary>
- **Mode**: standard | strict
- **Max Iterations**: 20
- **Checkpoint Every**: 5 iterations
- **Started**: <YYYY-MM-DD HH:MM>
- **Finished**: <YYYY-MM-DD HH:MM or "running">
- **Status**: running | converged | stuck | aborted | max-reached

## Success Criteria

1. [ ] <criterion — must be verifiable, not subjective>
2. [ ] <criterion>
3. [ ] <criterion>
4. [ ] <criterion — add more as needed, 3-7 total>

## Scope

**In scope:**
- <specific thing 1>
- <specific thing 2>

**Out of scope:**
- <thing explicitly excluded>
- <thing explicitly excluded>

## Progress

| Iter | Focus | Issues Found | Issues Fixed | Remaining | Verdict |
|------|-------|-------------|-------------|-----------|---------|
| 1    |       |             |             |           |         |

## Stuck Tracker

| Issue | First Seen | Consecutive Iters | Approach Changes | Resolved? |
|-------|-----------|-------------------|-----------------|-----------|
```

---

## Iteration Log Template

**File**: `.loop/<task-slug>/iteration-<NN>.md`

Use zero-padded two-digit numbers: `iteration-01.md`, `iteration-02.md`, etc.

```markdown
# Iteration <NN>

- **Timestamp**: <YYYY-MM-DD HH:MM>
- **Focus**: <one-line description of this iteration's focus>
- **Mode**: <standard|strict>

## What Was Executed

<describe what you actually did — commands run, code written, tests executed>

## Results

### ✅ Passed
- <thing that worked correctly>
- <thing that worked correctly>

### ❌ Failed
- 🔴 **CRITICAL**: <description> — <file:line if applicable>
- 🟠 **HIGH**: <description> — <file:line if applicable>
- 🟡 **MEDIUM**: <description> — <file:line if applicable>
- 🟢 **LOW**: <description> — <file:line if applicable>

### ⚠️ Warnings (not failures, but noteworthy)
- <observation>

## Edge Cases Tested This Iteration
- <edge case 1> → <PASS|FAIL> — <detail>
- <edge case 2> → <PASS|FAIL> — <detail>

## New Edge Cases Identified (queue for next iteration)
- <edge case to test next>
- <edge case to test next>

## Fixes Applied

### Fix 1: <short title>
- **Issue**: <what was wrong>
- **Root Cause**: <why it was wrong>
- **Fix**: <what was changed>
- **Files Modified**: <file paths>
- **Verified**: <yes/no — did you confirm the fix works>
- **Regression Check**: <yes/no — did previously passing things still pass>

### Fix 2: <short title>
- **Issue**: <what was wrong>
- **Root Cause**: <why it was wrong>
- **Fix**: <what was changed>
- **Files Modified**: <file paths>
- **Verified**: <yes/no>
- **Regression Check**: <yes/no>

## Convergence Check

- Success criteria met: <N> / <total>
- New issues this iteration: <count>
- Issues remaining: <count>
- **Verdict**: <PASS — all clear | PARTIAL — progress made | FAIL — regression or stuck>
- **Next iteration focus**: <what to focus on next, or "CONVERGED" if done>
```

---

## Checkpoint Report Template

**Show to user at iterations 5, 10, 15.**

```markdown
## 🔄 Loop Checkpoint — Iteration <N>/20

**Task**: <task description>
**Mode**: <standard|strict>

### Progress So Far
- Iterations completed: <N>
- Total issues found: <count across all iterations>
- Total issues fixed: <count>
- Remaining issues: <count>

### Success Criteria Status
1. [x] <met criterion>
2. [ ] <unmet criterion — why>
3. [x] <met criterion>

### Trend Analysis
- **Trend**: <improving — issues decreasing | plateau — same count | degrading — issues increasing>
- **Velocity**: <issues fixed per iteration average>
- **Estimated remaining iterations**: <N>

### Top Remaining Issues
1. <most important unresolved issue>
2. <second most important>

### Recommendation
<continue — on track | adjust — suggest scope change | escalate — need user input on X>

---

**Continue looping? (y/n)**
```

---

## Summary Template

**File**: `.loop/<task-slug>/summary.md`

```markdown
# Loop Summary: <task-slug>

## Result: ✅ CONVERGED | ⚠️ MAX REACHED | ❌ ABORTED

- **Task**: <what was done>
- **Mode**: <standard|strict>
- **Iterations Used**: <N> / 20
- **Total Issues Found**: <count>
- **Total Issues Fixed**: <count>
- **Started**: <timestamp>
- **Finished**: <timestamp>

## Convergence Path

| Iter | Focus | Found | Fixed | Remaining | Verdict |
|------|-------|-------|-------|-----------|---------|
| 1    |       |       |       |           |         |
| 2    |       |       |       |           |         |
| 3    |       |       |       |           |         |

## Success Criteria — Final Status

1. [x] <criterion 1> — verified at iteration <N>
2. [x] <criterion 2> — verified at iteration <N>
3. [x] <criterion 3> — verified at iteration <N>

## All Fixes Applied

| # | Iter | Issue | Severity | Root Cause | Fix | Files Changed |
|---|------|-------|----------|-----------|-----|---------------|
| 1 | 1    |       | 🔴      |           |     |               |
| 2 | 1    |       | 🟠      |           |     |               |
| 3 | 2    |       | 🟡      |           |     |               |

## Edge Cases Verified

| Edge Case | Iteration Tested | Result |
|-----------|-----------------|--------|
| <case 1>  | 3               | ✅ PASS |
| <case 2>  | 4               | ✅ PASS |

## Stuck Episodes

| Issue | Iters Stuck | Approach Change | Resolution |
|-------|------------|----------------|------------|
| <issue> | 3        | <what was tried differently> | <how it was resolved> |

## Lessons Learned

- <pattern discovered during the loop>
- <what made this task tricky>
- <what would make it faster next time>

## Recommendations

- <follow-up action if any>
- <monitoring or regression test suggestion>
```

---

## Stuck Escalation Template

**Show to user when stuck for 3+ iterations AND alternative approach failed.**

```markdown
## ⚠️ STUCK — Requesting Input

**Issue**: <description of the persistent issue>
**Stuck since**: Iteration <N> (<count> consecutive iterations)

### Approaches Tried
1. **Iteration <N>**: <approach 1> — ❌ <why it failed>
2. **Iteration <N+1>**: <approach 2> — ❌ <why it failed>
3. **Iteration <N+2>**: <alternative approach> — ❌ <why it failed>

### Root Cause Hypothesis
<your best guess at why this keeps failing>

### What I Need From You
- <specific question 1>
- <specific question 2>
- <possible direction: "Should I try X instead?">
```
