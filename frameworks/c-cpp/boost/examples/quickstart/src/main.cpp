#include <boost/algorithm/string.hpp>
#include <boost/container/small_vector.hpp>
#include <boost/lexical_cast.hpp>

#include <iostream>
#include <numeric>
#include <string>
#include <vector>

int main() {
    const std::string input = " 42, 7, invalid, 13 ";
    std::vector<std::string> tokens;
    boost::split(tokens, input, boost::is_any_of(","), boost::token_compress_on);

    boost::container::small_vector<int, 4> values;

    for (std::string token : tokens) {
        boost::algorithm::trim(token);
        try {
            values.push_back(boost::lexical_cast<int>(token));
        } catch (const boost::bad_lexical_cast&) {
            std::cout << "skip non-integer token: " << token << '\n';
        }
    }

    const int sum = std::accumulate(values.begin(), values.end(), 0);
    const double average = values.empty()
        ? 0.0
        : static_cast<double>(sum) / static_cast<double>(values.size());

    std::cout << "Boost utility demo\n";
    std::cout << "values:";
    for (int value : values) {
        std::cout << ' ' << value;
    }
    std::cout << "\nsum: " << sum << '\n';
    std::cout << "average: " << average << '\n';

    return 0;
}
