# test_q_update_hw.py
import cocotb

def from_fixed(val):
    if val & 0x80000000:
        val -= 0x100000000
    return val / float(1 << 16)

@cocotb.test()
async def test_q_update_hw(dut):
    with open("input_buffer.txt", "r") as f:
        line = f.readline()
        q_old, reward, max_q_next, alpha, gamma = map(int, line.strip().split())

    dut.q_old.value = q_old
    dut.reward.value = reward
    dut.max_q_next.value = max_q_next
    dut.alpha.value = alpha
    dut.gamma.value = gamma

    await cocotb.triggers.Timer(1, units="ns")  # give combinational logic time to settle

    q_new_fixed = dut.q_new.value.integer
    q_new_float = from_fixed(q_new_fixed)

    with open("output_buffer.txt", "w") as f:
        f.write(f"{q_new_float:.6f}\n")
