#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <Eigen/Dense>
#include <vector>

namespace py = pybind11;

class Aligner {
public:
    Eigen::Matrix4d align(const std::vector<Eigen::Vector3d>& src, const std::vector<Eigen::Vector3d>& tgt) {
        Eigen::Vector3d centroid_src = Eigen::Vector3d::Zero();
        Eigen::Vector3d centroid_tgt = Eigen::Vector3d::Zero();
        for (size_t i = 0; i < src.size(); ++i) {
            centroid_src += src[i];
            centroid_tgt += tgt[i];
        }
        centroid_src /= src.size();
        centroid_tgt /= tgt.size();

        Eigen::Matrix3d H = Eigen::Matrix3d::Zero();
        for (size_t i = 0; i < src.size(); ++i) {
            H += (src[i] - centroid_src) * (tgt[i] - centroid_tgt).transpose();
        }

        Eigen::JacobiSVD<Eigen::Matrix3d> svd(H, Eigen::ComputeFullU | Eigen::ComputeFullV);
        Eigen::Matrix3d R = svd.matrixV() * svd.matrixU().transpose();

        if (R.determinant() < 0) {
            Eigen::Matrix3d V = svd.matrixV();
            V.col(2) *= -1;
            R = V * svd.matrixU().transpose();
        }

        Eigen::Vector3d t = centroid_tgt - R * centroid_src;

        Eigen::Matrix4d T = Eigen::Matrix4d::Identity();
        T.block<3,3>(0,0) = R;
        T.block<3,1>(0,3) = t;

        return T;
    }
};

PYBIND11_MODULE(aligner_class_bindings, m) {
    py::class_<Aligner>(m, "Aligner")
        .def(py::init<>())
        .def("align", &Aligner::align);
}
