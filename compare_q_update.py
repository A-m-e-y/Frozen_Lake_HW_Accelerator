from hw_q_update import hw_batch_q_update
import time
import random

def to_fixed(val): return int(round(val * (1 << 16))) & 0xFFFFFFFF
def from_fixed(val): return val / float(1 << 16)

# Generate 1000 input sets
N = 100000
inputs = []
for _ in range(N):
    q_old = round(random.uniform(0.0, 1.0), 5)
    reward = random.choice([0.0, 1.0])
    max_q = round(random.uniform(0.0, 1.0), 5)
    alpha = round(random.uniform(0.1, 0.9), 5)
    gamma = 0.95  # fixed for all
    inputs.append((q_old, reward, max_q, alpha, gamma))

# SW calculation
start = time.time()
sw_outputs = []
for q_old, reward, max_q, alpha, gamma in inputs:
    new_q = (1 - alpha) * q_old + alpha * (reward + gamma * max_q)
    sw_outputs.append(new_q)
sw_time = (time.time() - start) * 1000

# HW calculation
total_hw_time_start = time.time()
hw_outputs, hw_time = hw_batch_q_update(inputs)
total_hw_time = (time.time() - total_hw_time_start) * 1000

# Compare
epsilon = 0.00003
match = 0
mismatch = 0

for sw, hw in zip(sw_outputs, hw_outputs):
    if abs(sw - hw) < epsilon:
        match += 1
    else:
        mismatch += 1

# Report
print(f"\n✅ Total Inputs: {N}")
print(f"✔️  Matches:     {match}")
print(f"❌ Mismatches:  {mismatch}")
print(f"\n⏱️  Software time: {sw_time:.2f} ms")
print(f"⏱️  Hardware time: {hw_time:.2f} ms\n")
print(f"⏱️  Total Hardware time: {total_hw_time:.2f} ms\n")
