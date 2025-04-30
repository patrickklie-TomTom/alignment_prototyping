#pragma once
#include <Eigen/Dense>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

inline std::vector<Eigen::Vector3d> load_pcd(const std::string& filename) {
    std::ifstream file(filename);
    std::string line;
    std::vector<Eigen::Vector3d> points;
    bool data_section = false;
    while (std::getline(file, line)) {
        if (line == "DATA ascii") {
            data_section = true;
            continue;
        }
        if (!data_section) continue;
        std::istringstream iss(line);
        double x, y, z;
        if (iss >> x >> y >> z) {
            points.emplace_back(x, y, z);
        }
    }
    return points;
}

inline void save_pcd(const std::string& filename, const std::vector<Eigen::Vector3d>& points) {
    std::ofstream file(filename);
    file << "# .PCD v0.7 - Point Cloud Data file format\n"
         << "FIELDS x y z\n"
         << "SIZE 4 4 4\n"
         << "TYPE F F F\n"
         << "COUNT 1 1 1\n"
         << "WIDTH " << points.size() << "\n"
         << "HEIGHT 1\n"
         << "VIEWPOINT 0 0 0 1 0 0 0\n"
         << "POINTS " << points.size() << "\n"
         << "DATA ascii\n";
    for (const auto& p : points) {
        file << p.x() << " " << p.y() << " " << p.z() << "\n";
    }
}
