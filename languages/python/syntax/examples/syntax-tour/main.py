from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable, List, Optional, Tuple


DEFAULT_OWNER = "learning-team"


@dataclass
class Task:
    title: str
    priority: int
    done: bool = False
    owner: str = DEFAULT_OWNER

    def __post_init__(self) -> None:
        if not self.title:
            raise ValueError("task title must not be empty")
        if self.priority < 1:
            raise ValueError("priority must be positive")


def parse_priority(raw_value: str, default: int = 1) -> int:
    try:
        return int(raw_value)
    except ValueError:
        print(f"Invalid priority {raw_value!r}; using default {default}.")
        return default


def status_label(task: Task) -> str:
    if task.done:
        return "done"
    if task.priority >= 3:
        return "urgent"
    return "open"


def collect_tags(tasks: Iterable[Task], extra_tags: Optional[List[str]] = None) -> List[str]:
    tags = [] if extra_tags is None else list(extra_tags)
    for task in tasks:
        tags.append(task.owner)
        if task.priority >= 3:
            tags.append("high-priority")
    return tags


def summarize(tasks: Iterable[Task]) -> Tuple[int, int]:
    done_count = 0
    open_count = 0

    for task in tasks:
        if task.done:
            done_count += 1
            continue
        open_count += 1

    return done_count, open_count


def write_report(path: Path, tasks: List[Task]) -> str:
    lines = [f"{index}. [{status_label(task)}] {task.title}" for index, task in enumerate(tasks, start=1)]

    with path.open("w", encoding="utf-8") as report:
        report.write("\n".join(lines))
        report.write("\n")

    with path.open("r", encoding="utf-8") as report:
        return report.read()


def main() -> None:
    tasks = [
        Task("Read syntax guide", priority=1, done=True),
        Task("Run the syntax tour", priority=2),
        Task("Explain default arguments", priority=parse_priority("high")),
        Task("Refactor repeated imports", priority=3, owner="platform"),
    ]

    for attempt in range(1, 4):
        print(f"Attempt {attempt}: inspecting {len(tasks)} tasks")

    status_counts = {"done": 0, "urgent": 0, "open": 0}
    for task in tasks:
        status_counts[status_label(task)] += 1

    unique_tags = {tag.lower() for tag in collect_tags(tasks, extra_tags=["Python", "Syntax"])}
    done_count, open_count = summarize(tasks)

    print(f"Summary: {done_count} done, {open_count} open")
    print(f"Status counts: {status_counts}")
    print(f"Tags: {sorted(unique_tags)}")

    with TemporaryDirectory() as temporary_directory:
        report_path = Path(temporary_directory) / "task-report.txt"
        content = write_report(report_path, tasks)
        print(f"Report path: {report_path}")
        print(content)


if __name__ == "__main__":
    main()
