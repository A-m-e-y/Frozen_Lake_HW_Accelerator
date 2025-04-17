import cocotb
from cocotb.triggers import RisingEdge, Timer
import struct
import random

def float_to_hex(f):
    return struct.unpack('<I', struct.pack('<f', f))[0]

def hex_to_float(h):
    return struct.unpack('<f', struct.pack('<I', h))[0]

@cocotb.test()
async def test_q_update_fp(dut):
    dut._log.info("Starting test...")

    # Provide inputs
    old_value = 0.5
    reward = 1.0
    next_max = 0.7
    learning_rate = 0.2
    discount_factor = 0.95

    dut.old_value.value = float_to_hex(old_value)
    dut.reward.value = float_to_hex(reward)
    dut.next_max.value = float_to_hex(next_max)
    dut.learning_rate.value = float_to_hex(learning_rate)
    dut.discount_factor.value = float_to_hex(discount_factor)
    dut.start.value = 1
    dut.rst.value = 0

    await RisingEdge(dut.clk)
    dut.start.value = 0

    for _ in range(100):  # wait for pipeline latency
        await RisingEdge(dut.clk)
        if dut.done.value:
            break

    result = hex_to_float(dut.new_value.value.integer)
    expected = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * next_max)
    dut._log.info(f"Hardware result: {result}")
    dut._log.info(f"Expected result: {expected}")
    assert abs(result - expected) < 1e-4
