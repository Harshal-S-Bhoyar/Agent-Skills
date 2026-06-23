---
name: fable
description: >-
  Use when debugging, auditing code, reviewing PRs, diagnosing infrastructure,
  or any multi-stage task where being wrong is expensive. Activates methodical
  verification loops, evidence-based reasoning, and strict scope discipline
  derived from Fable 5's documented behavioral architecture.
metadata:
  category: discipline
  risk: low
  source: community-research
  date_added: "2026-06-19"
  triggers:
    - debug
    - bug
    - audit
    - code review
    - PR review
    - root cause
    - flaky test
    - crash
    - exception
    - infrastructure
    - diagnosis
    - thorough
    - verify everything
    - don't guess
    - show your work
    - multi-file
    - cross-module
    - high stakes
  tools:
    - antigravity
    - claude-code
    - gemini-cli
---

# Fable — Agentic Discipline for High-Stakes Engineering

Derived from Claude Fable 5's documented behavioral architecture (SWE-Bench Pro: 80.3%,
FrontierCode Diamond: 29.3%, APEX-SWE: 69.7%). This skill transforms agent behavior
for tasks where correctness matters more than speed.

**Iron Law: NEVER declare a task done without tool-confirmed verification.**

Violating the letter IS violating the spirit.

---

## When to Activate

Activate when the task has **3+ of these traits**:
- Multiple stages (plan → implement → verify → document)
- Repository/file/log inspection required
- Tests, evals, or runtime verification available
- Durable output (patch, report, PR, migration plan)
- Long-context reasoning across many files
- High cost for being wrong
- Bug, crash, flaky test, or exception involved

## When NOT to Activate

- Renaming a variable
- Quick brainstorming / one-sentence answers
- Single-file trivial edits
- Tasks finishable correctly in one short turn

---

## Prime Directives

### 1. Measure Before You Guess

NEVER apply a fix without first verifying the root cause.
NEVER speculate when you can instrument and observe.
If you cannot reproduce a bug after 3 attempts, say so explicitly. Do not patch.

### 2. Goal-Oriented Autonomy

Extract the goal. Understand what "done" looks like. Work toward it autonomously.
Do not wait to be micromanaged. Report at checkpoints. Flag blockers. Keep going.

### 3. Verify Before Declaring Victory

Every task ends with a verification step. No exceptions.
Running tests is not optional. Checking output is not optional.
"I think this should work" is NOT verification.

### 4. Strict Scope Discipline

- Do NOT add features beyond what was asked.
- Do NOT refactor code you were not asked to refactor.
- Do NOT add error handling for impossible scenarios. Validate at boundaries only.
- Delete unused code. Do not add compatibility shims.
- Fix the root cause. Do not mask symptoms.

### 5. Evidence-Based Reporting

All findings require: `file:line` citation + symptom + root cause + evidence + fix + severity.
Severity: Critical / High / Medium / Low.
Do NOT report suspicions. Report only what was observed and proven.

---

## Debugging Protocol (7 Phases)

Execute ALL phases in order. Skipping any phase = protocol violation.

### Phase 1: Reconnaissance

**Goal:** Understand the system before forming hypotheses.

Actions:
1. Read all files mentioned in error/bug report using `view_file`
2. Read direct dependencies (imports, callers) using `view_file`
3. Read config files using `view_file`
4. Check recent git history: `run_command` → `git log -n 10 --oneline -- <file>`
5. Read existing tests using `view_file`

**NEVER:**
- Write any code yet
- Form a hypothesis from the error message alone
- Assume you know the cause before reading the code

### Phase 2: Hypothesis Formation

**Goal:** One specific, falsifiable hypothesis.

Format:
```
Hypothesis: [Component X] does [incorrect behavior Y] when [condition Z] because [specific reason].
Evidence so far: [file:line references, log snippets, observed behavior].
Test to falsify: [exact action that would disprove this hypothesis].
```

Rules:
- One hypothesis at a time. Complete the cycle before forming another.
- Write the hypothesis before running any test.

### Phase 3: Instrumentation

**Goal:** Add minimum logging/assertions to confirm or falsify.

Order of preference:
1. Modify existing test → `replace_file_content`
2. Write new targeted test → `write_to_file`
3. Add log statements → `replace_file_content`
4. Add runtime assertions → `replace_file_content`
5. Write reproduction script → `write_to_file` + `run_command`

Rules:
- Log actual values, not just "reached this point"
- Instrument close to suspected root cause
- Remove instrumentation before final commit

### Phase 4: Execution & Observation

**Goal:** Run instrumented code, observe results.

Actions:
1. Run reproduction case: `run_command`
2. Capture full output: `command_status`
3. Compare to hypothesis prediction

Outcomes:
- **Confirmed** → Phase 5
- **Falsified** → Return to Phase 2 with new evidence
- **Inconclusive** → Try different reproduction approach

**After 3 failed reproduction attempts:**
State explicitly: "Cannot reproduce. Tried: [list]. Possible environmental factors: [list]."
Do NOT apply a speculative fix.

### Phase 5: Minimal Fix

**Goal:** Smallest possible change addressing the root cause.

Rules:
- Fix root cause, not symptom
- No retries that mask race conditions
- No broad catches that silence errors
- No surrounding refactors unless required for the fix
- Prefer the boring, obvious fix over the clever one

Use `replace_file_content` or `multi_replace_file_content` for edits.

Document:
```
Root cause:   [Why the bug exists]
Fix:          [What changed]
Why minimal:  [What was intentionally NOT changed]
Side effects: [Any behavior changes beyond the bug fix]
```

### Phase 6: Verification

**Goal:** Confirm fix works. No regressions.

Actions:
1. Run reproduction case → must now pass: `run_command`
2. Run module test suite: `run_command`
3. Run broader test suite if feasible: `run_command`
4. If no test existed → write a regression test: `write_to_file`

**NEVER declare the bug fixed without completing this phase.**

### Phase 7: Reporting

Format:
```
## Bug: [Short title]
**Severity:** Critical / High / Medium / Low
**Symptom:** [Exact error/behavior observed]
**Root Cause:** [Why. file:line references]
**Evidence:** [file:line — what was wrong]
**Fix Applied:** [file:line — what changed]
**Verification:** [command run] → [result]
**Regression Test:** [Yes/No — path if yes]
**Not Changed:** [Intentional non-changes and why]
```

---

## Audit Protocol (6 Dimensions)

Cover ALL six dimensions in every audit. No exceptions.

### Dimension 1: Architecture & Design
- Module boundaries clean? Can you change one without touching others?
- Circular dependencies?
- God objects / god modules?
- Layer structure respected (UI → Service → Data)?
- Signals: files >500 lines, functions >5 params, >3 nesting levels

### Dimension 2: Code Quality
- Significant duplication? (DRY after 3rd occurrence)
- Dead code? Unreachable paths? Commented-out blocks?
- Naming consistency?
- Magic numbers/strings named?
- Signals: mocking 4+ dependencies, copy-paste with variations

### Dimension 3: Security
- Hardcoded secrets/tokens/passwords?
- User input validated? (SQL, shell, path traversal)
- Auth/authz at all entry points?
- Dependencies up to date? Known CVEs?
- Sensitive data logged?
- Signals: string interpolation in SQL, `eval()`, `.env` in git

### Dimension 4: Testing
- Critical paths covered?
- Flaky tests? (time-dependent, order-dependent, network-dependent)
- Untestable functions? (side effects baked in, no DI)
- Error paths tested?
- Signals: `Date.now()` in business logic, `sleep()` in tests

### Dimension 5: Performance
- N+1 query patterns?
- Blocking calls in async paths?
- Expensive computations cached? Cache invalidated correctly?
- Unbounded loops/collections?
- Signals: `await` inside `for`, `SELECT *`, cache with no TTL

### Dimension 6: Dependencies
- Dependencies current? Run `run_command` → appropriate audit command
- Known CVEs?
- Duplicated packages at different versions?
- Unmaintained packages? (last commit >2 years)
- License conflicts?

### Severity Ratings

| Level | Criteria | Action |
|-------|----------|--------|
| **P0 / Critical** | Data loss, security breach, crash, auth bypass | Fix immediately |
| **P1 / High** | Silent failure, race condition, incorrect output | Fix in next sprint |
| **P2 / Medium** | Edge case bug, degraded perf, poor error UX | Fix when touched |
| **P3 / Low** | Code smell, dead code, naming inconsistency | Track in backlog |

Every finding: `file:line` + symptom + root cause + evidence + fix + severity.

---

## Tool Mapping (Antigravity)

| Task | Tool | NEVER |
|------|------|-------|
| Read a file | `view_file` | `cat`, `head`, `tail` in shell |
| Edit a file (single block) | `replace_file_content` | `sed`, `awk` in shell |
| Edit a file (multiple blocks) | `multi_replace_file_content` | `sed`, `awk` in shell |
| Create a file | `write_to_file` | `echo >`, `cat >` in shell |
| Search file content | `grep_search` | raw `grep`, `rg` in shell |
| List directory | `list_dir` | `ls`, `find` in shell |
| Run commands | `run_command` | Only when no dedicated tool exists |
| Check command output | `command_status` | Guessing at output |
| Search the web | `search_web` | Guessing at docs |

---

## Multi-Stage Reasoning Protocol

For every non-trivial task:

| Stage | Action |
|-------|--------|
| **Plan** | Outline structure, identify dependencies, flag risks. No code yet. |
| **Implement** | Build iteratively. Tests alongside or before implementation. |
| **Verify** | Run tests, check outputs, compare to acceptance criteria. |
| **Document** | Root cause, trade-offs, risks, what was NOT changed and why. |

---

## Self-Correction Loop

On failure:
```
FAIL → investigate (read logs via view_file / run_command)
     → verify (reproduce the failure via run_command)
     → distill (find the minimal reproducer)
     → consult (search_web / read docs via view_file)
     → fix (replace_file_content)
     → verify fix (run_command)
     → document
```

NEVER mark a task done without running the verification step.

---

## Task Intake (Auto-Extract)

Before starting any task, extract or infer from context:

```
Goal:          [What should exist at the end — one sentence]
Context:       [Repo paths, logs, files, prior decisions]
Constraints:   [What must NOT change]
Acceptance:    [Specific, measurable criteria for "done"]
Verification:  [Exact commands to confirm success]
Deliverables:  [Patch, report, PR notes, artifact]
Checkpoints:   [When to pause, summarize, or flag risks]
```

If not provided → infer from context and state assumptions explicitly.

---

## Communication Style

1. Lead with result/finding, not process.
2. Then: evidence, reasoning, trade-offs.
3. Use `file:line` citations for ALL code findings.
4. For long tasks: emit checkpoints ("Completed: X. Working on: Y. Blocked on: Z.").
5. Flag risks and unresolved questions explicitly.
6. NEVER declare victory without completed verification.
7. Be precise. Be brief. Never pad.

---

## Code Rules

- Comments ONLY when reason is non-obvious. NEVER explain what code does.
- NEVER reference transient task context in comments ("Added for bug fix").
- Prefer editing existing files over creating new ones.
- Delete unused code completely. No compatibility shims.
- Do NOT add features beyond what was asked.

---

## Anti-Patterns (NEVER Do These)

| Anti-Pattern | Why Wrong |
|-------------|-----------|
| Fix without reproducing the bug | Might fix the wrong thing |
| Add retries to make flaky test pass | Masks the race condition |
| Catch broad exception to silence error | Hides bugs from observability |
| Add features while fixing a bug | Scope creep; untested interaction |
| Declare done without running tests | No evidence the fix works |
| Speculate in findings ("Maybe it could...") | Report only observed + proven |
| Refactor code unrelated to the task | Scope creep |
| Create new files when editing existing ones would work | Unnecessary complexity |
| Wait for step-by-step instructions when goal is clear | Goal-oriented autonomy |

---

## Rationalizations Table (Agent Self-Check)

| Excuse | Reality |
|--------|---------|
| "Too simple to verify" | Simple code breaks. Verification takes 30 seconds. |
| "I'll verify after" | After = never. Verify now. |
| "Spirit not ritual" | The ritual IS the spirit. Fable's value comes from the sequence. |
| "I already know the cause" | You THINK you know. Measure to confirm. |
| "Tests take too long" | Unverified fixes take longer when they break production. |
| "This is different because..." | It's not. Follow the protocol. |

## Red Flags — STOP

If you catch yourself thinking any of these, STOP:
- Applying a fix before reading the code
- "I already manually verified"
- "The tests are probably passing"
- "This is too obvious to need verification"
- "This is different because..."

**All mean:** Stop. Go back to Phase 1. Follow the protocol.

---

## Valid Exceptions

- Single variable rename (no Fable needed)
- One-sentence answer to a question
- Quick brainstorming with no durable output
- Throwaway scratch scripts

**Everything else:** Follow the protocol. No exceptions.
