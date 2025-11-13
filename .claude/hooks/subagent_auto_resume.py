#!/usr/bin/env python3
"""
Stop hook that reminds Claude Code to resume unfinished subagent work.

Triggered after the main run reaches the Stop stage. It inspects TODO.md to
detect remaining high-priority tasks, maps them to their designated subagents,
and emits a strong prompt telling Claude to spin up the next subagent so the
workflow can continue autonomously.
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

# Priority buckets used to sort pending work (lower value = higher urgency)
PRIORITY_WEIGHTS = {
    "P0": 0,
    "HIGH": 0,
    "高": 0,
    "P1": 1,
    "MEDIUM": 2,
    "中": 2,
    "P2": 2,
    "P3": 3,
    "LOW": 3,
    "低": 3,
}


@dataclass
class ModuleMeta:
    module_id: str
    title: Optional[str]
    subagent: Optional[str]
    task_path: Optional[str]


@dataclass
class PendingTask:
    order: int
    summary: str
    priority: str
    module_id: Optional[str]
    raw_line: str
    module_meta: Optional[ModuleMeta]


def read_event_payload() -> Dict:
    """Read JSON payload from stdin if present (Stop event metadata)."""
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except Exception:
        return {}


def load_module_metadata() -> Dict[str, ModuleMeta]:
    """Build a mapping of module id -> metadata from docs/admin-modules."""
    modules_dir = Path("docs/admin-modules")
    metadata: Dict[str, ModuleMeta] = {}

    if not modules_dir.exists():
        return metadata

    for task_file in modules_dir.glob("**/TASK*.md"):
        try:
            text = task_file.read_text(encoding="utf-8")
        except Exception:
            continue

        id_match = re.search(r"\*\*模块编号\*\*:\s*0*(\d+)", text)
        subagent_match = re.search(r"\*\*负责\s*Subagent\*\*:\s*([A-Za-z0-9_\-]+)", text)
        title_match = re.search(r"#\s*模块\s*\d+\s*[:：]\s*([^\n]+)", text)

        if not id_match:
            continue

        module_id = id_match.group(1).zfill(2)
        metadata[module_id] = ModuleMeta(
            module_id=module_id,
            title=title_match.group(1).strip() if title_match else None,
            subagent=subagent_match.group(1).strip() if subagent_match else None,
            task_path=str(task_file),
        )

    return metadata


def parse_priority(raw_line: str) -> str:
    """Extract the priority token from the TODO line."""
    match = re.search(r"优先级[:：]\s*([A-Za-z0-9Pp]+|[\u4e00-\u9fa5]+)", raw_line)
    if not match:
        return "P2"
    return match.group(1).upper()


def collect_pending_tasks(todo_path: Path, module_meta: Dict[str, ModuleMeta]) -> List[PendingTask]:
    """Parse TODO.md and collect unchecked tasks."""
    tasks: List[PendingTask] = []
    if not todo_path.exists():
        return tasks

    try:
        lines = todo_path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return tasks

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("- [ ]"):
            continue

        content = stripped[len("- [ ]"):].strip()
        module_match = re.search(r"模块\s*(\d+)", content)
        module_id = module_match.group(1).zfill(2) if module_match else None
        priority = parse_priority(content)
        summary = content.split(" - ", 1)[0].strip()
        meta = module_meta.get(module_id) if module_id else None

        tasks.append(
            PendingTask(
                order=idx,
                summary=summary,
                priority=priority,
                module_id=module_id,
                raw_line=content,
                module_meta=meta,
            )
        )

    tasks.sort(
        key=lambda task: (
            PRIORITY_WEIGHTS.get(task.priority.upper(), 99),
            task.order,
        )
    )
    return tasks


def build_prompt(stop_reason: Optional[str], pending: List[PendingTask]) -> str:
    """Create a natural-language prompt Claude can execute immediately."""
    total = len(pending)
    top_tasks = pending[:3]

    lines = [
        "Stop hook report:",
        f"- Remaining tasks in TODO.md: {total}",
    ]

    if stop_reason:
        lines.append(f"- Stop reason: {stop_reason}")

    lines.append("")
    lines.append("Highest-priority work to resume now:")

    for idx, task in enumerate(top_tasks, start=1):
        descriptor = f"{idx}. {task.summary.strip()}"
        descriptor += f" (priority {task.priority})"
        if task.module_meta:
            meta_bits = []
            if task.module_meta.subagent:
                meta_bits.append(f"subagent `{task.module_meta.subagent}`")
            if task.module_meta.task_path:
                meta_bits.append(f"brief {task.module_meta.task_path}")
            if meta_bits:
                descriptor += f" – " + ", ".join(meta_bits)
        lines.append(descriptor)

    lines.extend(
        [
            "",
            "Action:",
            "1. Immediately spin up the appropriate subagent for the top task above.",
            "2. Re-read the task brief, resume execution, and continue iterating until the task is completed or blocked.",
            "3. If the previous run stopped mid-stream, continue from the exact point of interruption.",
            "4. When handing off between agents, update `TODO.md` accordingly.",
        ]
    )

    return "\n".join(lines)


def main():
    payload = read_event_payload()
    stop_reason = payload.get("reason") or payload.get("stop_reason")

    module_meta = load_module_metadata()
    pending_tasks = collect_pending_tasks(Path("TODO.md"), module_meta)

    if not pending_tasks:
        sys.exit(0)

    prompt = build_prompt(stop_reason, pending_tasks)

    # Emit human-readable summary to stderr for logs.
    print(prompt, file=sys.stderr)

    # Claude Stop hooks expect JSON on stdout when issuing follow-up prompts.
    json.dump({"type": "prompt", "prompt": prompt}, sys.stdout, ensure_ascii=False)
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    main()
