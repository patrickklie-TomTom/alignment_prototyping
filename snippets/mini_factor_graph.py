import gtsam
from gtsam import symbol
import numpy as np

# Create an empty factor graph
graph = gtsam.NonlinearFactorGraph()

# Create an initial estimate for the variables
initial_estimate = gtsam.Values()

# Noise models
odometry_noise = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.1, 0.1, 0.05]))  # x, y, theta
measurement_noise = gtsam.noiseModel.Isotropic.Sigma(2, 0.1)  # 2D landmark measurement
prior_noise = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.01, 0.01, 0.01]))  # Prior is very confident

# Symbols for variables
X1 = symbol('x', 1)  # Pose at time 1
X2 = symbol('x', 2)  # Pose at time 2
L1 = symbol('l', 1)  # Landmark 1

# Add a prior on the first pose
graph.add(gtsam.PriorFactorPose2(X1, gtsam.Pose2(0.0, 0.0, 0.0), prior_noise))

# Add odometry factor between X1 and X2
odometry = gtsam.Pose2(2.0, 0.0, 0.0)  # moved 2 meters forward
graph.add(gtsam.BetweenFactorPose2(X1, X2, odometry, odometry_noise))

# Add landmark observation factor from X1
bearing = np.arctan2(1.0, 1.0)  # bearing to (1,1)
range_measurement = np.sqrt(2.0)  # distance to (1,1)
graph.add(gtsam.BearingRangeFactor2D(X1, L1, gtsam.Rot2(bearing), range_measurement, measurement_noise))

# Initial guesses (noisy)
initial_estimate.insert(X1, gtsam.Pose2(0.0, 0.0, 0.0))
initial_estimate.insert(X2, gtsam.Pose2(2.1, 0.1, 0.05))
initial_estimate.insert(L1, gtsam.Point2(1.1, 1.0))

# Optimize
optimizer = gtsam.GaussNewtonOptimizer(graph, initial_estimate)
result = optimizer.optimize()

# Print results
print("Pose 1:", result.atPose2(X1))
print("Pose 2:", result.atPose2(X2))
print("Landmark 1:", result.atPoint2(L1))

