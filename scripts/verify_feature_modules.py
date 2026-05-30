from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_DIR = ROOT / "languages"
REQUIRED_FEATURE_HEADINGS = [
    "## 如何使用",
    "## 思想总览",
    "## 核心特性地图",
    "## 教学例子索引",
    "## 学习检查",
]
REQUIRED_EXAMPLE_HEADINGS = ["## 目标", "## 运行", "## 观察点"]
MIN_FEATURE_CHARS = 1200
MIN_EXAMPLES = 3


def has_bash_command(text: str) -> bool:
    lines = text.splitlines()
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
            return True
    return False


def main() -> int:
    failures: list[str] = []
    languages = sorted(path for path in LANGUAGE_DIR.iterdir() if path.is_dir())

    if len(languages) != 12:
        failures.append(f"expected 12 language directories, found {len(languages)}")

    for language in languages:
        rel = language.relative_to(ROOT)
        language_readme = language / "README.md"
        if "features/" not in language_readme.read_text(encoding="utf-8"):
            failures.append(f"{rel}/README.md missing features link")

        feature_readme = language / "features" / "README.md"
        if not feature_readme.exists():
            failures.append(f"{rel}/features/README.md missing")
            continue

        feature_body = feature_readme.read_text(encoding="utf-8")
        for heading in REQUIRED_FEATURE_HEADINGS:
            if heading not in feature_body:
                failures.append(f"{feature_readme.relative_to(ROOT)} missing heading: {heading}")
        nonspace_chars = sum(1 for char in feature_body if not char.isspace())
        if nonspace_chars < MIN_FEATURE_CHARS:
            failures.append(f"{feature_readme.relative_to(ROOT)} too short: {nonspace_chars} non-space chars")

        examples_root = language / "features" / "examples"
        example_readmes = sorted(examples_root.glob("*/README.md"))
        if len(example_readmes) < MIN_EXAMPLES:
            failures.append(f"{examples_root.relative_to(ROOT)} expected at least {MIN_EXAMPLES} examples, found {len(example_readmes)}")
            continue

        for readme in example_readmes:
            body = readme.read_text(encoding="utf-8")
            for heading in REQUIRED_EXAMPLE_HEADINGS:
                if heading not in body:
                    failures.append(f"{readme.relative_to(ROOT)} missing heading: {heading}")
            if not has_bash_command(body):
                failures.append(f"{readme.relative_to(ROOT)} missing runnable bash command")
            source_files = [path for path in readme.parent.iterdir() if path.is_file() and path.name != "README.md"]
            if not source_files:
                failures.append(f"{readme.parent.relative_to(ROOT)} missing source file")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: feature teaching modules are present and runnable commands are documented")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
