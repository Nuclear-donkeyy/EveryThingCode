from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LANGUAGES = {
    "java": ["spring-boot"],
    "javascript-typescript": ["react", "vue", "angular", "sveltekit", "nextjs", "nestjs"],
    "python": ["django", "fastapi"],
    "go": ["net-http", "gin"],
    "rust": ["axum", "actix-web"],
    "csharp-dotnet": ["aspnet-core"],
    "kotlin": ["ktor", "compose-multiplatform"],
    "php": ["laravel", "symfony"],
    "c-cpp": ["cmake", "qt", "boost"],
    "ruby": ["rails", "sinatra"],
    "swift": ["swiftui", "vapor"],
    "dart": ["flutter", "shelf"],
}

LANGUAGE_INDEX_SECTIONS = [
    "## 常用框架清单",
    "## 选择思路",
    "## 学习路线",
    "## 本仓库案例",
]

FRAMEWORK_SECTIONS = [
    "## 核心定位",
    "## 设计思想",
    "## 架构模型",
    "## 请求/执行生命周期",
    "## 工程结构",
    "## 配置方式",
    "## 模块与依赖管理",
    "## 数据访问",
    "## 测试方式",
    "## 部署方式",
    "## 适用场景与取舍",
    "## 案例索引",
    "## 版本来源",
]

EXAMPLE_SECTIONS = [
    "## 目标",
    "## 学习重点",
    "## 工程结构",
    "## 运行前提",
    "## 运行",
    "## 预期输出",
    "## 代码讲解",
    "## 延伸练习",
    "## 验收",
]


def missing_sections(text: str, sections: list[str]) -> list[str]:
    return [section for section in sections if section not in text]


def has_bash_command(text: str) -> bool:
    lines = text.splitlines()
    in_bash = False
    for line in lines:
        if line.strip() == "```bash":
            in_bash = True
            continue
        if in_bash and line.strip() == "```":
            in_bash = False
            continue
        if in_bash:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return True
    return False


def example_has_project_files(path: Path) -> bool:
    ignored = {"README.md", "NOTES.md"}
    return any(child.is_file() and child.name not in ignored for child in path.rglob("*"))


def main() -> int:
    failures: list[str] = []
    frameworks_root = ROOT / "frameworks"

    for language, frameworks in LANGUAGES.items():
        index = frameworks_root / language / "README.md"
        if not index.exists():
            failures.append(f"{index.relative_to(ROOT)} missing")
        else:
            text = index.read_text(encoding="utf-8")
            for section in missing_sections(text, LANGUAGE_INDEX_SECTIONS):
                failures.append(f"{index.relative_to(ROOT)} missing {section}")
            for framework in frameworks:
                if f"({framework}/)" not in text and f"]({framework})" not in text:
                    failures.append(f"{index.relative_to(ROOT)} does not link {framework}")

        for framework in frameworks:
            framework_dir = frameworks_root / language / framework
            readme = framework_dir / "README.md"
            if not readme.exists():
                failures.append(f"{readme.relative_to(ROOT)} missing")
                continue
            text = readme.read_text(encoding="utf-8")
            for section in missing_sections(text, FRAMEWORK_SECTIONS):
                failures.append(f"{readme.relative_to(ROOT)} missing {section}")
            if len(text) < 2200:
                failures.append(f"{readme.relative_to(ROOT)} is too thin for teaching content")

            example = framework_dir / "examples" / "quickstart"
            example_readme = example / "README.md"
            if not example_readme.exists():
                failures.append(f"{example_readme.relative_to(ROOT)} missing")
                continue
            example_text = example_readme.read_text(encoding="utf-8")
            for section in missing_sections(example_text, EXAMPLE_SECTIONS):
                failures.append(f"{example_readme.relative_to(ROOT)} missing {section}")
            if not has_bash_command(example_text):
                failures.append(f"{example_readme.relative_to(ROOT)} missing runnable bash command")
            if len(example_text) < 1800:
                failures.append(f"{example_readme.relative_to(ROOT)} is too thin for example teaching")
            if not example_has_project_files(example):
                failures.append(f"{example.relative_to(ROOT)} has no project/source files")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("OK: framework teaching modules are complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
