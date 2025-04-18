TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/q_update_q16_16.v
TOPLEVEL = q_update_q16_16
MODULE = test_q_update_hw
SIM = verilator

include $(shell cocotb-config --makefiles)/Makefile.sim
