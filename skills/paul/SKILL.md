---
name: paul
description: "PAUL (Plan-Apply-Unify Loop) — auto-orchestrating development skill. Single entry point: @paul. Auto-detects project state, routes to correct phase, and continuously drives the loop forward. Only pauses for genuine human decisions."
risk: low
source: user
version: 2.0.0
---

# PAUL — Auto-Orchestrating Development Loop

**Single entry point: `@paul`**
No explicit commands needed. PAUL reads state, decides what's next, executes, and keeps moving.

---

## How It Works

When `@paul` is invoked:

```
@paul invoked
    │
    ▼
┌─ .paul/ exists? ─────────────────────────┐
│  NO → Run INIT (gather requirements)      │
│  YES → Read STATE.md                      │
│         │                                 │
│         ▼                                 │
│    ┌─ Loop Position? ──────────────┐      │
│    │ No plan    → Auto-run PLAN    │      │
│    │ Plan ready → Auto-run APPLY   │      │
│    │ Apply done → Auto-run UNIFY   │      │
│    │ Loop done  → Auto-run PLAN    │      │
│    │ Blocked    → Report + wait    │      │
│    └───────────────────────────────┘      │
│                                           │
│    After each phase completes:            │
│    → Auto-continue to next phase          │
│    → Only STOP for:                       │
│      • Plan approval (show plan, ask yes) │
│      • Checkpoints (human-verify/decision)│
│      • Blockers (missing info/access)     │
│      • Phase transition (confirm next)    │
└───────────────────────────────────────────┘
```

---

## CARL Rules (Mandatory — Never Override)

```
R1:  No implementation without approved PLAN.md.
R2:  Every APPLY must be followed by UNIFY. Never skip.
R3:  Respect PLAN.md "Boundaries" / "DO NOT CHANGE". Stop + confirm.
R4:  When blocked: document in STATE.md, notify human, await approval.
R5:  Phase transition: VERIFY state consistency. Blocking if misaligned.
R6:  Tasks require <verify>[proof]</verify>. No verify = cannot complete.
R7:  Log ALL deviations: what, why, downstream impact.
R8:  BDD acceptance criteria: Given/When/Then.
R9:  Size tasks for single session (~50% context). Split larger during planning.
R10: One commit per phase at transition. Format: {type}({phase}): {description}.
```

---

## AUTO-DISPATCH LOGIC

When `@paul` is invoked, execute this decision tree **automatically**:

### Step 0: Detect State

```
1. Check: does .paul/ directory exist?
   → NO  → goto INIT
   → YES → read .paul/STATE.md

2. Parse STATE.md "Loop Position" section:
   → Extract markers: PLAN [✓/○], APPLY [✓/○], UNIFY [✓/○]

3. Check for HANDOFF files:
   → If .paul/HANDOFF*.md exists → load most recent, present context

4. Route based on loop position:
```

| STATE.md Loop Position | Auto-Action |
|------------------------|-------------|
| No `.paul/` directory | → INIT |
| All ○ (no plan yet) | → PLAN |
| PLAN ✓, APPLY ○ | → Show plan summary, ask approval → APPLY |
| PLAN ✓, APPLY ✓, UNIFY ○ | → UNIFY |
| All ✓ (loop complete) | → Check ROADMAP for next phase → PLAN |
| Blocked | → Surface blocker, wait for human |

### Auto-Continue Rules

After each phase completes, **automatically continue** to next phase UNLESS:

| Stop Point | Why | Resume Trigger |
|------------|-----|----------------|
| Plan created | Needs human approval before execution | User says "yes"/"approved"/"go" |
| Checkpoint hit | Human verification/decision required | User responds |
| NEEDS_CONTEXT | Missing info not in plan | User provides info |
| BLOCKED | Structural impediment | User unblocks |
| Phase transition | Confirm next phase direction | User says "yes"/"continue" |
| Milestone complete | Celebrate + confirm next milestone | User says "yes"/"next" |

**Everything else auto-continues.** UNIFY flows into next PLAN. Quick-fixes flow end-to-end.

---

## PHASE: INIT (auto-triggers when no `.paul/`)

### Purpose
Create `.paul/` structure. Gather requirements conversationally.

### Auto-Flow

1. Create structure:
```bash
mkdir -p .paul/phases
```

2. Ask ONE question at a time (wait for each answer):
   - "What's the core value this project delivers?"
   - "What are you building? (1-2 sentences)"
   - Confirm project name (infer from directory/package.json)
   - "What kind of project? [1] Application [2] Campaign [3] Workflow [4] Other"

3. Infer complexity (don't ask): simple / standard / complex

4. Type-adapted requirements (1-2 sections at a time):

| Type | Ask In Order |
|------|-------------|
| Application | Tech Stack → Core Features → Data Model (skip if simple) → Deployment → Constraints → Success Criteria |
| Campaign | Deliverables → Platforms → Audience → Constraints → Success Metrics |
| Workflow | Automation Scope → Integrations → Data Flow → Constraints → Success Criteria |
| Other | Core Deliverables → Tools → Constraints → Success Criteria |

5. **Auto-generate** all three files from answers:

**`.paul/PROJECT.md`:**
```markdown
---
description: "[core_value]"
type: Project
about: "[project_name]"
---
# [project_name]

## What This Is
[description]

## Core Value
[core_value]

## Current State
| Attribute | Value |
|-----------|-------|
| Type | [project_type] |
| Version | 0.0.0 |
| Status | Initializing |
| Last Updated | [timestamp] |

## Requirements
### Core [Features/Deliverables]
- [items from walkthrough]

### Validated (Shipped)
None yet.

### Active (In Progress)
None yet.

### Out of Scope
[exclusions from walkthrough]

## Constraints
### Technical
- [from walkthrough]

### Business
- [from walkthrough]

## Key Decisions
| Decision | Rationale | Date | Status |
|----------|-----------|------|--------|

## Success Metrics
| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| [metric] | [target] | - | Not started |

## Tech Stack / Tools
| Layer | Technology | Notes |
|-------|------------|-------|
[from walkthrough]

---
*Created: [timestamp]*
```

**`.paul/ROADMAP.md`:**
```markdown
---
description: "[project_name] — milestone and phase structure"
type: Roadmap
about: "[project_name]"
---
# Roadmap: [project_name]

## Current Milestone
**v0.1 Initial Release**
Status: Not started

## Phases
| Phase | Name | Plans | Status | Completed |
|-------|------|-------|--------|-----------|
| 1 | TBD | TBD | Not started | - |

---
*Created: [timestamp]*
```

**`.paul/STATE.md`:**
```markdown
---
description: "[project_name] — current position"
type: ProjectState
about: "[project_name]"
---
# Project State

## Project Reference
**Core value:** [core_value]
**Current focus:** Project initialized — ready for planning

## Current Position
Milestone: v0.1 Initial Release
Phase: Not yet defined
Plan: None yet
Status: Ready for first PLAN
Last activity: [timestamp] — Project initialized

Progress:
- Milestone: [░░░░░░░░░░] 0%

## Loop Position
PLAN ──▶ APPLY ──▶ UNIFY
  ○        ○        ○     [Ready for first PLAN]

## Accumulated Context
### Decisions
[from init]

### Deferred Issues
None yet.

### Blockers/Concerns
None yet.

## Session Continuity
Last session: [timestamp]
Stopped at: Project initialization complete
Next action: PLAN
Resume file: .paul/PROJECT.md
```

6. **AUTO-CONTINUE → PLAN** (no pause needed after init)

---

## PHASE: PLAN (auto-triggers when loop needs a plan)

### Purpose
Create PLAN.md with objective, acceptance criteria, tasks, boundaries.

### Auto-Flow

1. **Validate**: Read STATE.md → confirm ready for PLAN
   - If mid-loop → warn, don't proceed

2. **Identify phase**: Read ROADMAP.md → find next incomplete phase
   - First plan ever? Help define phases from PROJECT.md requirements

3. **Classify scope** (auto-detect, confirm with user):

| Track | Signals | Format |
|-------|---------|--------|
| Quick-fix | 1 sentence, 1-2 files, no arch impact | Compressed: 1 task + 1 AC |
| Standard | Default | Full plan, multiple ACs, boundaries |
| Complex | 6+ tasks, multi-subsystem | Full + recommend splitting |

4. **Load context**: PROJECT.md + prior SUMMARYs (only relevant ones) + source files

5. **Create** `.paul/phases/{NN}-{name}/{plan}-PLAN.md`:

**Quick-fix:**
```markdown
---
phase: NN-name
plan: NN
plan_type: execute
autonomous: true
description: "[Goal]"
type: Plan
about: "[project]"
---

<objective>
## Goal
[Single sentence]
</objective>

<context>
@.paul/PROJECT.md
@relevant/source/file
</context>

<acceptance_criteria>
## AC-1: [Criterion]
Given [precondition]
When [action]
Then [expected outcome]
</acceptance_criteria>

<tasks>
<task type="auto">
  <name>[Name]</name>
  <files>[paths]</files>
  <action>[Instructions]</action>
  <verify>[Proof of success]</verify>
  <done>AC-1 satisfied: [condition]</done>
</task>
</tasks>
```

**Standard/Complex** adds: `<boundaries>`, `<verification>`, `<success_criteria>`, checkpoints.

6. **Coherence check** (silent if clean):
   - Plan vs PROJECT.md constraints
   - Plan vs recorded decisions
   - Plan vs ROADMAP phase scope
   - Only surface if issues found

7. **Update STATE.md** → PLAN ✓

8. **⏸ STOP: Show plan, ask approval**
```
════════════════════════════════════════
PLAN CREATED [track]
════════════════════════════════════════
Plan: [path]
Phase: [N] — [Name]
[summary of tasks + ACs]

Approve and execute? (yes/no/questions)
════════════════════════════════════════
```

> This is the ONE mandatory human gate in the loop.
> On "yes"/"approved"/"go" → **AUTO-CONTINUE → APPLY**

---

## PHASE: APPLY (auto-triggers after plan approval)

### Purpose
Execute tasks with Execute/Qualify verification per task.

### Auto-Flow

1. **Load plan**: Parse tasks, boundaries, ACs
2. **For each task** — Execute/Qualify loop:

**EXECUTE:**
- Log: "Task N: [name]"
- Execute `<action>` content
- Respect boundaries absolutely

**REPORT STATUS:**
| Status | Meaning | Flow |
|--------|---------|------|
| DONE | Completed, confident | → Qualify |
| DONE_WITH_CONCERNS | Completed, have doubts | → Qualify (focus concerns first) |
| NEEDS_CONTEXT | Missing info | ⏸ STOP: ask user |
| BLOCKED | Structural impediment | ⏸ STOP: report specifics |

**QUALIFY (auto-runs for DONE/DONE_WITH_CONCERNS):**

> Self-reports are inherently optimistic. Trust output, not memory.

1. **Re-read** actual files just modified
2. **Run `<verify>`** command fresh, read full output
3. **Compare** against `<action>` spec AND linked AC line-by-line
4. **Score:**
   - **PASS** → auto-continue to next task
   - **GAP** → fix → re-qualify (max 3 loops → escalate)
   - **DRIFT** → fix → re-qualify (max 3 loops → escalate)

**Self-check before claiming complete:**
| Thinking... | Do Instead |
|-------------|-----------|
| "Should work" | Run verify, read output |
| "Already checked" | Check again fresh |
| "Close enough" | Compare AC word by word |
| "Test passes" | Also compare against spec |
| "Minor deviation" | Log explicitly |
| "Confident" | Prove it |

**CHECKPOINT handling (⏸ STOP points):**

- `checkpoint:human-verify` → Show what was built + how to verify → wait
- `checkpoint:decision` → Show options → record decision to STATE.md → wait
- `checkpoint:human-action` → Show instructions → wait for confirmation

**Checkpoint failure diagnosis:**
| Type | Action |
|------|--------|
| Intent issue | Re-plan phase |
| Spec issue | Update ACs first, then code |
| Code issue | Fix in place |

3. **After all tasks**: Update STATE.md → APPLY ✓

4. **AUTO-CONTINUE → UNIFY** (no pause needed)

---

## PHASE: UNIFY (auto-triggers after apply complete)

### Purpose
Reconcile plan vs actual. Create SUMMARY.md. Close loop.

### Auto-Flow

1. **Gather**: Re-read PLAN.md ACs + recall APPLY results
2. **Compare**: Each AC → Pass/Fail with evidence. Each task → completed as spec? Deviations?

3. **Create SUMMARY.md** at `.paul/phases/{phase}/{plan}-SUMMARY.md`:

**Quick-fix (compressed):**
```markdown
---
phase: NN-name
plan: NN
completed: [timestamp]
description: "[One-liner]"
type: Summary
---
# Summary
**[What changed]**

## AC Result
| Criterion | Status |
|-----------|--------|
| AC-1 | Pass/Fail |

## Files Changed
| File | Change |
|------|--------|
| [path] | [brief] |
```

**Standard (full):** Objective, What Was Built, AC Results, Verification, Deviations, Decisions, Next Phase.

4. **Update STATE.md** → All ✓ (loop complete)

5. **Check phase completion:**
   - Count PLANs vs SUMMARYs
   - Equal → last plan → **MANDATORY TRANSITION**
   - More plans → auto-continue to next plan

6. **If last plan — Phase Transition (auto-executes):**
   - **Evolve PROJECT.md**: validated requirements → Validated, new requirements → Active
   - **Update ROADMAP.md**: phase → ✅ Complete
   - **Verify state consistency**: STATE/PROJECT/ROADMAP aligned (BLOCKING if not)
   - **⏸ STOP: Confirm next phase**:
```
════════════════════════════════════════
PHASE [N] COMPLETE
════════════════════════════════════════
✓ All plans complete
✓ PROJECT.md evolved
✓ State consistent

Next: Phase [N+1] — [Name]
Continue? (yes/pause)
════════════════════════════════════════
```

On "yes" → **AUTO-CONTINUE → PLAN** for next phase

7. **If milestone complete:**
```
════════════════════════════════════════
🎉 MILESTONE COMPLETE
════════════════════════════════════════
All [N] phases finished!
Start next milestone? (yes/pause)
```

---

## Stop Points Summary

PAUL auto-drives everything EXCEPT these genuine human gates:

| # | Stop Point | Why It Stops | Resume |
|---|-----------|-------------|--------|
| 1 | Init questions | Need project info | Answer questions |
| 2 | Plan approval | Must approve before execution | "yes" / "approved" |
| 3 | Checkpoint | Human verify/decision needed | Respond to checkpoint |
| 4 | NEEDS_CONTEXT | Missing information | Provide info |
| 5 | BLOCKED | Can't proceed | Unblock |
| 6 | Phase transition | Confirm next direction | "yes" / "continue" |
| 7 | Milestone complete | Confirm next milestone | "yes" / "next" |

**Everything else is auto-pilot.** UNIFY→PLAN, qualify loops, state updates, file creation — all automatic.

---

## Session Continuity

If conversation resets or new session starts:
- Invoke `@paul` again
- Auto-detects `.paul/STATE.md` → reads loop position → routes to exact next action
- If HANDOFF files exist → loads context automatically
- **ONE next action, no menu** — just continues where you left off

---

## Urgent/Interrupt Work

Decimal phases: `2.1`, `2.2` etc.
- Integers = planned, decimals = interruptions
- Still full PLAN→APPLY→UNIFY loop
- Quick-fix track keeps it fast

---

## Integration

PAUL orchestrates WHAT and WHEN. Other skills handle HOW:
- `@debugger` → during APPLY debugging tasks
- `@code-reviewer` → during PLAN coherence
- `@tdd-workflow` → when plan_type is TDD
- `@code-review-graph` → impact analysis during planning

PAUL sequences them — doesn't replace them.

---

## Anti-Patterns (NEVER do)

- Skip UNIFY after APPLY
- Execute without plan approval
- Trust memory over re-reading actual files
- Proceed past checkpoints without response
- Patch without diagnosing (intent/spec/code)
- Report DONE when uncertain (use DONE_WITH_CONCERNS)
- Modify protected/boundary files
- Offer multiple options when ONE action is correct
- Skip phase transition after last plan
