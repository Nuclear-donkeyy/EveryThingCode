from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def command_from_readme(readme: Path) -> str | None:
    lines = readme.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "```bash":
            if index + 1 < len(lines):
                command = lines[index + 1].strip()
                if command and not command.startswith("#"):
                    return command
    return None


def executable_available(command: str) -> bool:
    first = command.split()[0]
    if first in {"javac", "python3", "node", "go", "rustc", "dotnet", "kotlin", "php", "c++", "ruby", "swift", "dart"}:
        return shutil.which(first) is not None
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="run examples when the required tool is installed")
    parser.add_argument("--dry-run", action="store_true", help="print discovered commands without executing")
    args = parser.parse_args()

    failures: list[str] = []
    readmes = sorted((ROOT / "languages").glob("*/examples/*/README.md"))
    if not readmes:
        failures.append("no language example README files found")

    for readme in readmes:
        command = command_from_readme(readme)
        rel = readme.parent.relative_to(ROOT)
        if not command:
            failures.append(f"{rel} missing bash command")
            continue
        print(f"FOUND: {rel}: {command}")
        if args.execute:
            if not executable_available(command):
                print(f"SKIP: tool not installed for {rel}")
                continue
            result = subprocess.run(command, cwd=readme.parent, shell=True, text=True, capture_output=True, timeout=20)
            if result.returncode != 0:
                failures.append(f"{rel} failed: {result.stderr.strip() or result.stdout.strip()}")

    framework_readmes = sorted((ROOT / "frameworks").glob("*/*/examples/quickstart/README.md"))
    if not framework_readmes:
        failures.append("no framework quickstart README files found")
    for readme in framework_readmes:
        body = readme.read_text(encoding="utf-8")
        if "## 验收" not in body:
            failures.append(f"{readme.parent.relative_to(ROOT)} missing acceptance section")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: smoke structure checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
