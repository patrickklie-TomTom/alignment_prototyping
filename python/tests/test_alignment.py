import sys
import subprocess
import os

def run_pure_python():
    from alignment_pure.pdal_pipeline import preprocess_point_cloud
    preprocess_point_cloud("data/sample/lidar.pcd", "data/sample/aligned_python.pcd")

def run_standalone_cpp():
    subprocess.run(["./cpp/build/tools/standalone_aligner", "data/sample/lidar.pcd", "data/sample/aligned_cpp_tool.pcd"])

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_alignment.py [variant]")
        sys.exit(1)

    variant = sys.argv[1]
    if variant == "pure_python":
        run_pure_python()
    elif variant == "standalone_cpp":
        run_standalone_cpp()
    else:
        print(f"Variant '{variant}' is not implemented yet.")
        sys.exit(2)

if __name__ == "__main__":
    main()
