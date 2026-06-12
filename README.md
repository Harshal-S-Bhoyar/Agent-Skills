<div align="center">

# AUTONOMOUS SKILL ARCHITECTURE
<p align="center">
  <em>The universal orchestration layer for Antigravity, Claude, ChatGPT, and independent agent frameworks.</em>
</p>

[![Architecture: 3-Tier Routing](https://img.shields.io/badge/Architecture-3--Tier%20Routing-zinc?style=for-the-badge)](#)
[![Compatibility: Universal](https://img.shields.io/badge/Compatibility-Universal%20Agents-zinc?style=for-the-badge)](#)
[![Security: Hardened](https://img.shields.io/badge/Security-Hardened-zinc?style=for-the-badge)](#)

<br>

<img src="https://picsum.photos/seed/architecture/1920/600?grayscale&mix-blend-luminosity&contrast=125" width="100%" alt="Architecture Topology">

</div>

<br><br><br>

## UNIVERSAL INTELLIGENCE

This repository is an OS-level orchestration layer designed to scale autonomous execution. It is built natively for Antigravity but engineered to serve **any agent ecosystem**.

Standard LLM workflows degrade when exposed to thousands of prompts. This architecture utilizes a strict 3-Tier indexing algorithm (Manifest → Category → Skill) to ensure surgical execution, zero token waste, and absolute routing reliability.

<br><br>

## THE CORE ARSENAL

The foundational primitives that power autonomous workflows.

<div align="center">

| THE ORCHESTRATOR | THE GUARDIAN | THE COMPRESSOR |
| :--- | :--- | :--- |
| **`master-skill`**<br><br>The authoritative control unit. Enforces a strict 7-phase execution pipeline, parses intent, manages memory, and executes the Plan-Apply-Unify (PAUL) loop. | **`defender-agent`**<br><br>The security perimeter. Actively hunts for vulnerabilities (SSRF, DoS bypasses) and enforces rigorous input validation and IP-pinning. | **`caveman`**<br><br>The token preserver. Eliminates LLM narrative bias. Enforces facts, fragments, and absolute compression, preserving context windows. |

| THE AUTOMATOR | THE OBSERVER | THE ARCHITECT |
| :--- | :--- | :--- |
| **`cicd-automation`**<br><br>Designs and deploys complex, multi-stage pipelines and rollout strategies across cloud providers with zero human intervention. | **`agent-memory`**<br><br>The persistent neural state. Logs architectural decisions, workflow states, and contextual anchors for precise cross-session recall. | **`cloud-architect`**<br><br>Synthesizes fault-tolerant, multi-cloud topologies. Drives cost-optimization and scalable infrastructure design patterns. |

</div>

<br><br><br>

## UNIVERSAL AGENT INTEGRATION

This library is agnostic. Whether you are using Antigravity, Claude, OpenAI wrappers, or custom terminal agents, the invocation syntax adapts to your environment.

### Antigravity Native
Antigravity utilizes command symbols to directly hook into the file system index.
```bash
@master-skill
/defender-agent
```

### Generic LLMs (ChatGPT / Claude Web)
For standard chat interfaces, inject the skill directly via prompt context or system instructions.
```text
System: You are operating under the master-skill framework. 
Retrieve and apply the instructions from [skills/master-skill/SKILL.md].
```

### CLI Agents (Cursor, Aider, Cline)
Reference the physical markdown files directly in your terminal or chat panel commands.
```bash
> Apply the rules from @skills/cicd-automation/SKILL.md to build the deployment pipeline.
```

<br><br><br>

## SYSTEM INITIALIZATION

Deploy the routing architecture on your local hardware.

```bash
# Clone the foundational repository
git clone https://github.com/your-username/antigravity-skills.git ~/.gemini/antigravity/skills

# Enter the orchestration directory
cd ~/.gemini/antigravity/skills

# Compile the 3-Tier Routing Matrix
python generate_indexes.py
```

<br><br><br>

## EXPANDING THE ARSENAL

To extend the agent's capabilities, forge a new skill and recompile the index.

**1. Scaffold the Directory**
```bash
mkdir semantic-routing
touch semantic-routing/SKILL.md
```

**2. Establish the Metadata**
```markdown
---
name: semantic-routing
description: "High-level description of execution boundaries and purpose."
keywords: ["routing", "llm", "semantic"]
---

# Execution Directives
- Implement boundary X.
- Restrict variable Y.
```

**3. Recompile the Index Matrix**
```bash
python generate_indexes.py
```

<br><br><br>

<div align="center">
  
## DEPLOYMENT READY

The index is built. The pipeline is hardened. Initiate your first command.

</div>
