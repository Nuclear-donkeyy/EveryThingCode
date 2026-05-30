#include <algorithm>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

struct Task {
    std::string title;
    int priority;
    bool done;
};

int main() {
    std::vector<Task> tasks{
        {"write tests", 3, false},
        {"ship patch", 5, false},
        {"archive notes", 1, true},
        {"review api", 4, false},
    };

    auto active_titles = tasks
        | std::views::filter([](const Task& task) { return !task.done; })
        | std::views::transform([](const Task& task) { return task.title; });

    std::cout << "active titles:";
    for (const auto& title : active_titles) {
        std::cout << ' ' << title;
    }
    std::cout << '\n';

    std::ranges::sort(tasks, std::greater<>{}, &Task::priority);

    std::cout << "by priority:";
    for (const auto& task : tasks) {
        std::cout << ' ' << task.title << '(' << task.priority << ')';
    }
    std::cout << '\n';

    const auto urgent = std::ranges::find_if(tasks, [](const Task& task) {
        return !task.done && task.priority >= 4;
    });

    if (urgent != tasks.end()) {
        std::cout << "next urgent: " << urgent->title << '\n';
    }
}
