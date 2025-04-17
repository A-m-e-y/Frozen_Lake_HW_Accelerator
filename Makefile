TOPLEVEL_LANG = systemverilog
fpnew_dir = ./cvfpu/src

# Point to your top-level SystemVerilog module
VERILOG_SOURCES = \
  q_update_fp_top.sv \
  $(fpnew_dir)/fpnew_top.sv \
  $(fpnew_dir)/fpnew_pkg.sv \
  $(fpnew_dir)/fpnew_opgroup_block.sv \
  $(fpnew_dir)/common_cells/src/stream_register.sv \
  $(fpnew_dir)/common_cells/src/fifo_v3.sv \
  $(fpnew_dir)/common_cells/src/prim_fifo_sync.sv

TOPLEVEL = q_update_fp_top
MODULE = test_q_update_fp  # your cocotb test filename without .py
SIM = verilator
WAVES = 1
VERILATOR_FLAGS += --sv

include $(shell cocotb-config --makefiles)/Makefile.sim

debug:
	@echo "Debugging Makefile..."
	@echo "fpnew_dir: $(fpnew_dir)"
	@echo "VERILOG_SOURCES: $(VERILOG_SOURCES)"
	@echo "TOPLEVEL: $(TOPLEVEL)"
	@echo "MODULE: $(MODULE)"
	@echo "SIM: $(SIM)"


# TOPLEVEL_LANG = verilog
# VERILOG_SOURCES = simple.v
# TOPLEVEL = simple
# MODULE = test_simple
# SIM = verilator

# include $(shell cocotb-config --makefiles)/Makefile.sim
