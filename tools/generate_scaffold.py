from __future__ import annotations

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
CHECKED_DATE = "2026-05-30"


LANGUAGES = [
    {
        "key": "java",
        "name": "Java",
        "version": "25 LTS",
        "runtime": "JDK 25",
        "policy": "latest-lts",
        "source": "https://www.oracle.com/java/technologies/java-se-support-roadmap.html",
        "extension": "java",
        "package": "Maven / Gradle",
        "typing": "静态、名义类型、泛型擦除",
        "concurrency": "线程、虚拟线程、结构化并发",
        "error": "受检异常、运行时异常、try-with-resources",
        "scenario": "企业服务、Android 生态、数据平台、中间件",
    },
    {
        "key": "javascript-typescript",
        "name": "JavaScript / TypeScript",
        "version": "Node.js 24.16.0 LTS",
        "runtime": "Node.js 24.16.0",
        "policy": "latest-active-lts",
        "source": "https://nodejs.org/en/about/previous-releases",
        "extension": "mjs",
        "package": "npm / pnpm / yarn",
        "typing": "JS 动态类型，TS 结构化静态类型",
        "concurrency": "事件循环、Promise、async/await、Worker",
        "error": "Error 对象、Promise rejection、Result 风格封装",
        "scenario": "Web 前端、Node 服务、全栈应用、工具链",
    },
    {
        "key": "python",
        "name": "Python",
        "version": "3.14.5",
        "runtime": "Python 3.14.5",
        "policy": "latest-supported-stable",
        "source": "https://devguide.python.org/versions/",
        "extension": "py",
        "package": "pip / uv / poetry",
        "typing": "动态类型，typing 提供渐进式类型",
        "concurrency": "asyncio、线程、多进程",
        "error": "异常层级、上下文管理器、EAFP",
        "scenario": "自动化、AI/数据、Web API、脚本工具",
    },
    {
        "key": "go",
        "name": "Go",
        "version": "1.26.3",
        "runtime": "Go 1.26.3",
        "policy": "latest-supported-stable",
        "source": "https://go.dev/doc/devel/release",
        "extension": "go",
        "package": "Go modules",
        "typing": "静态类型、结构化接口、泛型",
        "concurrency": "goroutine、channel、context",
        "error": "显式 error 返回、errors.Is/As、defer",
        "scenario": "云原生、微服务、CLI、基础设施",
    },
    {
        "key": "rust",
        "name": "Rust",
        "version": "1.96.x",
        "runtime": "Rust stable",
        "policy": "latest-stable-no-lts",
        "source": "https://blog.rust-lang.org/",
        "extension": "rs",
        "package": "Cargo",
        "typing": "静态类型、代数数据类型、trait",
        "concurrency": "所有权、Send/Sync、async runtime",
        "error": "Result、Option、?、panic 边界",
        "scenario": "系统编程、性能服务、嵌入式、WebAssembly",
    },
    {
        "key": "csharp-dotnet",
        "name": "C# / .NET",
        "version": ".NET 10.0.8 LTS",
        "runtime": ".NET SDK 10.0.8",
        "policy": "latest-lts",
        "source": "https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core",
        "extension": "cs",
        "package": "NuGet",
        "typing": "静态类型、泛型、nullable reference types",
        "concurrency": "Task、async/await、TPL",
        "error": "异常、using、Result/OneOf 风格",
        "scenario": "企业后端、桌面、游戏、云服务",
    },
    {
        "key": "kotlin",
        "name": "Kotlin",
        "version": "2.3.x",
        "runtime": "Kotlin 2.3",
        "policy": "latest-stable-no-lts",
        "source": "https://kotlinlang.org/docs/releases.html",
        "extension": "kts",
        "package": "Gradle / Maven",
        "typing": "静态类型、空安全、协变/逆变",
        "concurrency": "coroutines、Flow、structured concurrency",
        "error": "异常、Result、sealed class 建模",
        "scenario": "Android、服务端、跨平台 UI",
    },
    {
        "key": "php",
        "name": "PHP",
        "version": "8.5.x",
        "runtime": "PHP 8.5",
        "policy": "latest-supported-stable",
        "source": "https://www.php.net/supported-versions.php",
        "extension": "php",
        "package": "Composer",
        "typing": "动态类型增强、strict_types、union/intersection types",
        "concurrency": "请求级并发、Fibers、队列",
        "error": "Throwable、Exception、Error、try/finally",
        "scenario": "Web 应用、CMS、电商、业务后台",
    },
    {
        "key": "c-cpp",
        "name": "C / C++",
        "version": "C23 / C++23",
        "runtime": "C23/C++23 compiler",
        "policy": "latest-published-standards",
        "source": "https://isocpp.org/std/the-standard",
        "extension": "cpp",
        "package": "CMake / Conan / vcpkg",
        "typing": "静态类型、手动内存、模板元编程",
        "concurrency": "线程、原子、协程、执行器生态",
        "error": "C 错误码，C++ 异常/expected/RAII",
        "scenario": "系统、游戏、音视频、数据库、性能核心",
    },
    {
        "key": "ruby",
        "name": "Ruby",
        "version": "4.0.x",
        "runtime": "Ruby stable",
        "policy": "latest-stable-no-lts",
        "source": "https://www.ruby-lang.org/en/downloads/branches/",
        "extension": "rb",
        "package": "Bundler / RubyGems",
        "typing": "动态类型、duck typing、RBS/Sorbet 可选",
        "concurrency": "Fiber、Ractor、线程",
        "error": "异常、ensure、显式领域错误",
        "scenario": "Web 产品、自动化、DSL、脚本工具",
    },
    {
        "key": "swift",
        "name": "Swift",
        "version": "6.3.x",
        "runtime": "Swift 6.3",
        "policy": "latest-stable-no-lts",
        "source": "https://www.swift.org/install/",
        "extension": "swift",
        "package": "Swift Package Manager",
        "typing": "静态类型、协议、值语义、泛型",
        "concurrency": "async/await、actor、Task",
        "error": "throws、Result、defer",
        "scenario": "Apple 平台、服务端、CLI、系统工具",
    },
    {
        "key": "dart",
        "name": "Dart",
        "version": "3.12.x",
        "runtime": "Dart 3.12",
        "policy": "latest-stable-no-lts",
        "source": "https://dart.dev/get-dart/archive",
        "extension": "dart",
        "package": "pub",
        "typing": "静态类型、sound null safety、泛型",
        "concurrency": "Future、Stream、isolate",
        "error": "Exception/Error、try/catch、sealed 结果类型",
        "scenario": "Flutter 应用、跨平台 UI、客户端工具",
    },
]


FRAMEWORKS = [
    ("java", "spring-boot", "Spring Boot", "4.0.x", "https://spring.io/projects/spring-boot", "约定优于配置，把 Spring 生态整合为可独立运行的应用。", "REST API"),
    ("javascript-typescript", "nextjs", "Next.js", "16.x Active LTS", "https://nextjs.org/docs", "以路由、渲染和数据获取为核心组织全栈 React 应用。", "App Router 页面"),
    ("javascript-typescript", "nestjs", "NestJS", "latest stable", "https://docs.nestjs.com/", "用模块、控制器、Provider 和依赖注入组织 Node 服务。", "模块化 API"),
    ("python", "django", "Django", "5.2 LTS", "https://docs.djangoproject.com/en/stable/releases/", "Batteries included，围绕 ORM、Admin、URL 和模板快速交付完整 Web 应用。", "CRUD 后台"),
    ("python", "fastapi", "FastAPI", "latest stable", "https://fastapi.tiangolo.com/", "以类型标注驱动 OpenAPI、校验和异步请求处理。", "JSON API"),
    ("go", "net-http", "net/http", "Go standard library", "https://pkg.go.dev/net/http", "用标准库直接表达 Handler、路由和中间件边界。", "HTTP 服务"),
    ("go", "gin", "Gin", "latest stable", "https://gin-gonic.com/docs/", "轻量路由和中间件栈，适合快速构建 JSON API。", "REST API"),
    ("rust", "axum", "Axum", "latest stable", "https://docs.rs/axum/latest/axum/", "基于 tower/hyper，把路由、提取器和状态组合成类型安全服务。", "异步 API"),
    ("rust", "actix-web", "Actix Web", "latest stable", "https://actix.rs/", "Actor 生态演进出的高性能 Web 框架。", "REST API"),
    ("csharp-dotnet", "aspnet-core", "ASP.NET Core", ".NET 10.0.8 LTS", "https://learn.microsoft.com/aspnet/core/", "通过中间件管线、Minimal API/MVC 和 DI 构建跨平台服务。", "Minimal API"),
    ("kotlin", "ktor", "Ktor", "latest stable", "https://ktor.io/docs/", "以插件和 DSL 组合 HTTP 服务端/客户端能力。", "JSON API"),
    ("kotlin", "compose-multiplatform", "Compose Multiplatform", "latest stable", "https://www.jetbrains.com/compose-multiplatform/", "声明式 UI 和状态驱动渲染，跨桌面/移动/Web 复用模型。", "计数器 UI"),
    ("php", "laravel", "Laravel", "latest supported major", "https://laravel.com/docs/releases", "用优雅语法整合路由、ORM、队列、事件和测试。", "CRUD API"),
    ("php", "symfony", "Symfony", "latest LTS line", "https://symfony.com/releases", "组件化框架，强调可组合、显式配置和长期维护。", "控制器 API"),
    ("c-cpp", "cmake", "CMake", "latest stable", "https://cmake.org/documentation/", "跨平台构建系统，用目标、依赖和生成器描述 C/C++ 工程。", "CLI 构建"),
    ("c-cpp", "qt", "Qt", "latest LTS", "https://www.qt.io/product/qt6", "跨平台 GUI/应用框架，使用对象模型、信号槽和工具链组织应用。", "窗口应用"),
    ("c-cpp", "boost", "Boost", "latest stable", "https://www.boost.org/", "高质量 C++ 库集合，很多思想会进入标准库。", "算法/工具库"),
    ("ruby", "rails", "Rails", "latest supported series", "https://rubyonrails.org/", "约定优于配置，把 MVC、ORM、路由和任务系统整合成产品框架。", "资源控制器"),
    ("ruby", "sinatra", "Sinatra", "latest stable", "https://sinatrarb.com/", "极小 DSL，把 HTTP 路由直接映射到处理逻辑。", "微服务 API"),
    ("swift", "swiftui", "SwiftUI", "latest stable", "https://developer.apple.com/xcode/swiftui/", "声明式 UI，以状态变化驱动界面重绘。", "列表 UI"),
    ("swift", "vapor", "Vapor", "latest stable", "https://docs.vapor.codes/", "Swift 服务端框架，提供路由、异步、ORM 和部署模型。", "JSON API"),
    ("dart", "flutter", "Flutter", "3.44 stable", "https://docs.flutter.dev/release/archive", "用 Widget 树和响应式状态构建跨平台应用。", "计数器 UI"),
    ("dart", "shelf", "Shelf", "latest stable", "https://pub.dev/packages/shelf", "用 Handler 和 Middleware 组合 HTTP 服务。", "HTTP 服务"),
]


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def language_by_key(key: str) -> dict:
    return next(lang for lang in LANGUAGES if lang["key"] == key)


def example_source(lang: dict, topic: str) -> tuple[str, str]:
    key = lang["key"]
    ext = lang["extension"]
    if key == "java":
        if topic == "hello":
            return "Main.java", """
                public class Main {
                    public static void main(String[] args) {
                        String language = "Java 25";
                        System.out.println("Hello, " + language);
                    }
                }
            """
        if topic == "data-flow":
            return "Main.java", """
                import java.util.List;

                public class Main {
                    record Course(String name, int minutes) {}

                    public static void main(String[] args) {
                        var courses = List.of(new Course("records", 20), new Course("streams", 30));
                        int total = courses.stream().mapToInt(Course::minutes).sum();
                        System.out.println("total minutes = " + total);
                    }
                }
            """
        return "Main.java", """
            import java.io.IOException;

            public class Main {
                static String loadName(boolean ok) throws IOException {
                    if (!ok) throw new IOException("config missing");
                    return "learner";
                }

                public static void main(String[] args) {
                    try {
                        System.out.println(loadName(false));
                    } catch (IOException ex) {
                        System.out.println("recover: " + ex.getMessage());
                    }
                }
            }
        """
    if key == "javascript-typescript":
        if topic == "hello":
            return "main.mjs", """
                const language = "Node.js 24 LTS";
                console.log(`Hello, ${language}`);
            """
        if topic == "data-flow":
            return "main.mjs", """
                const courses = [
                  { name: "promises", minutes: 25 },
                  { name: "modules", minutes: 35 },
                ];

                const total = courses.reduce((sum, item) => sum + item.minutes, 0);
                console.log(`total minutes = ${total}`);
            """
        return "main.mjs", """
            async function loadName(ok) {
              if (!ok) throw new Error("config missing");
              return "learner";
            }

            try {
              console.log(await loadName(false));
            } catch (error) {
              console.log(`recover: ${error.message}`);
            }
        """
    if key == "python":
        if topic == "hello":
            return "main.py", """
                language = "Python 3.14"
                print(f"Hello, {language}")
            """
        if topic == "data-flow":
            return "main.py", """
                from dataclasses import dataclass

                @dataclass(frozen=True)
                class Course:
                    name: str
                    minutes: int

                courses = [Course("typing", 20), Course("asyncio", 30)]
                print(f"total minutes = {sum(course.minutes for course in courses)}")
            """
        return "main.py", """
            def load_name(ok: bool) -> str:
                if not ok:
                    raise FileNotFoundError("config missing")
                return "learner"

            try:
                print(load_name(False))
            except FileNotFoundError as exc:
                print(f"recover: {exc}")
        """
    if key == "go":
        if topic == "hello":
            return "main.go", """
                package main

                import "fmt"

                func main() {
                    fmt.Println("Hello, Go 1.26")
                }
            """
        if topic == "data-flow":
            return "main.go", """
                package main

                import "fmt"

                type Course struct {
                    Name    string
                    Minutes int
                }

                func main() {
                    courses := []Course{{"interfaces", 20}, {"goroutines", 30}}
                    total := 0
                    for _, course := range courses {
                        total += course.Minutes
                    }
                    fmt.Printf("total minutes = %d\\n", total)
                }
            """
        return "main.go", """
            package main

            import (
                "errors"
                "fmt"
            )

            func loadName(ok bool) (string, error) {
                if !ok {
                    return "", errors.New("config missing")
                }
                return "learner", nil
            }

            func main() {
                name, err := loadName(false)
                if err != nil {
                    fmt.Println("recover:", err)
                    return
                }
                fmt.Println(name)
            }
        """
    if key == "rust":
        if topic == "hello":
            return "main.rs", """
                fn main() {
                    println!("Hello, Rust stable");
                }
            """
        if topic == "data-flow":
            return "main.rs", """
                struct Course {
                    name: &'static str,
                    minutes: u32,
                }

                fn main() {
                    let courses = [Course { name: "ownership", minutes: 25 }, Course { name: "traits", minutes: 35 }];
                    let total: u32 = courses.iter().map(|course| course.minutes).sum();
                    println!("total minutes = {total}");
                }
            """
        return "main.rs", """
            fn load_name(ok: bool) -> Result<&'static str, &'static str> {
                if ok { Ok("learner") } else { Err("config missing") }
            }

            fn main() {
                match load_name(false) {
                    Ok(name) => println!("{name}"),
                    Err(error) => println!("recover: {error}"),
                }
            }
        """
    if key == "csharp-dotnet":
        if topic == "hello":
            return "Program.cs", """
                Console.WriteLine("Hello, .NET 10 LTS");
            """
        if topic == "data-flow":
            return "Program.cs", """
                var courses = new[] {
                    new Course("nullable", 20),
                    new Course("async", 30),
                };

                Console.WriteLine($"total minutes = {courses.Sum(course => course.Minutes)}");

                public record Course(string Name, int Minutes);
            """
        return "Program.cs", """
            static string LoadName(bool ok)
            {
                if (!ok) throw new InvalidOperationException("config missing");
                return "learner";
            }

            try
            {
                Console.WriteLine(LoadName(false));
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"recover: {ex.Message}");
            }
        """
    if key == "kotlin":
        if topic == "hello":
            return "main.kts", """
                val language = "Kotlin 2.3"
                println("Hello, $language")
            """
        if topic == "data-flow":
            return "main.kts", """
                data class Course(val name: String, val minutes: Int)

                val courses = listOf(Course("null safety", 20), Course("coroutines", 30))
                println("total minutes = ${courses.sumOf { it.minutes }}")
            """
        return "main.kts", """
            fun loadName(ok: Boolean): String {
                require(ok) { "config missing" }
                return "learner"
            }

            runCatching { loadName(false) }
                .onSuccess(::println)
                .onFailure { println("recover: ${it.message}") }
        """
    if key == "php":
        if topic == "hello":
            return "main.php", """
                <?php
                declare(strict_types=1);

                echo "Hello, PHP 8.5\\n";
            """
        if topic == "data-flow":
            return "main.php", """
                <?php
                declare(strict_types=1);

                $courses = [
                    ["name" => "types", "minutes" => 20],
                    ["name" => "fibers", "minutes" => 30],
                ];

                echo "total minutes = " . array_sum(array_column($courses, "minutes")) . PHP_EOL;
            """
        return "main.php", """
            <?php
            declare(strict_types=1);

            function loadName(bool $ok): string {
                if (!$ok) {
                    throw new RuntimeException("config missing");
                }
                return "learner";
            }

            try {
                echo loadName(false) . PHP_EOL;
            } catch (Throwable $error) {
                echo "recover: {$error->getMessage()}" . PHP_EOL;
            }
        """
    if key == "c-cpp":
        if topic == "hello":
            return "main.cpp", """
                #include <iostream>

                int main() {
                    std::cout << "Hello, C++23\\n";
                }
            """
        if topic == "data-flow":
            return "main.cpp", """
                #include <iostream>
                #include <numeric>
                #include <vector>

                struct Course {
                    const char* name;
                    int minutes;
                };

                int main() {
                    std::vector<Course> courses{{"raii", 20}, {"ranges", 30}};
                    int total = std::accumulate(courses.begin(), courses.end(), 0, [](int sum, const Course& course) {
                        return sum + course.minutes;
                    });
                    std::cout << "total minutes = " << total << "\\n";
                }
            """
        return "main.cpp", """
            #include <expected>
            #include <iostream>
            #include <string>

            std::expected<std::string, std::string> load_name(bool ok) {
                if (!ok) return std::unexpected("config missing");
                return "learner";
            }

            int main() {
                auto name = load_name(false);
                if (!name) {
                    std::cout << "recover: " << name.error() << "\\n";
                }
            }
        """
    if key == "ruby":
        if topic == "hello":
            return "main.rb", """
                language = "Ruby stable"
                puts "Hello, #{language}"
            """
        if topic == "data-flow":
            return "main.rb", """
                Course = Data.define(:name, :minutes)

                courses = [Course.new("blocks", 20), Course.new("fibers", 30)]
                puts "total minutes = #{courses.sum(&:minutes)}"
            """
        return "main.rb", """
            def load_name(ok)
              raise "config missing" unless ok
              "learner"
            end

            begin
              puts load_name(false)
            rescue StandardError => error
              puts "recover: #{error.message}"
            end
        """
    if key == "swift":
        if topic == "hello":
            return "main.swift", """
                let language = "Swift 6.3"
                print("Hello, \\(language)")
            """
        if topic == "data-flow":
            return "main.swift", """
                struct Course {
                    let name: String
                    let minutes: Int
                }

                let courses = [Course(name: "actors", minutes: 20), Course(name: "protocols", minutes: 30)]
                print("total minutes = \\(courses.map(\\.minutes).reduce(0, +))")
            """
        return "main.swift", """
            enum ConfigError: Error {
                case missing
            }

            func loadName(_ ok: Bool) throws -> String {
                if !ok { throw ConfigError.missing }
                return "learner"
            }

            do {
                print(try loadName(false))
            } catch {
                print("recover: \\(error)")
            }
        """
    if key == "dart":
        if topic == "hello":
            return "main.dart", """
                void main() {
                  const language = 'Dart 3.12';
                  print('Hello, $language');
                }
            """
        if topic == "data-flow":
            return "main.dart", """
                class Course {
                  const Course(this.name, this.minutes);

                  final String name;
                  final int minutes;
                }

                void main() {
                  const courses = [Course('null safety', 20), Course('streams', 30)];
                  final total = courses.map((course) => course.minutes).reduce((a, b) => a + b);
                  print('total minutes = $total');
                }
            """
        return "main.dart", """
            String loadName(bool ok) {
              if (!ok) {
                throw StateError('config missing');
              }
              return 'learner';
            }

            void main() {
              try {
                print(loadName(false));
              } on StateError catch (error) {
                print('recover: ${error.message}');
              }
            }
        """
    raise ValueError(key)


def run_command(lang: dict, source_file: str) -> str:
    key = lang["key"]
    if key == "java":
        return f"javac {source_file} && java Main"
    if key == "javascript-typescript":
        return f"node {source_file}"
    if key == "python":
        return f"python3 {source_file}"
    if key == "go":
        return f"go run {source_file}"
    if key == "rust":
        return f"rustc {source_file} -o /tmp/{lang['key']}-example && /tmp/{lang['key']}-example"
    if key == "csharp-dotnet":
        return "dotnet new console --force && dotnet run"
    if key == "kotlin":
        return f"kotlin {source_file}"
    if key == "php":
        return f"php {source_file}"
    if key == "c-cpp":
        return f"c++ -std=c++23 {source_file} -o /tmp/cpp-example && /tmp/cpp-example"
    if key == "ruby":
        return f"ruby {source_file}"
    if key == "swift":
        return f"swift {source_file}"
    if key == "dart":
        return f"dart run {source_file}"
    return f"run {source_file}"


def write_root_files() -> None:
    language_rows = "\n        ".join(
        f"| [{lang['name']}](languages/{lang['key']}/) | {lang['version']} | {lang['policy']} | {lang['scenario']} |"
        for lang in LANGUAGES
    )
    framework_rows = "\n        ".join(
        f"| [{name}](frameworks/{language_key}/{framework_key}/) | {language_by_key(language_key)['name']} | {version} | {case} |"
        for language_key, framework_key, name, version, _source, _idea, case in FRAMEWORKS
    )
    write("README.md", f"""
        # 主流编程语言与框架学习仓库

        这个仓库用于系统学习主流编程语言及其代表性框架。第一版采用中文文档、统一章节模板和最小可运行案例，目标是让学习者能横向比较语言特性，也能纵向进入框架工程实践。

        ## 版本策略

        - 有官方 LTS 或 Active LTS 的生态，优先使用当前最新 LTS。
        - 没有官方 LTS 概念的生态，使用官方最新 stable 或受支持分支，并在 [`versions.yaml`](versions.yaml) 标注为 `latest-stable-no-lts` 或 `latest-supported-stable`。
        - 本仓库的版本基线最后校验日期为 {CHECKED_DATE}。实际安装时请以各官方页面和包管理器解析结果为准。

        ## 学习路线

        1. 先阅读一门语言的 `languages/<language>/README.md`，理解类型系统、错误处理、并发模型和工程化方式。
        2. 运行该语言的 3 个基础案例：`hello`、`data-flow`、`errors`。
        3. 再进入 `frameworks/<language>/<framework>/README.md`，学习框架核心思想和最小项目结构。
        4. 横向比较不同语言在同一类问题上的表达方式，例如数据建模、错误恢复、HTTP API。

        ## 语言目录

        | 语言 | 版本基线 | 策略 | 典型场景 |
        | --- | --- | --- | --- |
        {language_rows}

        ## 框架目录

        | 框架 | 语言 | 版本基线 | 第一案例 |
        | --- | --- | --- | --- |
        {framework_rows}

        ## 验证

        ```bash
        python3 scripts/verify_versions.py
        python3 scripts/run_smoke_tests.py --dry-run
        ```

        `run_smoke_tests.py` 默认只检查案例结构和运行命令；加上 `--execute` 后会尝试运行本机已经安装的语言工具链案例。
    """)
    yaml_languages = []
    for lang in LANGUAGES:
        is_lts = lang["policy"] in {"latest-lts", "latest-active-lts"}
        yaml_languages.append(
            f"""  - id: {lang['key']}
    name: "{lang['name']}"
    version: "{lang['version']}"
    runtime: "{lang['runtime']}"
    policy: "{lang['policy']}"
    lts: {str(is_lts).lower()}
    official_source: "{lang['source']}"
    checked_at: "{CHECKED_DATE}\""""
        )
    yaml_frameworks = []
    for language_key, framework_key, name, version, source, _idea, _case in FRAMEWORKS:
        is_lts = "LTS" in version or "Active LTS" in version
        yaml_frameworks.append(
            f"""  - id: {framework_key}
    language: {language_key}
    name: "{name}"
    version: "{version}"
    policy: "{'latest-lts' if is_lts else 'latest-stable-or-supported'}"
    lts: {str(is_lts).lower()}
    official_source: "{source}"
    checked_at: "{CHECKED_DATE}\""""
        )
    versions_yaml = "\n".join(
        [
            "meta:",
            f'  checked_at: "{CHECKED_DATE}"',
            '  rule: "Use latest LTS/Active LTS when officially defined; otherwise use latest official stable or supported branch and mark it explicitly."',
            '  note: "Patch versions for framework latest-stable entries should be refreshed with package managers before production use."',
            "languages:",
            "\n".join(yaml_languages),
            "frameworks:",
            "\n".join(yaml_frameworks),
        ]
    )
    write("versions.yaml", versions_yaml)
    write(".gitignore", """
        .DS_Store
        __pycache__/
        *.pyc
        node_modules/
        target/
        bin/
        obj/
        build/
        dist/
        .dart_tool/
        .gradle/
        vendor/
    """)
    write("docs/templates/language.md", """
        # <Language>

        ## 语言定位
        ## 适合场景
        ## 核心语法
        ## 类型/内存/并发模型
        ## 标准库与包管理
        ## 错误处理
        ## 工程化
        ## 常见坑
        ## 案例索引
    """)
    write("docs/templates/framework.md", """
        # <Framework>

        ## 核心思想
        ## 架构模型
        ## 请求/执行生命周期
        ## 配置方式
        ## 依赖注入或模块机制
        ## 数据访问
        ## 测试方式
        ## 部署方式
        ## 案例索引
    """)


def write_language_files() -> None:
    for lang in LANGUAGES:
        example_links = "\n            ".join(
            f"- [{topic}](examples/{topic}/)：{desc}"
            for topic, desc in [
                ("hello", "最小程序与运行方式"),
                ("data-flow", "数据建模、集合处理和函数组合"),
                ("errors", "错误建模、恢复和资源边界"),
            ]
        )
        write(f"languages/{lang['key']}/README.md", f"""
            # {lang['name']}

            ## 语言定位

            {lang['name']} 的第一版学习基线是 **{lang['version']}**，工具链入口是 **{lang['runtime']}**。它主要用于：{lang['scenario']}。

            ## 适合场景

            - 需要理解该生态的工程化默认选择，例如包管理、构建、测试和发布。
            - 需要横向比较不同语言在类型、并发和错误处理上的设计取舍。
            - 需要从小案例过渡到代表性框架，而不是只背语法。

            ## 核心语法

            重点学习变量/常量、函数、模块、数据结构、泛型或类型标注、控制流，以及该语言最常见的代码组织方式。案例会尽量保持短小，让语法特征直接暴露出来。

            ## 类型/内存/并发模型

            - 类型模型：{lang['typing']}。
            - 并发模型：{lang['concurrency']}。
            - 内存与资源：结合语言自己的生命周期管理方式学习，不把所有语言都套成同一种范式。

            ## 标准库与包管理

            包管理入口：{lang['package']}。第一版案例优先使用标准库，只有框架章节才引入生态依赖。

            ## 错误处理

            {lang['error']}。学习时关注错误如何被表达、传播、恢复，以及如何避免把异常路径藏在业务逻辑里。

            ## 工程化

            第一阶段关注代码格式、测试入口、依赖声明和可重复运行。大型工程主题，如性能分析、发布、观测和安全，会在框架章节逐步展开。

            ## 常见坑

            - 只学习语法而忽略包管理和项目结构。
            - 把其他语言的范式硬搬过来，错过本语言的惯用表达。
            - 示例能跑但没有预期输出，导致无法判断自己是否真正理解。

            ## 案例索引

            {example_links}

            ## 版本来源

            - 策略：`{lang['policy']}`
            - 官方来源：{lang['source']}
            - 校验日期：{CHECKED_DATE}
        """)
        for topic in ["hello", "data-flow", "errors"]:
            source_file, source = example_source(lang, topic)
            command = run_command(lang, source_file)
            write(f"languages/{lang['key']}/examples/{topic}/{source_file}", source)
            write(f"languages/{lang['key']}/examples/{topic}/README.md", f"""
                # {lang['name']} / {topic}

                ## 目标

                通过一个最小案例观察 {lang['name']} 在 `{topic}` 场景下的惯用写法。

                ## 运行

                ```bash
                {command}
                ```

                ## 预期输出

                输出应包含 `Hello`、`total minutes` 或 `recover` 之一，分别对应最小程序、数据流和错误恢复案例。

                ## 观察点

                - 源文件：`{source_file}`
                - 版本基线：{lang['version']}
                - 包管理：{lang['package']}
            """)


def write_framework_files() -> None:
    for language_key, framework_key, name, version, source, idea, case in FRAMEWORKS:
        lang = language_by_key(language_key)
        write(f"frameworks/{language_key}/{framework_key}/README.md", f"""
            # {name}

            ## 核心思想

            {idea}

            ## 架构模型

            - 语言生态：{lang['name']} / {lang['version']}
            - 框架版本基线：{version}
            - 第一案例：{case}
            - 工程边界：把路由/入口、业务逻辑、配置和测试分开，避免所有代码堆在启动文件中。

            ## 请求/执行生命周期

            学习顺序建议从入口开始：请求或事件进入框架，经过路由/组件树/构建目标，再进入业务处理，最后由响应、渲染或构建产物离开框架。

            ## 配置方式

            第一版只保留最小配置：运行时版本、依赖声明、启动命令和测试命令。更复杂的环境变量、配置中心、构建 profile 后续按案例补充。

            ## 依赖注入或模块机制

            重点观察框架如何管理组件生命周期：是显式传参、容器注入、插件注册、模块导入，还是编译期组合。

            ## 数据访问

            第一案例默认使用内存数据结构，避免数据库配置掩盖框架核心思想。数据库、迁移和事务会作为第二阶段案例加入。

            ## 测试方式

            每个框架至少保留一个可自动化验证的入口：单元测试、HTTP smoke test、构建命令或页面渲染检查。

            ## 部署方式

            第一版记录本地运行命令；后续扩展 Dockerfile、CI 和云平台部署。

            ## 案例索引

            - [quickstart](examples/quickstart/)：{case} 的最小工程骨架。

            ## 版本来源

            - 官方来源：{source}
            - 校验日期：{CHECKED_DATE}
        """)
        write(f"frameworks/{language_key}/{framework_key}/examples/quickstart/README.md", f"""
            # {name} quickstart

            ## 目标

            用最小文件展示 {name} 的核心结构：入口、路由或组件、业务处理和运行命令。

            ## 运行策略

            该目录是教学骨架。首次真正运行前，应按 `{ROOT.name}/versions.yaml` 中的版本策略锁定依赖 patch 版本，并用框架官方脚手架或包管理器生成 lockfile。

            ## 建议命令

            ```bash
            # 以官方文档为准安装依赖后运行
            # source: {source}
            ```

            ## 验收

            - 能说明 {name} 的核心思想。
            - 能指出入口文件、配置文件和业务处理位置。
            - 能把内存数据案例替换为真实数据访问案例。
        """)
        write(f"frameworks/{language_key}/{framework_key}/examples/quickstart/NOTES.md", f"""
            # {name} 设计笔记

            - 版本基线：{version}
            - 语言基线：{lang['name']} {lang['version']}
            - 核心案例：{case}
            - 下一步：补充依赖清单、测试命令和一个可运行端到端案例。
        """)


def write_scripts() -> None:
    write("scripts/verify_versions.py", r'''
        from __future__ import annotations

        import re
        from pathlib import Path

        ROOT = Path(__file__).resolve().parents[1]
        REQUIRED_FIELDS = ["id:", "name:", "version:", "policy:", "official_source:", "checked_at:"]
        EXPECTED_LANGUAGES = 12
        EXPECTED_FRAMEWORKS = 23


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
    ''')
    write("scripts/run_smoke_tests.py", r'''
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
    ''')


def main() -> None:
    write_root_files()
    write_language_files()
    write_framework_files()
    write_scripts()


if __name__ == "__main__":
    main()
