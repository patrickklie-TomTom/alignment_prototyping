#include <iostream>
void align_pointclouds(const std::string&, const std::string&, const std::string&); // forward decl

int main(int argc, char** argv) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " source.pcd target.pcd output.pcd\n";
        return 1;
    }
    align_pointclouds(argv[1], argv[2], argv[3]);
    return 0;
}
