import ray
import open3d as o3d
import numpy as np
import time

# Initialize Ray for local execution
ray.init()

# Larger and slower point cloud generator
def generate_point_cloud(shift=0, n_points=5000000):
    pc = o3d.geometry.PointCloud()
    points = np.random.rand(n_points, 3)
    points[:, 0] += shift
    pc.points = o3d.utility.Vector3dVector(points)
    return pc

# Ray task: align two clouds using ICP and sleep a bit
@ray.remote
def align_point_clouds(source_np, target_np, task_id):
    start = time.time()

    source_np = np.array(source_np, copy=True)
    target_np = np.array(target_np, copy=True)

    source = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(source_np))
    target = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(target_np))

    threshold = 0.1
    reg = o3d.pipelines.registration.registration_icp(
    source, target, threshold, np.eye(4),
    o3d.pipelines.registration.TransformationEstimationPointToPoint(),
    o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=100)
    )
    print(f"Task {task_id} finished in {reg.iteration_count} iterations")

    duration = time.time() - start
    print(f"Task {task_id} done in {duration:.2f}s")
    return reg.transformation

# Generate a large batch of point cloud pairs
n_tasks = 500
cloud_pairs = [
    (generate_point_cloud(i, n_points=50000).points, generate_point_cloud(i + 0.05, n_points=50000).points)
    for i in range(n_tasks)
]

# Launch tasks in parallel
futures = [
    align_point_clouds.remote(np.asarray(src), np.asarray(tgt), task_id=i)
    for i, (src, tgt) in enumerate(cloud_pairs)
]

# Wait for all to complete
results = ray.get(futures)

# Optional: summarize
print(f"\nCompleted {n_tasks} point cloud registrations.")

