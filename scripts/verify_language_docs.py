from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_HEADINGS = [
    "## 语言定位",
    "## 适合场景",
    "## 核心语法",
    "## 类型/内存/并发模型",
    "## 标准库与包管理",
    "## 错误处理",
    "## 工程化",
    "## 常见坑",
    "## 案例索引",
    "## 版本来源",
]
REQUIRED_CASES = ["examples/hello/", "examples/data-flow/", "examples/errors/"]
MIN_NONSPACE_CHARS = 1000


def main() -> int:
    failures: list[str] = []
    readmes = sorted((ROOT / "languages").glob("*/README.md"))

    if len(readmes) != 12:
        failures.append(f"expected 12 language README files, found {len(readmes)}")

    for readme in readmes:
        body = readme.read_text(encoding="utf-8")
        rel = readme.relative_to(ROOT)
        for heading in REQUIRED_HEADINGS:
            if heading not in body:
                failures.append(f"{rel} missing heading: {heading}")
        for case in REQUIRED_CASES:
            if case not in body:
                failures.append(f"{rel} missing case link: {case}")
        nonspace_chars = sum(1 for char in body if not char.isspace())
        if nonspace_chars < MIN_NONSPACE_CHARS:
            failures.append(f"{rel} is too short: {nonspace_chars} non-space chars")
        if "官方来源：" not in body or "校验日期：" not in body:
            failures.append(f"{rel} missing version source metadata")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: language docs are detailed and structurally complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
