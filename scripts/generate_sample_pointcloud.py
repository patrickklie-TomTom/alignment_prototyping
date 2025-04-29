import numpy as np
import open3d as o3d

def generate_lidar_pointcloud():
    pc = o3d.geometry.PointCloud()
    theta = np.linspace(0, 2 * np.pi, 1000)
    x = np.cos(theta) * 10
    y = np.sin(theta) * 10
    z = np.random.uniform(-0.2, 0.2, 1000)
    points = np.vstack((x, y, z)).T
    pc.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud("data/sample/lidar.pcd", pc)

generate_lidar_pointcloud()
