# Project Folder Structure Blueprint

This document serves as the definitive guide to the folder structure, organization principles, and conventions of the **Commander Igris — The System** project. It outlines the architectural decisions behind file placement and provides templates for extending the system.

---

## Initial Auto-detection Phase

- **Project Type**: Python Multi-Agent AI-Factory (using local Ollama models like `qwen2.5-coder:32b` and `llama3.1:8b`).
- **Frontend Components**: Static glassmorphism Web UI located in `igris/web/` (HTML, Vanilla CSS, Vanilla JavaScript) powered by a FastAPI backend API in `igris/api/`.
- **Desktop Component**: GUI application built using Python's `CustomTkinter` (`igris/desktop.py`).
- **Monorepo Status**: Non-monorepo (standard monolithic repository containing code and associated system planning/design documentation under `Overwatch/`).
- **Microservices**: None (monolithic single-process orchestrator with multi-agent simulation and local API server).
- **Structural Philosophy**: Organized under a *layer-first* structure where core logic is strictly separated, with the `skills/` library acting as an modular agent plugin-system.

---

## 1. Structural Overview

The folder structure of **Commander Igris** is organized around a clean separation of concerns between:
1. **Agent Engine Core (`igris/core`, `igris/models`, `igris/prompts`)**: Implements the multi-agent life cycle (Observe-Evaluate-Provision-Deploy), VRAM budgeting, OOM checks, and agent message contract validations.
2. **Agent Capabilities (`igris/skills`)**: 781 skills (754 security + 14 superpowers + 10 core + 3 agent-definitions).
3. **Distribution Interfaces (`igris/api`, `igris/web`, `igris/cli`, `igris/desktop.py`)**: Consists of a FastAPI HTTP/WebSocket server, a static dashboard front-end, a rich CLI, and a desktop GUI app.
4. **Research & Development (`Overwatch/`)**: Contains master plans, spikes, sketches, and specifications driving future implementation phases.

### Architecture Flow

```
Användare → CLI / Desktop / Web
              ↓
        Orchestrator (igris/core/)
              ↓
        Router (8B LLM) (llama3.1:8b) → väljer agent
              ↓
        Agent exekverar (igris/skills/)
              ↓
        Ollama (qwen2.5-coder:32b)
```

### Organizational Principles
- **Layer-First**: Modules are strictly separated by system function. E.g., `models` defines pure schemas, while `core` runs the orchestrator loop.
- **Contract-Driven Communication**: All inter-agent communication is validated via Pydantic schemas defined in `igris/core/contract_validator.py`.
- **Static Skill Encapsulation**: Skills are stored as static Markdown metadata (`SKILL.md`) with YAML frontmatter alongside implementation scripts to allow indexing and retrieval by local embedding models.

---

## 2. Directory Visualization

Below is the directory hierarchy for the project, documented to **Depth Level 4**, excluding auto-generated folders (such as `.git/`, `.pytest_cache/`, `.venv/`, and `__pycache__/`).

```
c:\Users\willi\the-system\
├── Overwatch\                      # System planning, spikes, and UI mockups
│   ├── demos\                      # Demo assets and screen recordings (currently empty)
│   ├── plans\                      # Deployment plan guides
│   │   └── DEPLOY.md               # Tunneling and installation guide for host computer
│   ├── prompts\                    # LLM routing prompts drafts (currently empty)
│   ├── sketches\                   # User interface wireframes & style guides
│   │   ├── 001-calm-editorial\     # Rejected — Linear/Stripe layout files (historical)
│   │   ├── 002-operator-dense\     # Rejected — Grafana-style layout files (historical)
│   │   ├── 003-living-machine\     # Rejected — Particle-style layout files (historical)
│   │   ├── 004-solo-system\        # Recommended base — Solo Leveling blue-neon System layout
│   │   ├── 005-solo-hud\           # Gaming HUD — purple-violet HP/MP layout
│   │   ├── 006-solo-commander\     # Shadow Army — violet-gold layout
│   │   └── MANIFEST.md             # List of UI designs and feedback
│   ├── spikes\                     # Throwaway research code verifying technical risks (currently empty)
│   ├── Dashboard-Plan.md           # Pixel-art GUI design spec (Alpedal)
│   ├── OVERWATCH_MASTER_PLAN.md    # Active system design and phase specification
│   ├── WEBAPP-PROTOTYPE-PLAN.md    # Webb-prototyp-plan (historical/archived)
│   └── WILLIAM-COLLAB-PLAN.md      # Samarbetsplan William + Alpedal (historical/archived)
├── archive\                        # Historical references and backups
│   └── old-igris\                  # Old codebase reference (removed/archived)
├── igris\                          # Main Python application package
│   ├── api\                        # FastAPI Web API application
│   │   ├── routes\                 # HTTP routes grouped by resource
│   │   │   ├── agents.py           # /agents endpoint (agent state)
│   │   │   ├── gpu.py              # /gpu endpoint (VRAM stats)
│   │   │   └── health.py           # /health endpoint (heartbeat)
│   │   ├── auth.py                 # Middleware-level token-auth helper
│   │   ├── main.py                 # FastAPI app entry point and router registrations
│   │   └── state.py                # Server-wide states and Orchestrator bindings
│   ├── cartographer\               # Repository incremental cartographer tool
│   │   ├── cache.py                # Scanner cache DB wrapper
│   │   ├── extractors.py           # Abstract Syntax Tree (AST) code extraction
│   │   ├── models.py               # Cache database schemas
│   │   └── scanner.py              # Incremental parsing & mapping coordinator
│   ├── cli\                        # Command Line Interface (CLI) commands
│   │   ├── chat.py                 # Non-blocking interactive shell console
│   │   └── main.py                 # CLI entry point (status, validate, map)
│   ├── config\                     # Configuration files directory
│   │   └── igris.yaml              # Main system settings, models, VRAM budgets
│   ├── core\                       # Core runtime execution logic
│   │   ├── contract_validator.py   # Pydantic schemas validating inter-agent envelopes
│   │   ├── gpu_manager.py          # NVIDIA GPU telemetry & budget validation
│   │   └── orchestrator.py         # Main loop (Observe-Evaluate-Provision-Deploy)
│   ├── data\                       # System state persistence directory
│   │   ├── agents.json             # Persisted active agents database
│   │   └── tasks.json              # Persisted task backlog database
│   ├── docs\                       # Project documentation markdown resources
│   ├── models\                     # System-wide Pydantic schemas
│   │   ├── agent.py                # Agent structure (rank, success metrics)
│   │   ├── hardware.py             # Hardware profiles specifications
│   │   └── task.py                 # Task lifecycle structures (pending/completed)
│   ├── prompts\                    # Local model prompting utilities
│   │   └── router_prompts.py       # Prompt templates for the 8B router model
│   ├── skills\                     # Capabilities directory containing 781 agent skills
│   │   ├── agents\                 # Agent-specific instructions (builder, reviewer)
│   │   ├── core\                   # Caveman core agent skills & dev utilities (10 skills)
│   │   ├── security\               # Security audit execution blueprints (754 skills)
│   │   ├── superpowers\            # Strategic coding techniques (14 skills)
│   │   └── caveman.py              # Caveman Ultra surgical patching implementation
│   ├── tests\                      # Pytest automated testing suite
│   │   ├── test_api.py             # API route handlers integration tests
│   │   ├── test_caveman.py         # Caveman patching logic tests
│   │   ├── test_contract_validator.py # Contract validation tests
│   │   ├── test_gpu_manager.py     # GPU VRAM allocations tests
│   │   └── test_phase0.py          # Cartographer scanner unit tests
│   ├── web\                        # Web Dashboard Static Frontend
│   │   ├── app.js                  # Frontend client orchestrator & API communications
│   │   ├── index.html              # Dashboard core HTML page
│   │   └── styles.css              # Glassmorphism dark layout rules
│   ├── AUDIT.md                    # Core code quality audit report
│   ├── desktop.py                  # CustomTkinter GUI Desktop controller
│   ├── idle_detector.py            # Idle state tracker (detects lack of user input)
│   └── requirements.txt            # Project dependencies manifest
└── README.md                       # High-level overview and run instructions (Swedish)
```

---

## 3. Key Directory Analysis

### `igris/core/`
This directory contains the central engine of the system.
- [contract_validator.py](file:///c:/Users/willi/the-system/igris/core/contract_validator.py): Standardizes inter-agent messaging. Every message is wrapped in a `ContractEnvelope` and validated against a registered Pydantic schema (e.g., `AgentSpawnRequest`, `TaskAssign`).
- [gpu_manager.py](file:///c:/Users/willi/the-system/igris/core/gpu_manager.py): Monitors hardware VRAM limits on the RTX 3090 (24 GB) using `pynvml` or system profiles. Prevents Out-Of-Memory (OOM) failures by rejecting actions that exceed limits.
- [orchestrator.py](file:///c:/Users/willi/the-system/igris/core/orchestrator.py): Runs the primary state machine. It queries GPU metrics, calls the Ollama router model to decide what actions to take, builds and provisions contracts, and executes them.

### `igris/skills/`
A repository of agent capabilities. It is split into specialized sub-directories:
- `security/`: Consists of 754 folders (e.g., `analyzing-windows-registry-for-artifacts`), each containing an execution script (`scripts/agent.py`), API references (`references/api-reference.md`), and metadata (`SKILL.md`).
- `superpowers/`: Guides for advanced engineering behavior like systematic debugging and writing plans.
- `core/`: Basic agent commands and automated utilities (10 core skills total, including `changelog-generator`, `git-commit-writer`, and `pr-description-writer`).
- [caveman.py](file:///c:/Users/willi/the-system/igris/skills/caveman.py): Core utility executing regex-based surgical file edits without rewriting files.

### `igris/api/` & `igris/web/`
Defines the distributed interface for multi-user access:
- [main.py](file:///c:/Users/willi/the-system/igris/api/main.py): Sets up a FastAPI application.
- `routes/`: Standard REST routers managing GPU, agents, and health queries.
- `web/`: Contains static HTML/CSS/JS files, using a pure vanilla style to maintain minimal load times and zero dependency overhead.

---

## 4. File Placement Patterns

### Configuration Files
- **Application Level**: Main application settings are located in [igris.yaml](file:///c:/Users/willi/the-system/igris/config/igris.yaml). This file configures Ollama URLs, context lengths, VRAM allocations, OOM thresholds, and agent ranks.
- **State Data**: Persistence occurs under `igris/data/` inside JSON formats (`agents.json`, `tasks.json`).

### Model/Entity Definitions
- All shared data schemas are represented as Pydantic models. They must be placed under `igris/models/` (e.g., `agent.py`, `hardware.py`, `task.py`).

### Business Logic
- Multi-agent orchestration belongs in `igris/core/`.
- AST parsing and indexing belongs in `igris/cartographer/`.
- Executable agent procedures are structured as isolated modules within `igris/skills/`.

### Test Files
- Automated tests are written using the `pytest` framework and placed in `igris/tests/`. All test filenames must prefix with `test_`.

---

## 5. Naming and Organization Conventions

### File Naming Patterns
- **Python Source Files**: `snake_case.py` (e.g., `gpu_manager.py`, `idle_detector.py`).
- **Markdown / Documentation**: `UPPERCASE_WITH_UNDERSCORES.md` for root documents (e.g., `AUDIT.md`, `README.md`), and standard `kebab-case.md` for subfolders.
- **Skill Folders**: `kebab-case` (e.g., `detecting-process-injection-techniques`).
- **Frontend Files**: lowercase naming (e.g., `index.html`, `styles.css`, `app.js`).

### Folder Naming Patterns
- Directories must use lowercase `snake_case` (e.g., `gpu_allocations`) or `kebab-case` for skill groupings.

### Namespace/Module Patterns
- Import statements in python source code must use absolute imports starting from `igris` package root:
  ```python
  from igris.core.gpu_manager import GPUManager
  from igris.models.task import Task
  ```

---

## 6. Navigation and Development Workflow

### Entry Points
1. **Desktop GUI Application**: [desktop.py](file:///c:/Users/willi/the-system/igris/desktop.py)
2. **FastAPI Server**: [main.py](file:///c:/Users/willi/the-system/igris/api/main.py)
3. **System CLI Wrapper**: [main.py](file:///c:/Users/willi/the-system/igris/cli/main.py)

### Common Development Tasks
- **To add a new API route**:
  1. Add a router file to `igris/api/routes/your_resource.py`.
  2. Register the router inside `igris/api/main.py`.
- **To add a new agent skill**:
  1. Create a sub-folder under `igris/skills/security/` or `igris/skills/superpowers/`.
  2. Populate `SKILL.md` (with YAML frontmatter), `scripts/agent.py` and `references/api-reference.md`.
- **To modify configurations**:
  1. Open [igris.yaml](file:///c:/Users/willi/the-system/igris/config/igris.yaml) and edit relevant sections (such as `oom_prevention` or `models`).

### Content Statistics

A breakdown of file and code distribution across the project:

- **Total Project Files**: 5,384 (includes recursively nested files in capabilities)
- **Python Files count**: ~1,074 files (including skills `agent.py` controllers)
- **Markdown Files count**: ~2,455 files (mostly skill descriptions)
- **HTML/CSS/JS files count**: 12 files (sketches and frontend client)
- **Core Python Lines of Code (LOC)**: ~3,761 lines (excl. skills)
- **Biggest Python File**: [orchestrator.py](file:///c:/Users/willi/the-system/igris/core/orchestrator.py) (617 lines)
- **Skills Distribution**:
  - `security/`: 754 individual skills (4,157 total files)
  - `superpowers/`: 14 strategic coding skills (51 total files)
  - `core/`: 10 basic agent skills and utilities (28 total files)
  - `agents/`: 3 agent presets (builder, reviewer, investigator)
- **Pytest Automated Tests**: 6 files (83 test cases)

---

## 7. Build and Output Organization

### Build Configuration
- All Python dependencies are tracked in [requirements.txt](file:///c:/Users/willi/the-system/igris/requirements.txt).
- No asset bundlers (Webpack/Vite) are used in the frontend; static files are loaded directly by the browser.

### Output Structure
- **Persistent Data**: Local JSON files stored in `igris/data/` persist the running state of agents and tasks.
- **Python Bytecode**: Ignored via `.gitignore` (`**/__pycache__/`).
- **Dev Server Execution**: The FastAPI backend can be launched locally via `uvicorn igris.api.main:app --reload --port 8000`.

---

## 8. Technology-Specific Organization

### Python Modules
- Standard Python structures are enforced. Every package folder contains an `__init__.py` to declare namespaces.
- Pydantic v2 is used as the validation standard for data contracts, settings, and communication envelopes.

### Frontend Web Layout
- Serves static assets from `igris/web/`.
- Utilizes CSS custom variables for dark/glassmorphic styling rules matching the "Solo Leveling / Shadow Army" aesthetic.
- The entry point HTML loads `app.js` using modular imports `<script type="module" src="app.js">`.

---

## 9. Extension and Evolution

As the project advances from **Phase 1** to **Phase 2 (Docker Sandbox, Post-Write Hooks)**, the folder structure is designed to remain stable and scale:

- **Isolated Sandboxes**: Spawning Dockerized agents will use base images configured in `igris.yaml` and spawn temporary containers on the host, referencing scripts in `igris/skills/` without altering host files.
- **Incremental Indexing**: The `igris/cartographer` uses AST extractors to scan the workspace and populate a local vectorized memory cache, allowing agents to query functions and dependencies dynamically.
- **Adding Custom Skills**: New agent workflows can be seamlessly registered by creating a directory inside `igris/skills/` which is scanned by the core model indexer.

---

## 10. Structure Templates

### New Skill Template
To add a capability inside `igris/skills/security/new-skill-name/`:

1. **`SKILL.md`**:
   ```markdown
   ---
   name: new-skill-name
   description: >
     Brief outline of what this skill does.
     Trigger: "trigger phrase 1", "trigger phrase 2".
   ---
   
   # New Skill Title
   
   ## Description
   Outline of behaviors.
   
   ## Requirements
   - Tools required
   - Inputs/Outputs specifications
   ```
2. **`references/api-reference.md`**:
   ```markdown
   # API Reference
   List of commands, endpoints, or variables utilized in this skill.
   ```
3. **`scripts/agent.py`**:
   ```python
   # Execution code for the agent
   def execute(context: dict) -> bool:
       print("Executing skill...")
       return True
   ```

### New API Route Template
To add a route `igris/api/routes/new_route.py`:
```python
from fastapi import APIRouter, Depends
from igris.api.auth import verify_token

router = APIRouter(prefix="/new-route", tags=["new"])

@router.get("/")
def get_data(token: str = Depends(verify_token)):
    return {"status": "success", "data": []}
```

### New Test File Template
To add a test file `igris/tests/test_new_feature.py`:
```python
import pytest

def test_new_feature_behavior():
    assert True
```

---

## 11. Structure Enforcement

- **Validation Checks**: [contract_validator.py](file:///c:/Users/willi/the-system/igris/core/contract_validator.py) automatically enforces message envelope schemas, preventing corrupted states.
- **Test Integrity**: Continuous testing is executed locally via:
  ```bash
  python -m pytest igris/tests/
  ```
- **Blueprint Maintenance**: This blueprint should be updated when new directories, framework frameworks, or tooling dependencies are added to the system.

---

## 12. Known Structural Issues and Technical Debt

Based on current repository audits, the following issues represent technical debt and structural misalignment to be resolved:

1. **Web & API Integration Gap**: The static files under `igris/web/` currently use mock data endpoints, and the FastAPI server under `igris/api/` does not implement the WebSocket stream mapping needed to push real-time agent updates.
2. **Redundant Planning Files**: The `Overwatch/` planning directory contains three partially overlapping plans (`OVERWATCH_MASTER_PLAN.md`, `WEBAPP-PROTOTYPE-PLAN.md`, and `WILLIAM-COLLAB-PLAN.md`) which should be unified into a single active plan.
3. **Unused Capabilities**: While `igris/skills/security/` defines 754 capabilities, none are actively wired into any orchestrator routes or contract handler schemas.
4. **Unexecuted Spikes**: The four spike sub-folders under `Overwatch/spikes/` represent validated concepts but have not yet been run on the host computer to check dependency compliance.
5. **Backup Cleanup**: Backup artifacts such as the `archive/` folder and loose `*.bak` python source files under `igris/` need to be regularly cleared from active repository commits.

*Last Updated: 2026-06-20*
