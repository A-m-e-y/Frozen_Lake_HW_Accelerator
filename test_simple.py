import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_simple(dut):
    dut.a.value = 1
    await Timer(1, units="ns")
    assert dut.b.value == 1