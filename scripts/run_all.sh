#!/bin/bash
set -e

echo "[1/5] Build C++ & Pybind modules"
cd ../cpp
mkdir -p build && cd build
conan install .. --build=missing
cmake ..
cmake --build .

echo "[2/5] Generate synthetic point clouds"
cd ../../scripts
python3 generate_sample_pointcloud.py

echo "[3/5] Run Open3D ICP"
cd ../python/alignment_pure
python3 alignment_open3d.py

echo "[4/5] Run C++ CLI aligner"
cd ../../cpp/build/tools
./standalone_aligner ../../../data/sample/scan_source.pcd ../../../data/sample/scan_target.pcd ../../../data/sample/aligned_cli_output.pcd

echo "[5/5] Done."
