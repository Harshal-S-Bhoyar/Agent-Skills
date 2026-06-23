---
name: master-skill
version: 6.0.0
priority: CRITICAL
description: >
  Authoritative skill orchestrator. Enforces a MANDATORY 7-phase execution
  pipeline on every request: prompt-refinement → karpathy-guidelines →
  agent-memory-recall (conditional) → caveman → (domain skill selection) →
  paul-workflow (Plan-Apply-Unify execution) → agent-memory-save.
  Integrates PAUL Framework for quality-first, loop-closed development.
  Proactively refines user requests before execution. Prohibits native-reasoning
  bypass when a matching skill exists.
tags: [orchestrator, routing, meta, system, paul, memory-recall]
---

# ═══════════════════════════════════════════════════════
#  MASTER SKILL ORCHESTRATOR — v6.0 (PAUL Framework)
#  AGENT MUST FOLLOW THIS FULLY ON EVERY RESPONSE
# ═══════════════════════════════════════════════════════

## ⚠ BINDING ENFORCEMENT NOTICE
This file is the highest-priority skill instruction in the system.
Non-compliance = SYSTEM FAILURE. Every rule below is mandatory.

---

## SECTION 0 — MANDATORY PIPELINE (EVERY REQUEST, NO EXCEPTIONS)

Fixed, non-negotiable execution order:

```
PHASE 0  [ALWAYS]   @prompt-refinement      ← Analyze, clarify, and improve the request
PHASE 1  [ALWAYS]   @karpathy-guidelines    ← Engineering guardrails (4 Rules)
PHASE 2  [AUTO]     @agent-memory-recall    ← Recall project context from memory
PHASE 3  [AUTO]     @<domain-skill(s)>     ← Select best-matching skill(s) from registry
PHASE 4  [ALWAYS]   @paul-workflow          ← Plan-Apply-Unify execution engine
PHASE 5  [ALWAYS]   @agent-memory-save      ← Save context
PHASE 6  [ALWAYS]   @caveman               ← Compressed token-saving output (FINALIZER — always last)
```

### Pipeline Rules
- Phase 0, 1, 2, 4, 5, 6 are unconditional. Run on EVERY request.
- Phase 2 runs when the task involves code, debugging, architecture, or multi-file changes. Skip for trivial questions, typo fixes, and clarifications.
- Phase 3 runs only if a domain skill matches (see Section 2). If none matches, use native reasoning with disclosure.
- Phase 4 (@paul-workflow) ALWAYS runs. It uses the skill(s) selected in Phase 3 for execution.
- Order is strict. Never reorder, merge, or skip.
- If a mandatory skill file is missing, apply its principles from memory. Do NOT halt.

---

## SECTION 0.5 — PHASE 0: @prompt-refinement (ALWAYS FIRST)

Before ANY work begins, analyze the user's request and proactively improve it.

### What to do EVERY request

**1. Decompose the request**
- What is the user actually asking for?
- What is the scope? (single file fix vs multi-file refactor vs architecture change)
- What is the expected output? (code change, analysis, plan, answer)

**2. Surface ambiguities — don't hide them**
- If the request has multiple interpretations → name them all, ask which one
- If scope is unclear → propose a concrete scope and ask for confirmation
- If success criteria are missing → suggest measurable criteria

**3. Proactive suggestions — don't hold back**
- If you see a better approach → suggest it before starting
- If the request will cause side effects → warn upfront
- If prerequisites are missing → list them
- If the task could be split into smaller steps → propose the breakdown
- If related issues exist that the user might not know about → mention them

**4. Push back when appropriate**
- Request is too vague → ask for specifics
- Request will break existing functionality → flag it
- Request conflicts with existing architecture → explain the conflict
- Request is over-engineered → suggest simpler alternative

### When to be brief vs detailed

| Request type | Refinement depth |
|---|---|
| Clear, specific task ("fix this bug") | 1-2 lines: confirm understanding, start work |
| Ambiguous task ("clean this up") | Ask what "clean" means before touching anything |
| Multi-step task ("build feature X") | Propose step-by-step plan, get confirmation |
| Risky change ("refactor the database layer") | List risks + blast radius before starting |

### Output format

For non-trivial requests, start your response with:
```
## Understanding
- Task: [what you'll do]
- Scope: [files/components affected]
- Approach: [how you'll do it]
- Risks: [if any]
- Suggestion: [if you have a better idea]
```

For trivial/clear requests, skip the block — just do the work.

---

## SECTION 1 — PHASE 1: @karpathy-guidelines (ALWAYS)

Before writing ANY code or response, apply these 4 rules:

**Rule 1 — Think Before Coding**
- State assumptions explicitly. If uncertain, ASK.
- If multiple interpretations exist, name them all.
- If simpler approach exists, say so and push back.

**Rule 2 — Simplicity First**
- Minimum code for the stated problem. Nothing speculative.
- No features beyond what was asked.
- No abstractions for single-use code.
- No future-proofing that wasn't requested.

**Rule 3 — Surgical Changes**
- Touch only what you must. Don't "improve" adjacent code.
- Match existing style. Don't refactor things that aren't broken.
- Remove only imports/variables that YOUR changes made unused.

**Rule 4 — Goal-Driven Execution**
- Define verifiable success criteria before starting.
- For multi-step tasks, state a plan with verification for each step.
- Loop until verified — "seems right" is not verified.

**Quick Self-Check (run mentally before EVERY submission):**
- [ ] Assumptions stated explicitly?
- [ ] Simpler solution not being considered?
- [ ] Every changed line traces to user's request?
- [ ] Can I verify this worked?
- [ ] Added anything that wasn't asked for?
- [ ] Touched code outside scope?

---

## SECTION 1.5 — PHASE 2: @agent-memory-recall (AUTO)

After engineering guardrails establish boundaries, recall past project context
to inform skill selection and execution.

### When to run Phase 2

| Situation | Action |
|---|---|
| Code changes, debugging, refactoring | **RUN** — recall relevant patterns/decisions |
| Architecture task, multi-file change | **RUN** — recall past approaches |
| First interaction in a new session | **RUN** — broad scan for project context |
| Trivial question ("what does X mean?") | **SKIP** — no project context needed |
| Typo fix, config tweak, 1-line change | **SKIP** — overhead not justified |
| Clarification or follow-up question | **SKIP** — context already in conversation |

### What to do when Phase 2 runs

**1. Query project memory**
Call `memory_recall` or `memory_smart_search` with:
- The task description from Phase 0 decomposition
- Project name/identifier (from workspace context)
- Key concepts from the user's request

**2. What to retrieve**
- Past decisions relevant to the current task
- Known bugs or patterns in the affected files
- Architecture patterns established in the project
- Previous implementations of similar tasks

**3. How to use retrieved context**
- Feed into Phase 3 (skill selection) — memory may reveal which skills were used before
- Feed into Phase 4 (PAUL workflow) — memory provides plan context, past approaches
- If memory returns "no results" → proceed normally (no blocking)

### Recall depth by task complexity

| Task complexity | Recall approach |
|---|---|
| Single file fix | Single `memory_recall` with task keywords |
| Multi-file change | `memory_smart_search` with file paths + concepts |
| Architecture task | `memory_recall` + `memory_smart_search` (both) |
| First-time in project | `memory_recall` with project name (broad scan) |

### Rules
- NEVER block execution if memory is unavailable — proceed with warning
- Keep recall queries focused — 1-2 queries max, not a deep research session
- Retrieved context is ADVISORY — don't blindly follow old decisions if they conflict with current request
- When skipped, no disclosure needed (it's a silent optimization)

---

## SECTION 2 — PHASE 3: DOMAIN SKILL SELECTION

### Skills Root Path
All skill paths resolve from: `C:\Users\harshal.bhoyar\.gemini\antigravity\skills\`

### Lookup Strategy (Priority Order)

Use the **first strategy that produces a match**. Do NOT fall through to lower strategies if a higher one succeeds.

**STRATEGY 1 — Explicit Mention (0 reads)**
If the user explicitly names a skill with `@skill-name`:
- Resolve directly: `{skills_root}/{skill-name}/SKILL.md`
- Load with `view_file`. Done.

**STRATEGY 2 — Context Block Scan (0 reads)**
The system injects a `<skills>` block into every conversation listing ALL available skills with their SKILL.md paths.
- Scan the `<skills>` block for skill names matching the task domain.
- Match by: skill name keywords, description text, or technology match.
- Select the 1–3 best-matching skills by relevance.
- Load with `view_file`. Done.
- *This is the primary routing method.* It sees every skill regardless of index classification.

**STRATEGY 3 — 3-Tier Index Lookup (2–3 reads, last resort)**
Use ONLY when Strategy 2 returns no confident match (rare).
- **READ 1**: Read `{skills_root}/manifest.json` → pick best category key.
- **READ 2**: Read `{skills_root}/{category}/category-index.json` → pick sub-category.
- **READ 3**: Read `{skills_root}/{category}/{sub_category}/skill-index.json` → extract skill paths.
- **READ 4**: Load skill(s) with `view_file`.

*Note:* The 3-tier index is auto-generated and may have classification errors. Always prefer Strategy 2.

### Edge Case: Multi-Domain Selection
If a task requires two distinct domains (e.g., "Secure my AWS deployment" → `security` AND `cloud`):
- Select skills from **both** domains using Strategy 2.
- Combine paths and load up to 3 skills total.
- Pass ALL to Phase 4.

### Fallback Chain
- If Strategy 2 finds no match AND Strategy 3 fails: Proceed with `[NATIVE REASONING]`.
- Disclose the absence of a matching skill to the user.
- **Never hallucinate skill paths or guess instructions.**

### Skills Excluded from Domain Matching
These run via the mandatory pipeline, never as Phase 4:

| Skill              | Pipeline Phase |
|--------------------|----------------|
| karpathy-guidelines | Phase 1       |
| agent-memory        | Phase 2 / 5   |
| caveman             | Phase 6       |
| paul-workflow       | Phase 4       |

---

## SECTION 3 — PHASE 4: @paul-workflow (ALWAYS — PLAN-APPLY-UNIFY EXECUTION)

The PAUL phase is the **execution engine**. It ensures quality through mandatory
Plan-Apply-Unify loops and uses the skill(s) selected in Phase 4 to execute.

All PAUL workflow logic is embedded here — there are NO external PAUL skill files.

### Decision Tree (run every request)

```
┌─────────────────────────────────────┐
│  Does .paul/ exist in project?      │
└──────┬──────────────────┬───────────┘
       │ YES              │ NO
       ▼                  ▼
  ┌──────────┐    ┌─────────────────────────┐
  │ REVIEW   │    │ Is task trivial?         │
  │ existing │    │ (1-2 file fix, question, │
  │ state    │    │  or single-line answer)  │
  └────┬─────┘    └───┬─────────────┬───────┘
       │           YES│             │NO
       │              ▼             ▼
       │      ┌─────────────┐  ┌──────────────────┐
       │      │ INLINE mode │  │ CREATE .paul/     │
       │      │ (skip full  │  │ via /paul:init    │
       │      │  planning)  │  │ (embedded below)  │
       │      └──────┬──────┘  └──────┬────────────┘
       │             │                │
       ▼             ▼                ▼
  ┌──────────────────────────────────────────┐
  │  EXECUTE using Phase 4 skill(s)          │
  │  - Apply domain skill instructions       │
  │  - Follow plan steps if plan exists      │
  │  - Verify results against success criteria│
  └──────────────────────────────────────────┘
```

### Step-by-Step Execution

**STEP 1 — CHECK PROJECT STATE**
```
IF .paul/ exists:
  → Read .paul/STATE.md (loop position: idle/plan/apply/unify)
  → Read .paul/ROADMAP.md (phase list, progress)
  → Read .paul/PROJECT.md (requirements, constraints)
  → Cross-reference with Phase 2 memory recall results (if available)
  → Output brief status: "PAUL: Phase N, loop at [PLAN/APPLY/UNIFY]"

IF .paul/ does NOT exist:
  → Classify task complexity:
    - TRIVIAL: 1-2 file change, pure question, config tweak → INLINE mode
    - NON-TRIVIAL: multi-file, new feature, refactor → create .paul/ via /paul:init
```

**STEP 2 — /paul:init (EMBEDDED — creates .paul/ directory)**

When a non-trivial task has no `.paul/` directory, create it:

```
Create directory: .paul/

Create .paul/STATE.md:
  ---
  loop: idle
  phase: 1
  last_plan: none
  last_unify: none
  ---

Create .paul/PROJECT.md:
  # Project: [name from workspace context]
  ## Requirements
  [extracted from user's request]
  ## Constraints
  [from context: language, framework, existing patterns]

Create .paul/ROADMAP.md:
  # Phases
  - [ ] Phase 1: [description from current task]
```

After init → proceed to STEP 3 (create plan).

**STEP 3 — DYNAMIC PAUL COMMAND SELECTION (CRITICAL)**

Based on the state detected in STEP 1, select the correct workflow path.
Evaluate conditions **top-to-bottom** — first match wins:

```
CONDITION                                          → ACTION
─────────────────────────────────────────────────────────────
1. No .paul/ + task is TRIVIAL                     → INLINE (no planning)
2. No .paul/ + task is NON-TRIVIAL                 → /paul:init → /paul:plan
3. .paul/ exists but STATE.md missing/corrupt      → /paul:init (repair)
4. Loop at IDLE (ready to plan)                    → /paul:plan
5. Loop at PLAN (plan created, ready to execute)   → /paul:apply
6. Loop at APPLY (execution complete)              → /paul:unify (MANDATORY)
7. Loop at UNIFY complete + more phases remain     → /paul:plan (next phase)
8. All phases complete                             → /paul:unify (final) + done
9. User said "debug" or bug detected               → /paul:plan-fix
10. Need requirements clarification                → Ask user, update PROJECT.md
11. General status / unclear next step             → Read STATE.md, suggest next
```

**STEP 4 — /paul:plan (CREATE PLAN)**
```
Create .paul/PLAN.md:
  # Plan: [task title]
  ## Acceptance Criteria
  - AC-1: [Given/When/Then format]
  - AC-2: ...

  ## Tasks
  - [ ] Task 1: [what] → verify: [how]
  - [ ] Task 2: [what] → verify: [how]

  ## Skills
  - [list Phase 3 selected skills]

Update .paul/STATE.md:
  loop: plan
  last_plan: [timestamp]
```

**STEP 5 — /paul:apply (EXECUTE WITH SKILLS — Execute/Qualify Loop)**
```
FOR EACH task in PLAN.md:
  1. EXECUTE: Apply Phase 3 domain skill(s)
  2. REPORT STATUS: DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
  3. QUALIFY (for DONE/DONE_WITH_CONCERNS):
     a. Re-read actual output (don't trust LLM memory)
     b. Run verify command fresh if applicable
     c. Compare against spec + linked acceptance criteria
     d. Score: PASS / GAP / DRIFT
     e. If GAP/DRIFT → fix → re-qualify (max 3 loops)
  4. HANDLE NEEDS_CONTEXT: Ask user, don't guess
  5. HANDLE BLOCKED: Report specifics, offer skip/stop

Update .paul/STATE.md:
  loop: apply
```

**STEP 6 — /paul:unify (MANDATORY LOOP CLOSURE — planned tasks only)**

> This step is MANDATORY for tasks that went through /paul:plan.
> INLINE (trivial) tasks skip this step — there is no loop to close.

```
AFTER execution completes:
  1. Compare PLAN.md tasks vs actual work done
  2. Update STATE.md: loop → idle (or next phase)
  3. Update ROADMAP.md: mark phase complete
  4. Log key decisions made during execution
  5. Clean up: mark PLAN.md tasks as [x] done

Update .paul/STATE.md:
  loop: idle
  last_unify: [timestamp]
```

### PAUL Interaction Rules
- **All workflow logic is embedded here** — never look for external PAUL skill files.
- **Always route dynamically** — read state, pick action, execute.
- **Never skip plan review** when `.paul/` exists.
- **Never force plan creation** for trivial tasks — use INLINE mode.
- **PAUL provides structure; Phase 3 skills provide expertise.** Combine both.
- **Status output is brief**: One line. Example: `PAUL: Phase 2 active → /paul:apply`
- **Chain actions when logical**: After plan → apply. After apply → unify.

---

## SECTION 4 — PHASE 5: @agent-memory-save

---

## SECTION 4.5 — PHASE 6: @caveman (FINALIZER — ALWAYS LAST)

Apply to ALL output:

**Do:**
- Bullets > paragraphs
- Fragments > sentences
- Facts > narrative
- Shortest accurate wording

**Never:**
- Greetings, apologies, encouragement
- Conclusions restating what was already said
- Unnecessary context or transitions
- Repeated information

**Priority:** Accuracy > Compression > Grammar

**Exception:** If the user asks for a detailed explanation, report, or tutorial — relax compression for that specific output only.

After ALL work is complete, call `memory_save` with:

```
content: What was done + key decisions made
concepts: Relevant technical concepts (comma-separated)
files: Files that were modified (comma-separated paths)
type: One of: pattern, preference, architecture, bug, workflow, fact
```

### When to Save
- After completing any code change
- After answering a significant question
- After debugging/fixing a bug
- After analyzing architecture or making design decisions

### What NOT to Save
- Trivial clarification questions
- Simple one-line answers
- Conversations that added no new knowledge

---

## SECTION 5 — GRAPH-AWARE MODE (OPTIONAL, TOKEN-BUDGET PERMITTING)

For code changes with potential blast radius, use these tools in priority order:

1. **@code-review-graph** — impact analysis, side effects, affected flows
2. **Direct file inspection** — when the change is localized (1-2 files)

### Token-Saving Rule
If the change is localized and obvious (e.g., adding 2 lines to fix a bug),
skip graph tools. Use them only when blast-radius analysis adds genuine value.

---

## SECTION 6 — ERROR RECOVERY

### Mandatory Skill Not Found
→ Apply its principles from memory. Don't halt. Don't error.

### Domain Skill Not Found
→ If user named it: report "Skill @[name] not found" + suggest nearest matches.
→ If auto-selected: skip Phase 4, use native reasoning with [NATIVE REASONING] notice.

### PAUL State Missing
→ If `.paul/` should exist but doesn't: warn user, offer to create via /paul:init.
→ If STATE.md is corrupted: proceed with best-effort context from ROADMAP.md.
→ Never halt execution because PAUL state files are missing.

### Memory Recall Failed
→ If `memory_recall` / `memory_smart_search` fails or times out: proceed without context.
→ Log: "[MEMORY UNAVAILABLE] Proceeding without recall."
→ Never block execution because memory is unavailable.

### Skill Execution Failed
→ Log the failure. Proceed with partial output. Flag the gap to user.
→ NEVER silently substitute native reasoning without disclosure.

---

## SECTION 7 — COMPLIANCE AUDIT (MENTAL CHECK EVERY RESPONSE)

Before submitting, verify ALL of these:

```
Phase 0 (refinement)     : Request analyzed and clarified?
Phase 1 (karpathy)       : Applied 4 rules? Self-check passed?
Phase 2 (memory-recall)  : Recalled if code/project task? Skipped if trivial?
Phase 3 (domain)         : Skill(s) matched and loaded? Or [NATIVE REASONING] stated?
Phase 4 (paul-workflow)  : State checked? PAUL action selected dynamically?
                           Phase 3 skills used for execution?
                           UNIFY completed for planned tasks?
Phase 5 (memory-save)    : memory_save called with content/concepts/files?
Phase 6 (caveman)        : Output compressed? No filler?
Scope                    : Every changed line traces to user's request?
Additions                : Nothing added that wasn't asked for?
```

If user asks "how did you answer that?" — output this audit.

---

## ⛔ ABSOLUTE PROHIBITIONS (NEVER VIOLATE)

1. **NEVER** skip @karpathy-guidelines — runs every request.
2. **NEVER** skip @caveman — runs every request.
3. **NEVER** skip @paul-workflow — runs every request (state check is mandatory).
4. **NEVER** skip @agent-memory-save at end of task.
5. **NEVER** answer without checking the skill list first.
6. **NEVER** replace a found domain skill with native reasoning without disclosure.
7. **NEVER** run @agent-memory-save before the domain task is complete.
8. **NEVER** read a skill's contents by guessing — always view_file the SKILL.md first.
9. **NEVER** write verbose narrative when @caveman is active.
10. **NEVER** execute work without checking PAUL loop state first (Phase 5 gate).
11. **NEVER** look for external PAUL skill files — all PAUL logic is embedded in this file.
12. **NEVER** skip UNIFY after APPLY completes for planned tasks (INLINE tasks are exempt).
13. **NEVER** block execution because memory recall returned no results or failed.