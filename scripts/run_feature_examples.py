from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def command_from_readme(readme: Path) -> str | None:
    lines = readme.read_text(encoding="utf-8").splitlines()
    in_bash = False
    for line in lines:
        stripped = line.strip()
        if stripped == "```bash":
            in_bash = True
            continue
        if in_bash and stripped == "```":
            in_bash = False
            continue
        if in_bash and stripped and not stripped.startswith("#"):
            return stripped
    return None


def command_cwd(command: str, example_dir: Path) -> Path:
    if command.strip().startswith("cd ") and "&&" in command:
        prefix = command.split("&&", 1)[0].strip()
        parts = shlex.split(prefix)
        if len(parts) >= 2:
            path = Path(parts[1])
            return path if path.is_absolute() else ROOT / path
    return example_dir


def executable_part(command: str) -> str:
    if command.strip().startswith("cd ") and "&&" in command:
        return command.split("&&", 1)[1].strip()
    return command


def first_tool(command: str) -> str:
    return executable_part(command).split()[0]


def tool_available(command: str) -> bool:
    tool = first_tool(command)
    return shutil.which(tool) is not None


def is_environment_failure(output: str) -> bool:
    markers = [
        "Unable to locate a Java Runtime",
        "could not build Objective-C module 'SwiftShims'",
        "this SDK is not supported by the compiler",
        "unable to open output file",
        "Operation not permitted",
    ]
    return any(marker in output for marker in markers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="run examples when the required tool is installed")
    parser.add_argument("--dry-run", action="store_true", help="list discovered commands without running")
    args = parser.parse_args()

    failures: list[str] = []
    readmes = sorted((ROOT / "languages").glob("*/features/examples/*/README.md"))
    if not readmes:
        failures.append("no feature example README files found")

    for readme in readmes:
        rel = readme.parent.relative_to(ROOT)
        command = command_from_readme(readme)
        if not command:
            failures.append(f"{rel} missing runnable bash command")
            continue

        print(f"FOUND: {rel}: {command}")
        if not args.execute:
            continue

        if not tool_available(command):
            print(f"SKIP: {first_tool(command)} is not installed for {rel}")
            continue

        env = os.environ.copy()
        env.setdefault("CLANG_MODULE_CACHE_PATH", "/tmp/clang-module-cache")
        env.setdefault("SWIFT_MODULE_CACHE_PATH", "/tmp/swift-module-cache")
        result = subprocess.run(
            executable_part(command),
            cwd=command_cwd(command, readme.parent),
            shell=True,
            text=True,
            capture_output=True,
            env=env,
            timeout=30,
        )
        if result.returncode != 0:
            output = result.stderr.strip() or result.stdout.strip()
            if is_environment_failure(output):
                print(f"SKIP: local toolchain is not usable for {rel}: {output.splitlines()[0]}")
                continue
            failures.append(f"{rel} failed: {output}")
        else:
            print(f"OK: {rel}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: feature example command scan completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
