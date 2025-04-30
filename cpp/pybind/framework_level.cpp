#include <pybind11/pybind11.h>
#include <string>
#include "../utils/pcd_io.hpp"
#include "../src/align_gtsam.cpp"

namespace py = pybind11;

void align_pointcloud_files(const std::string& file1, const std::string& file2, const std::string& out_file) {
    align_pointclouds(file1, file2, out_file);
}

PYBIND11_MODULE(aligner_pipeline, m) {
    m.def("align_pointcloud_files", &align_pointcloud_files);
}
