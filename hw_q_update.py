import subprocess
import time

def to_fixed(val): return int(round(val * (1 << 16))) & 0xFFFFFFFF
def from_fixed(val):
    if val & 0x80000000:
        val -= 0x100000000
    return val / float(1 << 16)

def hw_batch_q_update(batch_inputs):
    with open("input_buffer.txt", "w") as f:
        for q_old, reward, max_q, alpha, gamma in batch_inputs:
            f.write(f"{to_fixed(q_old)} {to_fixed(reward)} {to_fixed(max_q)} {to_fixed(alpha)} {to_fixed(gamma)}\n")

    start = time.time()
    subprocess.run(["make"], check=True)
    elapsed = (time.time() - start) * 1000

    outputs = []
    with open("output_buffer.txt", "r") as f:
        for line in f:
            outputs.append(float(line.strip()))

    return outputs, elapsed
