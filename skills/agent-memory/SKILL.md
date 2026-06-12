---
name: agent-memory
description: "Use when starting any project session, switching context, completing a feature, or when the user says 'save context', 'remember this', 'store progress', or 'activate memory'. Automatically captures all important project state, architecture decisions, file changes, bugs, and patterns into agentmemory MCP persistent storage so future sessions always have full context without re-explaining."
category: memory
risk: low
source: custom
date_added: "2026-06-04"
metadata:
  triggers: memory, context, save, remember, agentmemory, progress, session, store, recall, history, project-state
---

# Agent Memory Skill

Captures and persists all critical project context into **agentmemory MCP** storage so that any future AI session can instantly resume with full knowledge — no re-explaining required.

---

## When to Activate

This skill activates **automatically** when:
- The user says `save context`, `remember this`, `store progress`, `activate memory`
- Starting a new coding session on any project
- Completing a feature, fix, or major code change
- Switching between tasks within the same project
- Before ending a long conversation
- When the user references a previous decision or asks "what did we decide about X?"

---

## What Gets Saved

Capture and store ALL of the following that are relevant to the current session:

### 1. Project Identity
- Project name, slug, and root path
- Tech stack (language, framework, key libraries)
- Current phase / milestone

### 2. Architecture Decisions
- Why specific patterns were chosen
- What was explicitly rejected and why
- Key constraints (e.g., "VPN must be on-device only", "no Java files")

### 3. File-Level Context
- Recently created or modified files
- What each file's responsibility is
- Any non-obvious structure decisions

### 4. Active Work State
- Current task / feature being built
- What is done, what is in-progress, what is next
- Blockers or open questions

### 5. Bugs & Fixes
- Bugs found, root cause, and the fix applied
- Any recurring issues or known gotchas

### 6. Patterns & Conventions
- Established code patterns (naming, structure, error handling)
- Rules that must not be violated

---

## Execution Protocol

Follow these steps in order when this skill is activated:

### Step 1 — Gather Context

Scan the current conversation and open files. Identify:
- What project is being worked on?
- What was the most recent task or goal?
- What files were created/modified?
- What decisions were made?
- What bugs were found/fixed?
- What is left to do?

### Step 2 — Save to agentmemory MCP

For each distinct piece of context, call `mcp_agentmemory_memory_save` with the correct `type`:

| Context Type | `type` value |
|---|---|
| Architecture choice / design decision | `architecture` |
| Reusable coding pattern | `pattern` |
| User preference or style rule | `preference` |
| Bug found and fixed | `bug` |
| Workflow or process step | `workflow` |
| Any other important fact | `fact` |

**Required fields for every save call:**
- `content` — Clear, self-contained description (write as if explaining to a fresh agent with zero context)
- `type` — One of the types above
- `concepts` — Comma-separated keywords (e.g., `"session, Room, DAO, Kotlin"`)
- `project` — Stable project slug (e.g., `"focuselocker"`, `"emcure-npd"`) — use the same slug every time
- `files` — Comma-separated relevant file paths (relative, if applicable)

**Example save call:**

```
mcp_agentmemory_memory_save(
  content: "SessionRepositoryImpl.hasActiveSession() now checks expiresAt > now() to avoid treating expired sessions as active. Previously it only checked status = ACTIVE which caused 'Session Still Active' bug after session expiry.",
  type: "bug",
  concepts: "session, repository, expiry, bug, Room, DAO",
  project: "focuselocker",
  files: "app/src/main/java/com/focuslock/data/repository/SessionRepositoryImpl.kt, app/src/main/java/com/focuslock/data/local/dao/SessionDao.kt"
)
```

### Step 3 — Recall Verification (Optional)

After saving, optionally call `mcp_agentmemory_memory_recall` with the project name to verify entries were stored:

```
mcp_agentmemory_memory_recall(
  query: "<project-slug> recent session",
  limit: 5,
  format: "compact"
)
```

### Step 4 — Confirm to User

After all saves are complete, report a summary to the user:

```
✅ Memory Saved — <N> entries stored to agentmemory
Project: <project-slug>
Saved: architecture decisions, patterns, bugs, workflow state
Next session: just say "recall memory for <project>" to restore full context.
```

---

## How to Recall Saved Context

In a new session, use:

```
mcp_agentmemory_memory_recall(
  query: "<project-slug> architecture patterns bugs workflow",
  limit: 10,
  format: "narrative"
)
```

Or use smart search for specific topics:

```
mcp_agentmemory_memory_smart_search(
  query: "session expiry bug fix"
)
```

---

## FocuseLock Project Defaults

When working on the **FocuseLocker** project (`project: "focuselocker"`), always include context about:
- Android Accessibility Service, VPN Service, Device Admin, WorkManager
- Session lifecycle: ACTIVE / EXPIRED / CANCELLED states
- OTP unlock flow (trusted contact, 10-min cooldown)
- Backend: Node.js/Express/TypeScript, Twilio, in-memory OTP only (no DB)
- Key rule: backend stores NOTHING permanently

---

## Rules — Non-Negotiable

- **Never log phone numbers or OTPs** — even in memory content strings
- **Always use a stable project slug** — do not use the folder path as the slug
- **Write content as standalone facts** — assume the reader has zero prior context
- **Separate concerns** — one save call per distinct concept, not one giant blob
- **Tag files accurately** — helps future retrieval via file-path search

---

## Quick Reference — MCP Tools Used

| Tool | Purpose |
|---|---|
| `mcp_agentmemory_memory_save` | Save a new memory entry |
| `mcp_agentmemory_memory_recall` | Search past memories by keyword |
| `mcp_agentmemory_memory_smart_search` | Hybrid semantic + keyword search |
| `mcp_agentmemory_memory_sessions` | List recent sessions |
| `mcp_agentmemory_memory_audit` | View audit trail of all operations |
| `mcp_agentmemory_memory_export` | Export all memory as JSON |
| `mcp_agentmemory_memory_governance_delete` | Delete specific entries |

---

## Limitations

- agentmemory MCP must be connected and authenticated for saves to persist
- This skill does **not** automatically run — it needs to be triggered by the user or via rule
- Content quality depends on what was discussed in the current session — always save before ending long sessions
