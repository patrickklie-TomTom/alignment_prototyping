#include <Eigen/Dense>
#include <vector>
#include <iostream>
#include "../utils/pcd_io.hpp"

void align_pointclouds(const std::string& file1, const std::string& file2, const std::string& output) {
    auto source = load_pcd(file1);
    auto target = load_pcd(file2);
    if (source.size() != target.size()) {
        std::cerr << "Point clouds must have the same number of points.\n";
        return;
    }

    Eigen::Vector3d centroid_src = Eigen::Vector3d::Zero();
    Eigen::Vector3d centroid_tgt = Eigen::Vector3d::Zero();
    for (size_t i = 0; i < source.size(); ++i) {
        centroid_src += source[i];
        centroid_tgt += target[i];
    }
    centroid_src /= source.size();
    centroid_tgt /= target.size();

    std::vector<Eigen::Vector3d> src_centered, tgt_centered;
    for (size_t i = 0; i < source.size(); ++i) {
        src_centered.push_back(source[i] - centroid_src);
        tgt_centered.push_back(target[i] - centroid_tgt);
    }

    Eigen::Matrix3d H = Eigen::Matrix3d::Zero();
    for (size_t i = 0; i < src_centered.size(); ++i) {
        H += src_centered[i] * tgt_centered[i].transpose();
    }

    Eigen::JacobiSVD<Eigen::Matrix3d> svd(H, Eigen::ComputeFullU | Eigen::ComputeFullV);
    Eigen::Matrix3d R = svd.matrixV() * svd.matrixU().transpose();

    if (R.determinant() < 0) {
        Eigen::Matrix3d V = svd.matrixV();
        V.col(2) *= -1;
        R = V * svd.matrixU().transpose();
    }

    Eigen::Vector3d t = centroid_tgt - R * centroid_src;

    std::vector<Eigen::Vector3d> aligned;
    for (const auto& pt : source) {
        aligned.push_back(R * pt + t);
    }

    save_pcd(output, aligned);

    std::cout << "Alignment complete. Output written to " << output << "\n";
}
