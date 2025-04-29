#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: standalone_aligner input.pcd output.pcd" << std::endl;
        return 1;
    }

    std::ifstream src(argv[1], std::ios::binary);
    std::ofstream dst(argv[2], std::ios::binary);
    dst << src.rdbuf();
    std::cout << "Standalone aligner (simulated): copied input to output." << std::endl;
    return 0;
}
