import subprocess

def run_cpp_tool():
    subprocess.run(["./cpp/build/tools/standalone_aligner", "data/sample/lidar.pcd", "data/sample/aligned_output.pcd"])

if __name__ == '__main__':
    run_cpp_tool()
