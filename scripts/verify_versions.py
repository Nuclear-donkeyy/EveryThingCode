from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = ["id:", "name:", "version:", "policy:", "official_source:", "checked_at:"]
EXPECTED_LANGUAGES = 12
EXPECTED_FRAMEWORKS = 27


def block_between(text: str, start: str, end: str | None = None) -> str:
    start_index = text.index(start)
    if end is None:
        return text[start_index:]
    end_index = text.index(end, start_index + len(start))
    return text[start_index:end_index]


def entries(block: str) -> list[str]:
    parts = re.split(r"\n(?=  - id: )", block.strip())
    return [part for part in parts if part.startswith("- id:") or part.startswith("  - id:")]


def main() -> int:
    versions = ROOT / "versions.yaml"
    text = versions.read_text(encoding="utf-8")
    failures: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in text:
            failures.append(f"versions.yaml missing field marker: {field}")

    for section in ["languages:", "frameworks:"]:
        if section not in text:
            failures.append(f"versions.yaml missing section: {section}")

    if not failures:
        language_entries = entries(block_between(text, "languages:", "frameworks:"))
        framework_entries = entries(block_between(text, "frameworks:"))
        if len(language_entries) != EXPECTED_LANGUAGES:
            failures.append(f"expected {EXPECTED_LANGUAGES} language entries, found {len(language_entries)}")
        if len(framework_entries) != EXPECTED_FRAMEWORKS:
            failures.append(f"expected {EXPECTED_FRAMEWORKS} framework entries, found {len(framework_entries)}")
        for entry in language_entries + framework_entries:
            if 'policy: "latest-stable-no-lts"' in entry and "lts: true" in entry:
                failures.append("no-lts entry is marked lts: true")
            if "official_source: \"http" not in entry:
                failures.append(f"entry missing official URL: {entry.splitlines()[0]}")

    for readme in list((ROOT / "languages").glob("*/README.md")) + list((ROOT / "frameworks").glob("*/*/README.md")):
        body = readme.read_text(encoding="utf-8")
        if "## 版本来源" not in body:
            failures.append(f"{readme.relative_to(ROOT)} missing version source section")
        if "校验日期" not in body:
            failures.append(f"{readme.relative_to(ROOT)} missing checked date")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: version metadata and source sections are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
