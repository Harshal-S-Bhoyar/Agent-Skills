# @loop Anti-Patterns

Common ways the loop fails. Recognize and avoid these.

---

## ❌ 1. Fake Convergence

**What it looks like**: Agent claims "all tests pass" without actually running them. Or downgrades a 🔴 to 🟡 to exit the loop faster.

**Why it happens**: Agent wants to finish. Convergence feels like success.

**Fix**: Every claim must be backed by actual execution output. If you can't run it, say so. Never downgrade severity to force convergence.

---

## ❌ 2. Groundhog Day Loop

**What it looks like**: Same fix applied in iteration 3, 4, 5, 6 — with identical results each time.

**Why it happens**: Agent doesn't track stuck issues. Doesn't try alternative approaches.

**Fix**: The stuck tracker in the manifest exists for this reason. After 3 consecutive iterations on the same issue, you MUST try a fundamentally different approach — not a variation of the same one.

---

## ❌ 3. Scope Creep

**What it looks like**: User asks to test login flow. By iteration 5, agent is refactoring the auth module, adding validation, improving error messages.

**Why it happens**: During testing, agent notices "improvements" and acts on them.

**Fix**: If it wasn't in the original task, it's not in scope. Note it in the iteration log under "Warnings" but do NOT fix it. The loop fixes the task — nothing else.

---

## ❌ 4. Shotgun Fixing

**What it looks like**: Agent changes 15 files in one fix. Touches code far from the actual issue. "While I was in there, I also..."

**Why it happens**: Agent conflates "thorough" with "touching everything."

**Fix**: One issue = one surgical fix. Every changed line must trace to the specific issue. If you can't explain why a line changed, revert it.

---

## ❌ 5. Skipping Regression Checks

**What it looks like**: Fix applied in iteration 4. Previous passing tests now fail in iteration 5. Agent doesn't notice because it only tested the new fix.

**Why it happens**: Agent focuses forward, not backward.

**Fix**: After EVERY fix, re-run previously passing checks. This is mandatory, not optional. A fix that breaks something else is not a fix.

---

## ❌ 6. Edge Case Theater

**What it looks like**: Agent "tests" edge cases by reasoning about them ("this would probably work because...") instead of actually executing them.

**Why it happens**: Running actual tests is harder than reasoning about them.

**Fix**: Edge case testing means executing the edge case and observing the result. "Probably works" is not a test result. Run it.

---

## ❌ 7. Infinite Abstraction

**What it looks like**: Agent introduces a base class, interface, factory, or abstraction layer as a "fix" — when a simple if-statement would do.

**Why it happens**: Agent defaults to "proper engineering" patterns.

**Fix**: Karpathy Rule 2. Minimum code that solves the problem. An abstraction for a single use case is not a fix, it's overhead. Add abstractions only when there are 2+ concrete users RIGHT NOW.

---

## ❌ 8. Silent Assumption

**What it looks like**: Agent encounters ambiguity in the task, picks one interpretation silently, builds on it for 5 iterations, then discovers it was the wrong interpretation.

**Why it happens**: Agent avoids asking questions because it feels like "wasting" an iteration.

**Fix**: Phase 0 exists to resolve ambiguity BEFORE the loop starts. If new ambiguity emerges mid-loop, surface it at the next checkpoint. A question at iteration 3 saves 10 wasted iterations.

---

## ❌ 9. Log Skipping

**What it looks like**: Agent runs 3 iterations but only creates 1 log file. Or creates logs with missing sections.

**Why it happens**: Logging feels like overhead when you're "in the flow."

**Fix**: Every iteration gets its complete log file. No exceptions. The logs are the proof that the loop ran properly. They also enable cross-session resume.

---

## ❌ 10. Premature Exit

**What it looks like**: Agent hits one clean iteration and declares convergence — but only tested 2 out of 7 success criteria.

**Why it happens**: "No issues found" ≠ "all criteria met." Agent confuses absence of failure with presence of success.

**Fix**: Convergence requires BOTH: (1) all success criteria marked as met, AND (2) zero new issues in the latest iteration. Both conditions. Not just one.

---

## Recognition Patterns

If you catch yourself doing any of these, **stop and correct immediately**:

| Signal | Anti-Pattern | Correction |
|--------|-------------|------------|
| "I'll assume..." | Silent Assumption | Ask or state the assumption explicitly |
| "While I'm here..." | Scope Creep | Note it, don't fix it |
| "This should work..." | Fake Convergence | Run it and verify |
| "Same fix, slightly different..." | Groundhog Day | Try fundamentally different approach |
| "I also improved..." | Shotgun Fixing | Revert the extras |
| "Previous tests probably still pass..." | Skipping Regression | Actually run them |
| "This edge case would likely..." | Edge Case Theater | Actually execute it |
