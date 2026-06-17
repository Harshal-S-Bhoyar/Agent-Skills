# @loop Checklists

## Pre-Loop Checklist (Phase 0)

Run through this **before** starting the first iteration. Every box must be checked.

- [ ] **Task parsed**: I can state in one sentence exactly what the user wants.
- [ ] **Mode detected**: Standard (no flag) or Strict (`-strict`).
- [ ] **Ambiguity resolved**: If the task is vague, I asked for clarification BEFORE starting. I did not guess.
- [ ] **Success criteria defined**: I wrote 3-7 concrete, verifiable conditions. Each one is testable — not subjective.
- [ ] **Criteria are SMART**: Specific, Measurable, Achievable, Relevant, Time-bound (within 20 iterations).
- [ ] **Scope locked**: I know exactly what is IN scope and what is OUT. I will not expand scope during the loop.
- [ ] **Baseline captured**: I know what the current state is BEFORE I change anything. I can detect regressions.
- [ ] **State folder created**: `.loop/<task-slug>/manifest.md` exists with all fields populated.
- [ ] **No premature coding**: I have not written a single line of code yet. Plan first, code second.

---

## Per-Iteration Checklist

Run through this **during every iteration**. No exceptions.

### Before Executing
- [ ] I know what THIS iteration is focusing on (not repeating the last one).
- [ ] I identified at least 1 new edge case to test that wasn't tested before.
- [ ] I reviewed the previous iteration's results to avoid repeating the same approach on a stuck issue.

### After Executing
- [ ] I ran/tested the actual code — I did not just read it and assume it works.
- [ ] I classified every issue by severity (🔴🟠🟡🟢).
- [ ] I logged results honestly — no faking passes, no downgrading severity.

### After Fixing
- [ ] Every fix is surgical — only touches what's needed for this specific issue.
- [ ] I verified each fix resolves its specific issue.
- [ ] I ran regression checks — things that passed before still pass.
- [ ] I did NOT refactor, rename, or "improve" anything outside the fix scope.
- [ ] I did NOT add features, abstractions, or future-proofing.

### Before Moving to Next Iteration
- [ ] Iteration log file created: `.loop/<task-slug>/iteration-<NN>.md`.
- [ ] Manifest progress table updated.
- [ ] Convergence check performed against success criteria.
- [ ] If iteration is 5/10/15 — checkpoint report shown, waiting for user approval.
- [ ] If same issue for 3+ iterations — stuck protocol activated.

---

## Convergence Checklist

Run this to verify you're ACTUALLY converged, not just hoping.

### Standard Mode
- [ ] All 🔴 Critical issues: fixed and verified.
- [ ] All 🟠 High issues: fixed and verified.
- [ ] No NEW issues appeared in the latest iteration.
- [ ] All success criteria from manifest: marked [x].
- [ ] Regression check: all previously passing tests still pass.

### Strict Mode (all of Standard, plus)
- [ ] All 🟡 Medium issues: fixed and verified.
- [ ] All 🟢 Low issues: fixed and verified.
- [ ] At least ONE completely clean iteration with zero issues found.
- [ ] Edge cases from all difficulty tiers tested (not just happy path).

---

## Post-Loop Checklist (Phase 2)

- [ ] Manifest status updated to `converged` (or `aborted` if max iterations hit).
- [ ] Summary file created: `.loop/<task-slug>/summary.md`.
- [ ] All success criteria have final status.
- [ ] Convergence path table is complete.
- [ ] Key fixes table lists every fix with files changed.
- [ ] Edge cases verified list is populated.
- [ ] User notified with final summary.
