import numpy as np
import open3d as o3d

def create_circle(radius=5, num_points=1000):
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.zeros_like(x)
    return np.vstack((x, y, z)).T

def apply_transform(points, R, t):
    return (R @ points.T).T + t

def write_pcd(filename, points):
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(filename, pc)

def main():
    source = create_circle()

    # Apply known transformation
    angle = np.pi / 4
    R = o3d.geometry.get_rotation_matrix_from_axis_angle([0, 0, angle])
    t = np.array([1.0, 0.5, 4.0])
    target = apply_transform(source, R, t)
    # Apply another random transformation
    random_angle = np.deg2rad(45)
    random_R = o3d.geometry.get_rotation_matrix_from_axis_angle([2*random_angle, 3*random_angle, random_angle])
    random_t = np.random.uniform(-2.0, 2.0, size=(3,))
    target = apply_transform(target, random_R, random_t)
    target += np.random.normal(0, 0.4, target.shape)  # Add noise

    os.makedirs("data/sample", exist_ok=True)
    write_pcd("data/sample/scan_source.pcd", source)
    write_pcd("data/sample/scan_target.pcd", target)

if __name__ == "__main__":
    import os
    main()
