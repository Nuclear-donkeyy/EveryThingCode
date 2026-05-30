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
    std::cout << "total minutes = " << total << "\n";
}
