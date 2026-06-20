"""
CLI entry point for Commander Igris.

Usage:
  python -m igris.cli.main            # Direct Chat (default)
  python -m igris.cli.main run        # Direct Chat
  python -m igris.cli.main status     # Print system status
  python -m igris.cli.main validate   # Validate contracts
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def cmd_chat(data_dir: str = "data", interval: int = 5) -> None:
    """Start Igris Direct Chat."""
    from igris.core.orchestrator import IgrisOrchestrator
    igris = IgrisOrchestrator(data_dir=Path(data_dir))
    igris.chat(interval_s=interval)


def cmd_status(data_dir: str = "data") -> None:
    """Print system status."""
    from igris.core.orchestrator import IgrisOrchestrator
    igris = IgrisOrchestrator(data_dir=Path(data_dir))
    igris._print_status()
    print()
    print("Agents:")
    for agent in igris.agents.values():
        print(f"  {agent.agent_id}: rank={agent.rank.value} status={agent.status.value} "
              f"tasks={agent.tasks_completed} success={agent.success_rate:.0%}")
    print(f"\nTasks ({len(igris.tasks)} total):")
    for task in igris.tasks.values():
        print(f"  {task.task_id}: [{task.priority.value}] {task.status.value} — {task.description[:60]}")


def cmd_validate() -> None:
    """Validate all contracts."""
    from igris.core.contract_validator import ContractValidator, ContractType
    validator = ContractValidator()
    print("Contract Schema Registry:")
    print("-" * 40)
    test_payloads = {
        ContractType.AGENT_SPAWN_REQUEST: {
            "contract_type": "agent_spawn_request", "sender_id": "test",
            "payload": {"name": "test-agent", "language": "python"},
        },
        ContractType.TASK_ASSIGN: {
            "contract_type": "task_assign", "sender_id": "test",
            "payload": {"task_id": "t1", "agent_id": "a1", "description": "Test"},
        },
        ContractType.AGENT_PROMOTE: {
            "contract_type": "agent_promote", "sender_id": "test",
            "payload": {"agent_id": "a1", "from_rank": "level_0", "to_rank": "b_rank", "reason": "test"},
        },
        ContractType.HEARTBEAT: {
            "contract_type": "heartbeat", "sender_id": "test",
            "payload": {"agent_id": "a1", "sequence": 0},
        },
    }
    all_ok = True
    for ct, payload in test_payloads.items():
        result = validator.validate(payload)
        status = "PASS" if result.valid else "FAIL"
        if not result.valid:
            all_ok = False
        print(f"  {ct.value:30s} -> {status}")
        if result.errors:
            for err in result.errors:
                print(f"    Error: {err[:100]}")
    print("-" * 40)
    print(f"Overall: {'ALL PASSED' if all_ok else 'SOME FAILED'}")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "chat"
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "data"

    if cmd in ("chat", "run"):
        cmd_chat(data_dir=data_dir)
    elif cmd == "status":
        cmd_status(data_dir=data_dir)
    elif cmd == "validate":
        cmd_validate()
    else:
        print(f"Unknown: {cmd}")
        print("Usage: python -m igris.cli.main [chat|status|validate]")
        sys.exit(1)


if __name__ == "__main__":
    main()
