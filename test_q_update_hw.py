import cocotb
from cocotb.triggers import Timer

def from_fixed(val):
    if val & 0x80000000:
        val -= 0x100000000
    return val / float(1 << 16)

@cocotb.test()
async def test_q_update_hw(dut):
    with open("input_buffer.txt", "r") as f:
        lines = f.readlines()

    results = []
    for line in lines:
        q_old, reward, max_q, alpha, gamma = map(int, line.strip().split())

        dut.q_old.value = q_old
        dut.reward.value = reward
        dut.max_q_next.value = max_q
        dut.alpha.value = alpha
        dut.gamma.value = gamma

        await Timer(1, units="ns")
        results.append(from_fixed(dut.q_new.value.integer))

    with open("output_buffer.txt", "w") as f:
        for val in results:
            f.write(f"{val:.6f}\n")

