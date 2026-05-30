#include <iostream>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace demo {

struct RawTask {
    std::string title;
    std::optional<int> priority;
};

struct Task {
    std::string title;
    int priority;
    bool done;
};

class ScopeLog {
public:
    explicit ScopeLog(std::string label) : label_(std::move(label)) {
        std::cout << "begin " << label_ << '\n';
    }

    ~ScopeLog() {
        std::cout << "end " << label_ << '\n';
    }

private:
    std::string label_;
};

std::optional<int> parse_priority(const std::optional<int>& raw_priority) {
    if (!raw_priority.has_value()) {
        return std::nullopt;
    }

    if (*raw_priority < 0) {
        throw std::runtime_error("priority must not be negative");
    }

    return *raw_priority;
}

Task make_task(const RawTask& raw_task, int fallback_priority) {
    auto priority = parse_priority(raw_task.priority).value_or(fallback_priority);
    return Task{raw_task.title, priority, false};
}

std::string bucket_for(const Task& task) {
    switch (task.priority) {
        case 1:
            return "low";
        case 2:
        case 3:
            return "normal";
        default:
            return "urgent";
    }
}

std::string describe(const Task& task) {
    std::string status = task.done ? "done" : "open";
    return task.title + " [" + bucket_for(task) + ", " + status + "]";
}

class TaskBoard {
public:
    void add(Task task) {
        tasks_.push_back(std::move(task));
    }

    void complete_first() {
        if (!tasks_.empty()) {
            tasks_[0].done = true;
        }
    }

    std::map<std::string, int> count_by_bucket() const {
        std::map<std::string, int> counts;
        for (const auto& task : tasks_) {
            counts[bucket_for(task)] += 1;
        }
        return counts;
    }

    const Task* top_priority() const {
        if (tasks_.empty()) {
            return nullptr;
        }

        const Task* best = &tasks_[0];
        for (const auto& task : tasks_) {
            if (task.priority > best->priority) {
                best = &task;
            }
        }
        return best;
    }

    const std::vector<Task>& tasks() const {
        return tasks_;
    }

private:
    std::vector<Task> tasks_;
};

}  // namespace demo

int main() {
    demo::ScopeLog log("syntax tour");

    const int fallback_priority = 2;
    const std::vector<demo::RawTask> raw_tasks{
        {"read C++ syntax guide", 3},
        {"compare C strings and std::string", std::nullopt},
        {"run the example", 5},
    };

    demo::TaskBoard board;
    int skipped = 0;

    for (std::size_t index = 0; index < raw_tasks.size(); ++index) {
        try {
            auto task = demo::make_task(raw_tasks[index], fallback_priority);
            board.add(std::move(task));
        } catch (const std::exception& error) {
            ++skipped;
            std::cout << "skip task #" << index << ": " << error.what() << '\n';
        }
    }

    board.complete_first();

    std::cout << "tasks:\n";
    for (const auto& task : board.tasks()) {
        std::cout << " - " << demo::describe(task) << '\n';
    }

    std::cout << "bucket counts:\n";
    for (const auto& [bucket, count] : board.count_by_bucket()) {
        std::cout << " - " << bucket << ": " << count << '\n';
    }

    if (const demo::Task* top = board.top_priority(); top != nullptr) {
        std::cout << "top priority: " << top->title << " (" << top->priority << ")\n";
    }

    std::cout << "skipped: " << skipped << '\n';
    return 0;
}
