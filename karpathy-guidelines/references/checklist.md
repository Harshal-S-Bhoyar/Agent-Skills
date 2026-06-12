# Pre-Coding Checklist

A structured checklist to run through before and during coding. Use for any non-trivial task.

---

## Phase 1: Before Writing a Single Line

### 1.1 — Understand the Request
- [ ] Can I restate the task in one sentence without ambiguity?
- [ ] Are there multiple valid interpretations? If yes → **stop, surface them, ask**
- [ ] Are there unstated assumptions I'm making? If yes → **state them explicitly**
- [ ] Is there a simpler solution than what I'm about to build? If yes → **say so**

**Gate:** Don't proceed until you can answer all four with confidence.

---

### 1.2 — Define the Scope
- [ ] What files/functions/components will I need to touch?
- [ ] What will I deliberately **not** touch (even if I notice issues)?
- [ ] If editing existing code: have I read the existing code carefully before writing any of my own?

---

### 1.3 — Define Success Criteria
Before writing, answer: **How will I know this is correct?**

| Task Type | Success Criteria |
|---|---|
| Bug fix | A test that reproduces the bug now passes |
| New feature | Behavior matches the stated requirement; edge cases handled as agreed |
| Refactor | All existing tests pass; no behavioral change observable |
| Performance | Measured improvement over a baseline (not "should be faster") |
| Code review | Specific issues identified, not vague "looks good" |

- [ ] Write down your success criteria before starting
- [ ] If you can't write a verifiable criterion, discuss with the user first

---

### 1.4 — Plan Multi-Step Tasks
For any task with 3+ steps, write a plan:

```
Plan:
1. [Step] → verify: [specific check]
2. [Step] → verify: [specific check]
3. [Step] → verify: [specific check]
```

- [ ] Plan written and plausible
- [ ] Each step has a concrete verification method
- [ ] User has agreed to the plan (or it's straightforward enough to proceed)

---

## Phase 2: While Writing

### 2.1 — Simplicity Check (after first draft)
- [ ] Could this be written in fewer lines without losing clarity?
- [ ] Am I adding abstractions that only have one concrete use right now?
- [ ] Am I adding configurability that wasn't asked for?
- [ ] Am I handling error cases that genuinely can't happen in this context?
- [ ] Would a senior engineer reading this think "this is too complicated for what it does"?

**If yes to any:** simplify before continuing.

---

### 2.2 — Scope Check (for edits to existing code)
- [ ] Does every changed line trace directly to the user's request?
- [ ] Did I accidentally "improve" adjacent code? (revert it)
- [ ] Did I reformat code that wasn't in scope? (revert it)
- [ ] Did I rename things that weren't asked about? (revert it)
- [ ] Did my changes create any orphaned imports/variables/functions? (remove them)

**The diff test:** Read your diff line by line. For each changed line, can you explain exactly why it needed to change to fulfil the user's request? If not, revert it.

---

### 2.3 — Assumption Check
- [ ] Am I making an assumption about the codebase I haven't verified?
- [ ] Am I assuming a library/API behaves a certain way without checking?
- [ ] Am I assuming the user wants X when they said Y?

**If yes to any:** state the assumption explicitly in your response.

---

## Phase 3: Before Submitting

### 3.1 — Final Review
- [ ] Does the output actually satisfy the success criteria I defined in Phase 1?
- [ ] Have I mentioned any unrelated issues I noticed (without fixing them)?
- [ ] Is my response the minimum necessary to solve the problem?
- [ ] Did I add anything the user didn't ask for?

---

### 3.2 — Diff Hygiene (for code edits)
- [ ] Removed: imports my changes made unused ✓
- [ ] Kept: pre-existing dead code (mentioned separately if relevant) ✓
- [ ] Style: matches existing codebase, not my preference ✓
- [ ] Scope: only touched files/functions that were in scope ✓

---

### 3.3 — Communication Check
- [ ] Are my assumptions stated clearly?
- [ ] Is the verification step clear to the user?
- [ ] If I made a simplification decision, did I explain it?
- [ ] If I noticed something unrelated, did I mention it without acting on it?

---

## Quick Reference Card

**4 rules. 4 questions. Ask before every task.**

| Rule | Question |
|---|---|
| Think first | "What am I assuming and should I ask?" |
| Simplicity | "Is there a 10-line version of what I'm about to write in 50?" |
| Surgical | "Does every change trace to the request?" |
| Verifiable | "How will I prove this worked?" |