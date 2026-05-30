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
        std::cout << "recover: " << name.error() << "\n";
    }
}
