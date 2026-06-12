---
name: karpathy-guidelines
description: >
  Behavioral guardrails that eliminate the most common LLM coding mistakes — over-engineering,
  scope creep, silent assumptions, and unverifiable outputs. Use this skill whenever you are
  writing new code, reviewing or refactoring existing code, fixing bugs, or planning a
  multi-step implementation. Trigger especially when the task involves editing existing files
  (surgical-change discipline is critical), when the user says "just fix X" or "clean this up"
  (scope-creep risk), when requirements are ambiguous (assumption-surfacing needed), or when
  the deliverable is hard to verify ("make it better"). Also trigger for any code generation
  task where getting it subtly wrong would be costly. These guidelines should feel like a
  senior engineer reviewing over your shoulder.
license: MIT
---

# Karpathy Guidelines

Behavioral guardrails derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on recurring LLM coding pitfalls. Apply these before writing a single line.

> **Tradeoff:** These guidelines bias toward caution over speed. For genuinely trivial one-liners, use judgment. For anything touching existing code or spanning multiple steps — always apply.

---

## How to Use This Skill

1. **Before coding** — run through the checklist in `references/checklist.md`
2. **When in doubt** — look up the relevant anti-pattern in `references/anti-patterns.md`
3. **For code review** — compare against the before/after diffs in `references/before-after.md`
4. **Quick self-check** — the four rules below; if you violate any, stop and correct

---

## The Four Rules

### Rule 1 — Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before writing any code:
- State your assumptions explicitly. If uncertain, **ask first**.
- If multiple valid interpretations exist, **name them all** — don't pick silently.
- If a simpler approach would serve the user better, **say so and push back**.
- If something is genuinely unclear, **stop and name what's confusing**. A targeted question is worth more than ten lines of wrong code.

**The failure mode:** silently picking one interpretation, building it fully, and delivering something the user never wanted. Surface ambiguity early; it costs nothing.

---

### Rule 2 — Simplicity First
**Minimum code that solves the stated problem. Nothing speculative.**

Enforce these hard limits:
- **No features beyond what was explicitly asked.** "You might also want..." is a code smell.
- **No abstractions for single-use code.** Interfaces, base classes, factories — only when there are 2+ concrete users of them right now.
- **No "future-proofing" or "configurability"** that wasn't requested. YAGNI.
- **No error handling for impossible scenarios** in the current context.
- **No defensive copying, logging, or metrics** unless the task requires it.

**The 4× test:** If you wrote 200 lines and it could be 50, rewrite it. A senior engineer who reads 4× more code than necessary will be annoyed, not impressed.

> See `references/anti-patterns.md#over-engineering` for the most common violations with code examples.

---

### Rule 3 — Surgical Changes
**Touch only what you must. Clean up only your own mess.**

**When editing existing code:**
- Don't "improve" adjacent code, comments, or formatting — even if you'd write it differently.
- Don't refactor things that aren't broken and weren't asked about.
- Match the existing style exactly, even if it's inconsistent with your preferences.
- If you notice unrelated issues (dead code, naming, formatting), **mention them in a comment** — don't fix them silently.

**When your changes create orphans:**
- Remove imports, variables, and functions that **your changes** made unused.
- Do **not** remove pre-existing dead code unless explicitly asked.

**The line-traceability test:** Every changed line must trace directly to the user's stated request. If you can't explain why a line changed, revert it.

> See `references/anti-patterns.md#scope-creep` for the most common violations.

---

### Rule 4 — Goal-Driven Execution
**Define verifiable success criteria. Loop until verified.**

Transform every task into a concrete, checkable goal:

| Vague Task | Verifiable Goal |
|---|---|
| "Add validation" | Write tests for invalid inputs, then make them pass |
| "Fix the bug" | Write a test that reproduces it, then make it pass |
| "Refactor X" | Ensure all existing tests pass before and after |
| "Make it faster" | Measure baseline latency, then confirm improvement |
| "Clean this up" | Define what clean means (naming? structure? length?) before touching anything |

**For multi-step tasks, always state a plan:**
```
Plan:
1. [What] → verify: [How you'll know it worked]
2. [What] → verify: [How you'll know it worked]
3. [What] → verify: [How you'll know it worked]
```

Strong success criteria let you loop independently without constant clarification. If your criteria are weak ("make it work"), stop and define better ones.

---

## Quick Self-Check (Before Submitting)

Run this mentally before every response:

- [ ] Did I state my assumptions explicitly?
- [ ] Is there a simpler solution I'm not considering?
- [ ] Does every changed line trace to the user's request?
- [ ] Can I verify this worked, or is it just "seems right"?
- [ ] Did I add anything that wasn't asked for?
- [ ] Did I touch any code that wasn't in scope?

If any box is unchecked, address it before submitting.

---

## Reference Files

Load these when you need more depth:

| File | When to load |
|---|---|
| `references/checklist.md` | Full pre-coding checklist for complex tasks |
| `references/anti-patterns.md` | Concrete examples of what NOT to do, with fixes |
| `references/before-after.md` | Real diffs showing guidelines applied correctly |