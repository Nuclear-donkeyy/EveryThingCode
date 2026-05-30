#include <cstddef>
#include <cstdint>
#include <iostream>
#include <span>
#include <vector>

struct PacketHeader {
    std::uint16_t type;
    std::uint32_t length;
    std::uint8_t flags;
};

struct PackedLikeHeader {
    std::uint32_t length;
    std::uint16_t type;
    std::uint8_t flags;
};

int main() {
    std::cout << "PacketHeader size=" << sizeof(PacketHeader)
              << " align=" << alignof(PacketHeader) << '\n';
    std::cout << "  type offset=" << offsetof(PacketHeader, type) << '\n';
    std::cout << "  length offset=" << offsetof(PacketHeader, length) << '\n';
    std::cout << "  flags offset=" << offsetof(PacketHeader, flags) << '\n';

    std::cout << "PackedLikeHeader size=" << sizeof(PackedLikeHeader)
              << " align=" << alignof(PackedLikeHeader) << '\n';
    std::cout << "  length offset=" << offsetof(PackedLikeHeader, length) << '\n';
    std::cout << "  type offset=" << offsetof(PackedLikeHeader, type) << '\n';
    std::cout << "  flags offset=" << offsetof(PackedLikeHeader, flags) << '\n';

    std::vector<PackedLikeHeader> packets{
        {128, 1, 0b001},
        {256, 2, 0b010},
        {512, 3, 0b100},
    };

    std::span<PackedLikeHeader> view{packets};
    std::cout << "contiguous lengths:";
    for (const auto& packet : view) {
        std::cout << ' ' << packet.length;
    }
    std::cout << '\n';
}
