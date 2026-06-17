---
name: loop
description: Autonomous self-improving execution loop. Forces agent into iterative cycles of execute→evaluate→fix→retest until task converges to perfection. Tracks all progress in .loop/ folder.
---

# @loop — Autonomous Self-Improving Execution Loop

Force yourself into an iterative execution loop that keeps running until the task is done **flawlessly**. You execute, evaluate, find problems, fix them, and re-execute — progressively testing harder edge cases each iteration.

> **This is not optional guidance. When @loop is invoked, you MUST follow this protocol exactly. Do not skip steps. Do not exit the loop early unless convergence criteria are met.**

---

## Invocation

```
use @loop to <task description>
use @loop -strict to <task description>
```

### Modes

| Mode | Flag | Behavior |
|---|---|---|
| **Standard** | `@loop` (no flag) | Fixes critical and high issues. Accepts minor/cosmetic issues. Converges when core functionality works correctly. |
| **Strict** | `@loop -strict` | Zero tolerance. Fixes ALL issues including minor, cosmetic, and edge cases. Converges only when absolutely perfect. |

---

## Loop Protocol

### Phase 0 — Initialize

Before the first iteration, do these steps exactly:

1. **Parse the task**: Extract what the user wants done from their prompt.
2. **Detect mode**: Check for `-strict` flag. Default to `standard` if absent.
3. **Define success criteria**: Write 3-7 concrete, verifiable conditions that define "done". These are your convergence targets.
4. **Create state folder**: Create `.loop/<task-slug>/` in the project root.
5. **Write manifest**: Create `.loop/<task-slug>/manifest.md` with task definition.

**Manifest format:**

```markdown
# Loop Task: <task-slug>

- **Task**: <what the user asked>
- **Mode**: standard | strict
- **Max Iterations**: 20
- **Checkpoint Every**: 5 iterations
- **Started**: <timestamp>
- **Status**: running | converged | stuck | aborted

## Success Criteria

1. [ ] <criterion 1>
2. [ ] <criterion 2>
3. [ ] <criterion 3>
...

## Progress Summary

| Iter | Issues Found | Issues Fixed | Status |
|------|-------------|-------------|--------|
```

---

### Phase 1 — Execute (Each Iteration)

For **every** iteration, follow this exact sequence:

#### Step 1: Execute the Task

Do the work. This depends on what the task is:

- **Testing a feature** → Run the feature through test cases. Start with happy path, then add edge cases progressively with each iteration.
- **Building something** → Write/modify code. Build it. Run it.
- **Optimizing** → Measure baseline, apply optimization, measure again.
- **Fixing a bug** → Reproduce, apply fix, verify fix.
- **Any other task** → Execute the task as defined.

#### Step 2: Evaluate Results

After execution, evaluate honestly:

- **What worked?** List everything that passed/succeeded.
- **What failed?** List every issue, error, unexpected behavior.
- **What edge cases haven't been tested yet?** List at least 2-3 new edge cases to test in the next iteration.
- **Severity classification** for each issue:
  - 🔴 **Critical** — Breaks core functionality. Must fix.
  - 🟠 **High** — Significant issue. Must fix.
  - 🟡 **Medium** — Noticeable issue. Fix in standard+strict mode.
  - 🟢 **Low** — Minor/cosmetic. Fix only in strict mode.

#### Step 3: Log the Iteration

Create `.loop/<task-slug>/iteration-<NN>.md`:

```markdown
# Iteration <NN>

- **Timestamp**: <timestamp>
- **Focus**: <what this iteration focused on>

## Executed

<what was done this iteration>

## Results

### ✅ Passed
- <thing that worked>
- <thing that worked>

### ❌ Failed
- 🔴 <critical issue description>
- 🟠 <high issue description>
- 🟡 <medium issue description>
- 🟢 <low issue description>

## Edge Cases Tested
- <edge case 1> → result
- <edge case 2> → result

## New Edge Cases Identified (for next iteration)
- <edge case to test next>
- <edge case to test next>

## Fixes Applied
- <fix 1: what was wrong → what was changed → file(s) modified>
- <fix 2: what was wrong → what was changed → file(s) modified>

## Iteration Verdict
<PASS | PARTIAL | FAIL> — <one-line summary>
```

#### Step 4: Fix Issues

For each issue found (respecting mode severity threshold):

1. **Diagnose** — Understand root cause, not just symptoms.
2. **Fix** — Apply the minimal, surgical fix. Don't over-engineer. Don't refactor unrelated code.
3. **Verify the fix** — Confirm the specific issue is resolved.
4. **Check for regressions** — Make sure your fix didn't break something that was working.

> **Karpathy Rule 3 applies**: Touch only what you must. Every changed line must trace to the issue you're fixing.

#### Step 5: Check Convergence

After fixing, evaluate against success criteria:

**Standard mode converges when:**
- All 🔴 Critical issues are fixed
- All 🟠 High issues are fixed
- No new issues found in the latest iteration
- All success criteria marked as met

**Strict mode converges when:**
- ALL issues at ALL severity levels are fixed
- No new issues found in the latest iteration (including edge cases)
- All success criteria marked as met
- At least one clean iteration with zero issues

**If converged** → Go to Phase 2 (Finalize).
**If not converged** → Go back to Step 1 with the next iteration number.

---

### Checkpoints (Every 5 Iterations)

At iterations **5, 10, 15**, pause and report to the user:

```markdown
## 🔄 Loop Checkpoint — Iteration <N>/20

**Task**: <task description>
**Mode**: <standard|strict>

### Progress So Far
- Iterations completed: <N>
- Total issues found: <count>
- Total issues fixed: <count>
- Remaining issues: <count>

### Success Criteria Status
1. [x] <met criterion>
2. [ ] <unmet criterion>
3. [x] <met criterion>

### Trend
<improving | plateau | degrading>

### Recommendation
<continue | need your input on X | consider switching approach>

**Continue looping?** (y/n)
```

**Wait for user response before continuing.**

---

### Stuck Detection (3+ Iterations Same Issue)

If the same issue persists for **3 consecutive iterations**:

1. **First**: Try a completely different approach to fix it.
   - Rethink assumptions.
   - Consider if the issue is a symptom of a deeper problem.
   - Try an alternative implementation strategy.
   - Log the approach change in the iteration file.

2. **If still stuck after the alternative approach**: Escalate to the user.
   ```
   ⚠️ STUCK: Issue "<description>" has persisted for <N> iterations.
   
   Approaches tried:
   1. <approach 1> — result
   2. <approach 2> — result
   3. <alternative approach> — result
   
   I need your input:
   - <specific question about the issue>
   - <possible direction to explore>
   ```

---

### Hard Limits

| Limit | Value | Action |
|---|---|---|
| Max iterations | 20 | Stop loop, generate summary, report to user |
| Checkpoint interval | 5 | Pause and ask user to continue |
| Stuck threshold | 3 | Try alternative approach, then escalate |
| Max fixes per iteration | 10 | If more than 10 issues, prioritize by severity |

If **iteration 20** is reached without convergence:

```markdown
⚠️ MAX ITERATIONS REACHED (20/20)

The loop has not fully converged. Here's where things stand:
- Issues remaining: <count> (<list severities>)
- Success criteria unmet: <list>

Recommendation: <what the user should do next>
```

---

## Phase 2 — Finalize

When the loop converges:

1. **Update manifest**: Set status to `converged`, mark all criteria as met.
2. **Create summary**: Write `.loop/<task-slug>/summary.md`.

**Summary format:**

```markdown
# Loop Summary: <task-slug>

## Result: ✅ CONVERGED

- **Task**: <what was done>
- **Mode**: <standard|strict>
- **Iterations**: <N> / 20
- **Total Issues Found**: <count>
- **Total Issues Fixed**: <count>
- **Duration**: <started> → <finished>

## Convergence Path

| Iter | Issues Found | Fixed | Remaining | Verdict |
|------|-------------|-------|-----------|---------|
| 1    | 5           | 5     | 0         | PARTIAL |
| 2    | 3           | 3     | 0         | PARTIAL |
| 3    | 1           | 1     | 0         | PASS    |

## Success Criteria — Final Status

1. [x] <criterion 1>
2. [x] <criterion 2>
3. [x] <criterion 3>

## Key Fixes Applied

| # | Issue | Severity | Fix | Files Changed |
|---|-------|----------|-----|---------------|
| 1 | <issue> | 🔴 | <fix> | <files> |
| 2 | <issue> | 🟠 | <fix> | <files> |

## Edge Cases Verified

- <edge case 1> ✅
- <edge case 2> ✅
- <edge case 3> ✅

## Lessons Learned

- <pattern or insight discovered during the loop>
- <what made this task tricky>
```

3. **Report to user**: Show the summary and confirm task completion.

---

## Edge Case Progression Strategy

Don't test the same cases every iteration. Progressively increase difficulty:

| Iteration | Focus |
|-----------|-------|
| 1-2 | Happy path, basic functionality |
| 3-5 | Common edge cases, invalid inputs, boundary values |
| 6-10 | Stress cases, concurrency, race conditions, large inputs |
| 11-15 | Adversarial inputs, security edge cases, failure recovery |
| 16-20 | Exotic combinations, platform-specific quirks, integration edges |

Adapt this to the specific task. The principle: **each iteration should test something the previous iteration didn't.**

---

## .loop/ Folder Structure

```
.loop/
├── <task-slug-1>/
│   ├── manifest.md
│   ├── iteration-01.md
│   ├── iteration-02.md
│   ├── iteration-03.md
│   └── summary.md
├── <task-slug-2>/
│   ├── manifest.md
│   ├── iteration-01.md
│   └── ...
└── .gitignore          ← auto-create, ignore .loop/ from git
```

**Task slug rules:**
- Derive from the task description
- Lowercase, hyphens, no spaces
- Max 40 characters
- Examples: `test-blocking-service`, `fix-login-flow`, `optimize-api-latency`

**Auto-create `.loop/.gitignore`** on first run if it doesn't exist:
```
# Loop state files — not committed to source control
*
```

---

## Behavioral Rules

1. **Never fake results.** If you can't actually run/test something, say so. Don't pretend an iteration passed.
2. **Never skip the log.** Every iteration gets its file. No exceptions.
3. **Never fix what isn't broken.** Karpathy Rule 3 — surgical changes only.
4. **Never add features.** The loop fixes the task. It doesn't enhance, extend, or "improve" beyond scope.
5. **Be honest about convergence.** Don't claim convergence if issues remain. Don't downgrade severity to force convergence.
6. **Progressive edge cases are mandatory.** Each iteration must test at least one new edge case not tested before.
7. **Regression checks are mandatory.** After every fix, verify that previously passing tests still pass.

---

## Reference Files

Load these when you need more depth on a specific aspect:

| File | When to Load |
|---|---|
| `references/checklist.md` | Pre-loop initialization, per-iteration checks, convergence verification |
| `references/templates.md` | Creating any `.loop/` state file — manifest, iteration log, summary, checkpoint |
| `references/edge-cases.md` | Planning edge cases for the current iteration tier |
| `references/anti-patterns.md` | When you suspect you're falling into a bad pattern (fake convergence, scope creep, etc.) |

> **Rule**: Load `references/checklist.md` at Phase 0 (initialization). Load others on-demand when relevant.

---

## Quick Reference

```
@loop to <task>              → Standard mode, 20 max, checkpoint@5
@loop -strict to <task>      → Strict mode, zero tolerance, 20 max
```

**The loop is: Execute → Evaluate → Log → Fix → Check Convergence → Repeat**

**You stop when: All success criteria met + zero new issues in latest iteration.**
