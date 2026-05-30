#include <iostream>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

#ifndef CMAKE_QUICKSTART_VERSION
#define CMAKE_QUICKSTART_VERSION "dev"
#endif

struct Task {
    std::string_view name;
    std::string_view status;
};

int main() {
    const std::vector<Task> tasks{
        {"configure", "done"},
        {"generate", "done"},
        {"build", "ready"},
    };

    std::cout << "CMake target model demo\n";
    std::cout << "project version: " << CMAKE_QUICKSTART_VERSION << '\n';
    std::cout << "C++ standard: " << __cplusplus << '\n';
    std::cout << "tasks:\n";

    for (const Task& task : tasks) {
        std::cout << "- " << task.name << ": " << task.status << '\n';
    }

    return 0;
}
