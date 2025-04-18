from hw_q_update import hw_q_update
import time

# Q16.16 scaling helpers
def to_fixed(val):
    return int(round(val * (1 << 16))) & 0xFFFFFFFF

def from_fixed(val):
    if val & 0x80000000:
        val -= 0x100000000
    return val / float(1 << 16)

# Example input values (Q-learning params)
q_old       = 0.45
reward      = 1.0
max_q_next  = 0.9
alpha       = 0.3
gamma       = 0.95

# Software calculation
start = time.time()
term1 = (1 - alpha) * q_old
term2 = alpha * (reward + gamma * max_q_next)
q_new_sw = term1 + term2
sw_time = (time.time() - start) * 1000

# Fixed-point conversion
q_old_fx      = to_fixed(q_old)
reward_fx     = to_fixed(reward)
max_q_next_fx = to_fixed(max_q_next)
alpha_fx      = to_fixed(alpha)
gamma_fx      = to_fixed(gamma)

# Hardware call
total_hw_start = time.time()
q_new_hw, hw_time = hw_q_update(q_old_fx, reward_fx, max_q_next_fx, alpha_fx, gamma_fx)
total_hw_time = (time.time() - total_hw_start) * 1000

# Print results
print("\n📊 Q-learning Update Formula Test (Q16.16)\n")
print(f"Q_old       = {q_old}")
print(f"Reward      = {reward}")
print(f"Max Q_next  = {max_q_next}")
print(f"Alpha       = {alpha}")
print(f"Gamma       = {gamma}\n")

print(f"SW Result   = {q_new_sw:.6f} (time: {sw_time:.3f} ms)")
print(f"HW Result   = {q_new_hw:.6f} (time: {hw_time:.3f} ms)")
print(f"Total HW Runtime   = {total_hw_time:.3f} ms")

epsilon = 3 / (1 << 16)
if abs(q_new_sw - q_new_hw) < epsilon:
    print("\n✅ Result matches within Q16.16 precision.\n")
else:
    print("\n❌ Result mismatch!\n")
