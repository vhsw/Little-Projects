#include <vector>
#include <string>
#include <cmath>
#include <iostream>

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        std::cerr << "Usage: " << argv[0] << " maxN" << std::endl;
        return 1;
    }
    auto n = std::stoul(argv[1]);

    std::vector<unsigned long> arr;
    arr.resize(n + 1);
    auto upper_lim = static_cast<unsigned long>(std::sqrt(n)) + 1;
    for (unsigned long k1 = 1; k1 < upper_lim; ++k1)
    {
        for (auto k2 = k1; k2 < (n / k1 + 1); ++k2)
        {
            auto val = k1 != k2 ? k1 + k2 : k1;
            arr[k1 * k2] += val;
        }
    }

    std::cout << arr.back() << std::endl;
}
