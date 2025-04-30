import open3d as o3d
import numpy as np

def align_pcd_files(source_path, target_path, output_path):
    source = o3d.io.read_point_cloud(source_path)
    target = o3d.io.read_point_cloud(target_path)

    threshold = 1.5
    trans_init = np.eye(4)

    print("Running ICP...")
    reg = o3d.pipelines.registration.registration_icp(
        source, target, threshold, trans_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )

    print("Estimated transformation:\n", reg.transformation)

    source.transform(reg.transformation)
    o3d.io.write_point_cloud(output_path, source)
    print(f"Aligned point cloud written to {output_path}")

if __name__ == "__main__":
    align_pcd_files("data/sample/scan_source.pcd", "data/sample/scan_target.pcd", "data/sample/aligned_output.pcd")
