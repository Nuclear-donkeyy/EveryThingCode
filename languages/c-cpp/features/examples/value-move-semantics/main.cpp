#include <iostream>
#include <numeric>
#include <string>
#include <utility>
#include <vector>

class Buffer {
public:
    Buffer(std::string name, std::vector<int> values)
        : name_(std::move(name)), values_(std::move(values)) {
        std::cout << "construct " << name_ << '\n';
    }

    Buffer(const Buffer& other) : name_(other.name_ + " copy"), values_(other.values_) {
        std::cout << "copy      " << other.name_ << " -> " << name_ << '\n';
    }

    Buffer& operator=(const Buffer& other) {
        name_ = other.name_ + " copy";
        values_ = other.values_;
        std::cout << "copy=     " << other.name_ << " -> " << name_ << '\n';
        return *this;
    }

    Buffer(Buffer&& other) noexcept
        : name_(std::move(other.name_)), values_(std::move(other.values_)) {
        std::cout << "move      " << name_ << '\n';
    }

    Buffer& operator=(Buffer&& other) noexcept {
        name_ = std::move(other.name_);
        values_ = std::move(other.values_);
        std::cout << "move=     " << name_ << '\n';
        return *this;
    }

    int sum() const {
        return std::accumulate(values_.begin(), values_.end(), 0);
    }

    const std::string& name() const {
        return name_;
    }

private:
    std::string name_;
    std::vector<int> values_;
};

Buffer make_buffer() {
    Buffer local{"sensor-window", {3, 5, 8}};
    return local;
}

void inspect_by_value(Buffer buffer) {
    std::cout << "inspect   " << buffer.name() << " sum=" << buffer.sum() << '\n';
}

int main() {
    std::cout << "return a value\n";
    Buffer original = make_buffer();

    std::cout << "\ncopy into a function parameter\n";
    inspect_by_value(original);
    std::cout << "original  " << original.name() << " sum=" << original.sum() << '\n';

    std::cout << "\nmove into a vector\n";
    std::vector<Buffer> buffers;
    buffers.reserve(2);
    buffers.push_back(std::move(original));
    buffers.emplace_back("batch", std::vector<int>{10, 20});

    for (const auto& buffer : buffers) {
        std::cout << "stored    " << buffer.name() << " sum=" << buffer.sum() << '\n';
    }
}
