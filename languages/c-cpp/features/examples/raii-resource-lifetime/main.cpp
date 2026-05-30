#include <iostream>
#include <string>
#include <utility>

class ScopedHandle {
public:
    explicit ScopedHandle(std::string name) : name_(std::move(name)), open_(true) {
        std::cout << "open  " << name_ << '\n';
    }

    ScopedHandle(const ScopedHandle&) = delete;
    ScopedHandle& operator=(const ScopedHandle&) = delete;

    ScopedHandle(ScopedHandle&& other) noexcept
        : name_(std::move(other.name_)), open_(std::exchange(other.open_, false)) {
        std::cout << "move  " << name_ << '\n';
    }

    ScopedHandle& operator=(ScopedHandle&& other) noexcept {
        if (this != &other) {
            close();
            name_ = std::move(other.name_);
            open_ = std::exchange(other.open_, false);
            std::cout << "move= " << name_ << '\n';
        }
        return *this;
    }

    ~ScopedHandle() {
        close();
    }

    void write(std::string_view message) const {
        if (open_) {
            std::cout << "write " << name_ << ": " << message << '\n';
        }
    }

private:
    void close() {
        if (open_) {
            std::cout << "close " << name_ << '\n';
            open_ = false;
        }
    }

    std::string name_;
    bool open_ = false;
};

bool send_report(bool network_ok) {
    ScopedHandle file{"report.txt"};
    ScopedHandle socket{"telemetry-socket"};

    file.write("prepare payload");
    if (!network_ok) {
        std::cout << "network failed, leave scope early\n";
        return false;
    }

    socket.write("payload delivered");
    return true;
}

int main() {
    std::cout << "success path\n";
    send_report(true);

    std::cout << "\nfailure path\n";
    send_report(false);
}
