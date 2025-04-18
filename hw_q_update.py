import subprocess
import time

def hw_q_update(q_old, reward, max_q_next, alpha, gamma):
    with open("input_buffer.txt", "w") as f:
        f.write(f"{q_old} {reward} {max_q_next} {alpha} {gamma}\n")

    start = time.time()
    subprocess.run(["make"], check=True)
    elapsed = (time.time() - start) * 1000  # in ms

    with open("output_buffer.txt", "r") as f:
        hw_result = float(f.read().strip())

    return hw_result, elapsed
