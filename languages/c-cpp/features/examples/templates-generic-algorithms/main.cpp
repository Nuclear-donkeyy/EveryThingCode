#include <array>
#include <concepts>
#include <iostream>
#include <string>
#include <vector>

struct Reading {
    std::string sensor;
    double value;
};

template <typename Iterator, typename Project>
requires requires(Iterator it, Project project) {
    { project(*it) } -> std::convertible_to<double>;
}
double summarize(Iterator first, Iterator last, Project project) {
    double total = 0.0;
    int count = 0;

    for (auto it = first; it != last; ++it) {
        total += project(*it);
        ++count;
    }

    return count == 0 ? 0.0 : total / count;
}

int main() {
    std::vector<Reading> temperatures{
        {"north", 21.5},
        {"south", 24.0},
        {"west", 20.0},
    };

    std::array<int, 4> scores{80, 95, 90, 85};

    const double average_temperature = summarize(
        temperatures.begin(),
        temperatures.end(),
        [](const Reading& reading) { return reading.value; });

    const double average_score = summarize(
        scores.begin(),
        scores.end(),
        [](int score) { return score; });

    std::cout << "average temperature: " << average_temperature << '\n';
    std::cout << "average score: " << average_score << '\n';
}
