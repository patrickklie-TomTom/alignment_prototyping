import subprocess
import time

variants = ["pure_python", "method_level", "class_level", "framework_level", "pure_cpp", "standalone_cpp"]
results = {}

for variant in variants:
    start = time.time()
    subprocess.run(["python", f"python/tests/test_alignment.py", variant])
    elapsed = time.time() - start
    results[variant] = elapsed

with open('benchmarks/results.md', 'w') as f:
    for k, v in results.items():
        f.write(f"{k}: {v:.2f} seconds\n")
