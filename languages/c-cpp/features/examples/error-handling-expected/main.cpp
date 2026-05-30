#include <expected>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

enum class ParseError {
    empty,
    invalid_digit,
    out_of_range,
};

std::string describe(ParseError error) {
    switch (error) {
    case ParseError::empty:
        return "empty input";
    case ParseError::invalid_digit:
        return "invalid digit";
    case ParseError::out_of_range:
        return "value out of range";
    }
    return "unknown error";
}

std::expected<int, ParseError> parse_port(std::string_view text) {
    if (text.empty()) {
        return std::unexpected(ParseError::empty);
    }

    int value = 0;
    for (char ch : text) {
        if (ch < '0' || ch > '9') {
            return std::unexpected(ParseError::invalid_digit);
        }

        value = value * 10 + (ch - '0');
        if (value > 65535) {
            return std::unexpected(ParseError::out_of_range);
        }
    }

    return value;
}

int main() {
    const std::vector<std::string_view> inputs{"443", "", "80x", "70000"};

    for (std::string_view input : inputs) {
        std::cout << "parse '" << input << "': ";
        if (auto port = parse_port(input)) {
            std::cout << "ok port=" << *port << '\n';
        } else {
            std::cout << "error " << describe(port.error()) << '\n';
        }
    }
}
