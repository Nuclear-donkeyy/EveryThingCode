from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGE_DIR = ROOT / "languages"
REQUIRED_SYNTAX_HEADINGS = [
    "## 读者定位",
    "## 运行方式",
    "## 语法速览",
    "## 类型与值",
    "## 控制流",
    "## 函数与模块",
    "## 集合与数据建模",
    "## 错误处理",
    "## 惯用写法",
    "## 可运行示例",
    "## 学习检查",
]
REQUIRED_EXAMPLE_HEADINGS = [
    "## 目标",
    "## 覆盖语法",
    "## 运行",
    "## 观察点",
    "## 修改练习",
]
MIN_SYNTAX_CHARS = 1800
MIN_EXAMPLE_CHARS = 600


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
        if "syntax/" not in language_readme.read_text(encoding="utf-8"):
            failures.append(f"{rel}/README.md missing syntax link")

        syntax_readme = language / "syntax" / "README.md"
        if not syntax_readme.exists():
            failures.append(f"{rel}/syntax/README.md missing")
            continue

        syntax_body = syntax_readme.read_text(encoding="utf-8")
        for heading in REQUIRED_SYNTAX_HEADINGS:
            if heading not in syntax_body:
                failures.append(f"{syntax_readme.relative_to(ROOT)} missing heading: {heading}")
        syntax_chars = sum(1 for char in syntax_body if not char.isspace())
        if syntax_chars < MIN_SYNTAX_CHARS:
            failures.append(f"{syntax_readme.relative_to(ROOT)} too short: {syntax_chars} non-space chars")

        example_readme = language / "syntax" / "examples" / "syntax-tour" / "README.md"
        if not example_readme.exists():
            failures.append(f"{rel}/syntax/examples/syntax-tour/README.md missing")
            continue

        example_body = example_readme.read_text(encoding="utf-8")
        for heading in REQUIRED_EXAMPLE_HEADINGS:
            if heading not in example_body:
                failures.append(f"{example_readme.relative_to(ROOT)} missing heading: {heading}")
        example_chars = sum(1 for char in example_body if not char.isspace())
        if example_chars < MIN_EXAMPLE_CHARS:
            failures.append(f"{example_readme.relative_to(ROOT)} too short: {example_chars} non-space chars")
        if not has_bash_command(example_body):
            failures.append(f"{example_readme.relative_to(ROOT)} missing runnable bash command")

        source_files = [
            path
            for path in example_readme.parent.iterdir()
            if path.is_file() and path.name != "README.md"
        ]
        if not source_files:
            failures.append(f"{example_readme.parent.relative_to(ROOT)} missing source file")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: syntax quickstarts are present and documented")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
