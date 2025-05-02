import open3d as o3d
import numpy as np
import importlib

def load_pcd(path):
    pc = o3d.io.read_point_cloud(path)
    return np.asarray(pc.points)

def test_estimate_transform():
    mod = importlib.import_module("aligner_bindings")
    src = load_pcd("data/sample/scan_source.pcd")
    tgt = load_pcd("data/sample/scan_target.pcd")
    transform = mod.estimate_transform(src.tolist(), tgt.tolist())
    print("Method-level transform:\n", transform)

def test_class_aligner():
    mod = importlib.import_module("aligner_class_bindings")
    src = load_pcd("data/sample/scan_source.pcd")
    tgt = load_pcd("data/sample/scan_target.pcd")
    aligner = mod.Aligner()
    transform = aligner.align(src.tolist(), tgt.tolist())
    print("Class-level transform:\n", transform)

def test_framework_pipeline():
    mod = importlib.import_module("aligner_pipeline")
    mod.align_pointcloud_files("data/sample/scan_source.pcd", "data/sample/scan_target.pcd", "data/sample/aligned_pipeline_output.pcd")
    print("Framework-level alignment written to aligned_pipeline_output.pcd")

if __name__ == "__main__":
    test_estimate_transform()
    test_class_aligner()
    test_framework_pipeline()
