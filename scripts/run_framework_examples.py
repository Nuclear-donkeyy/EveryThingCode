from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_CACHE = Path("/tmp/everythingcode-framework-smoke")

TOOL_NAMES = {
    "java",
    "javac",
    "mvn",
    "gradle",
    "node",
    "npm",
    "pnpm",
    "python",
    "python3",
    "go",
    "cargo",
    "rustc",
    "dotnet",
    "kotlinc",
    "kotlin",
    "php",
    "composer",
    "cmake",
    "c++",
    "clang++",
    "g++",
    "ruby",
    "bundle",
    "swift",
    "dart",
    "flutter",
}


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


def first_tool(command: str) -> str | None:
    try:
        parts = shlex.split(command)
    except ValueError:
        return None
    if not parts:
        return None
    if parts[0] in {"env", "time"} and len(parts) > 1:
        return parts[1]
    return parts[0]


def executable_available(command: str) -> bool:
    tool = first_tool(command)
    if tool is None:
        return False
    if tool not in TOOL_NAMES:
        return True
    return shutil.which(tool) is not None


def execution_env(command: str) -> dict[str, str]:
    env = os.environ.copy()
    tool = first_tool(command)

    if tool in {"python", "python3"}:
        pycache = RUN_CACHE / "pycache"
        pycache.mkdir(parents=True, exist_ok=True)
        env["PYTHONPYCACHEPREFIX"] = str(pycache)

    if tool == "swift":
        swift_home = RUN_CACHE / "swift-home"
        module_cache = RUN_CACHE / "swift-module-cache"
        swift_home.mkdir(parents=True, exist_ok=True)
        module_cache.mkdir(parents=True, exist_ok=True)
        env["HOME"] = str(swift_home)
        env["XDG_CACHE_HOME"] = str(swift_home / ".cache")
        env["CLANG_MODULE_CACHE_PATH"] = str(module_cache)

    return env


def known_environment_failure(command: str, message: str) -> str | None:
    tool = first_tool(command)
    if tool == "swift" and (
        "SDK is not supported by the compiler" in message
        or "could not build Objective-C module 'SwiftShims'" in message
        or "org.swift.swiftpm" in message
    ):
        return "Swift toolchain/cache is not usable in this environment"

    if tool in {"python", "python3"} and "com.apple.python" in message and "Operation not permitted" in message:
        return "Python bytecode cache is not writable in this environment"

    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="run quickstarts when the required tool exists")
    parser.add_argument("--dry-run", action="store_true", help="print discovered commands")
    args = parser.parse_args()

    failures: list[str] = []
    readmes = sorted((ROOT / "frameworks").glob("*/*/examples/quickstart/README.md"))
    if not readmes:
        failures.append("no framework quickstart README files found")

    for readme in readmes:
        command = command_from_readme(readme)
        rel = readme.parent.relative_to(ROOT)
        if not command:
            failures.append(f"{rel} missing runnable command")
            continue
        print(f"FOUND: {rel}: {command}")
        if args.execute:
            if not executable_available(command):
                print(f"SKIP: tool not installed for {rel}")
                continue
            result = subprocess.run(
                command,
                cwd=readme.parent,
                shell=True,
                text=True,
                capture_output=True,
                timeout=30,
                env=execution_env(command),
            )
            if result.returncode != 0:
                message = result.stderr.strip() or result.stdout.strip()
                skip_reason = known_environment_failure(command, message)
                if skip_reason:
                    print(f"SKIP: {skip_reason} for {rel}")
                    continue
                failures.append(f"{rel} failed: {message}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: framework example commands discovered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
