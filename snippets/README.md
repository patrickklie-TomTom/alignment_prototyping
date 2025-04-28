# Mini Factor Graph Example (GTSAM + Python)

This is a minimal working example of building and optimizing a simple factor graph using [GTSAM](https://gtsam.org/) in Python.

The graph includes:
- 2 robot poses (`x1`, `x2`)
- 1 landmark (`l1`)
- An odometry constraint between the poses
- A landmark observation from the first pose
- A prior factor to anchor the graph and make it solvable

The goal is to demonstrate how to set up variables, add factors, initialize guesses, and optimize the graph.

---

## 📦 Requirements

You can create the Conda environment from the provided file:

```bash
conda env create -f ../alignment_prototyping.yml
conda activate alignment_prototyping

