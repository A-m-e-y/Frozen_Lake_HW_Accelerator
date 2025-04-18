# Frozen Lake Q-Learning Accelerator Project

## Purpose of the Project

The purpose of this project is to accelerate the Q-learning algorithm, a fundamental reinforcement learning technique, by leveraging hardware-based computation. Specifically, the project implements the Q-value update formula in hardware using Verilog, enabling faster computation compared to software-based implementations. This is particularly useful for large-scale reinforcement learning problems or real-time applications where computational efficiency is critical.

The project includes:
1. A Python-based Q-learning implementation for the Frozen Lake environment.
2. A hardware implementation of the Q-value update formula in Verilog.
3. A comparison framework to validate and benchmark the hardware implementation against the software implementation.

---
## How the Flow Works

The flow of the project starts with the Python script `compare_q_update.py` and ends with the Verilog module `q_update_q16_16.v`. Here’s how the files interact with each other:

1. **`compare_q_update.py`**:
   - This is the entry point of the project. It generates random inputs for the Q-value update formula and computes the results using both software and hardware implementations.
   - For the hardware implementation, it calls the `hw_batch_q_update` function from `hw_q_update.py`.

2. **`hw_q_update.py`**:
   - This file acts as the interface between Python and the Verilog hardware. It:
     - Converts the inputs to fixed-point representation.
     - Writes the inputs to `input_buffer.txt`.
     - Invokes the Verilog simulation using the `make` command.
     - Reads the results from `output_buffer.txt` and converts them back to floating-point representation.

3. **`q_update_q16_16.v`**:
   - This Verilog module implements the Q-value update formula using fixed-point arithmetic.
   - It reads the inputs from `input_buffer.txt`, computes the updated Q-values, and writes the results to `output_buffer.txt`.

4. **Back to `compare_q_update.py`**:
   - The script reads the hardware results from `hw_q_update.py`, compares them with the software results, and reports the number of matches, mismatches, and the time taken by both implementations.

### Visualization of the Flow

```plaintext
+-----------------------+
| compare_q_update.py   |
| (Entry Point)         |
+-----------------------+
           |
           v
+-----------------------+
| hw_q_update.py        |
| (Hardware Interface)  |
+-----------------------+
           |
           v
+-----------------------+
|       Write           |
|  input_buffer.txt     |
| (Input for Verilog)   |
+-----------------------+
           |
           v
+-----------------------+
| test_q_update_hw.py   |
| (cocotb TestBench)    |
+-----------------------+
           |
           v
+-----------------------+
| q_update_q16_16.v     |
| (Verilog Module)      |
+-----------------------+
           |
           v
+-----------------------+
| test_q_update_hw.py   |
|  cocotb writes the    |
| output_buffer.txt     |
| (Output from Verilog) |
+-----------------------+
           |
           v
+-----------------------+
| hw_q_update.py        |
| (Result Conversion)   |
+-----------------------+
           |
           v
+-----------------------+
| compare_q_update.py   |
| (Comparison & Report) |
+-----------------------+
```

---
## How to Run `compare_q_update.py`

### Prerequisites
1. Python 3.x installed on your system.
2. Required Python libraries: `cocotb`, `gymnasium`.
3. A working Verilog simulation environment (e.g., Verilator, VCS) for hardware execution.
4. Ensure the `hw_q_update.py` file is correctly configured to invoke the Verilog simulation.

### Steps to Run
1. Open a terminal in the project directory.
2. Run the `compare_q_update.py` script:
   ```bash
   python3 compare_q_update.py
   ```

### Understanding the Printed Results
After running the script, you will see output similar to the following:

```
✅ Total Inputs: 100000
✔️   Matches:     87989
❌ Mismatches:  12011

⏱️   Software time: 66.39 ms
⏱️   Hardware time: 15210.13 ms

⏱️   Total Hardware time: 15922.73 ms
```

- **Total Inputs**: The total number of Q-value update computations performed.
- **Matches**: The number of computations where the hardware and software results match within a specified precision (`epsilon`).
- **Mismatches**: The number of computations where the hardware and software results differ beyond the allowed precision.
- **Software Time**: The total time taken by the software implementation to compute all Q-value updates.
- **Hardware Time**: The time taken by the hardware implementation for the Q-value updates (excluding setup/initialization).
- **Total Hardware Time**: The total time taken by the hardware implementation, including setup and execution.

---

## How `compare_q_update.py` Works

### Overview
The `compare_q_update.py` script benchmarks the Q-value update formula in both software and hardware. It generates a large number of random inputs (User configurable by changing value of `N`), computes the Q-value updates using both implementations, and compares the results.

### Steps in the Script
1. **Input Generation**:
   - Generates `N` random input sets for the Q-value update formula.
   - Each input set includes:
     - `q_old`: The old Q-value.
     - `reward`: The reward received.
     - `max_q`: The maximum Q-value of the next state.
     - `alpha`: The learning rate.
     - `gamma`: The discount factor.

2. **Software Calculation**:
   - Computes the Q-value updates using the formula:
     ```
     new_q = (1 - alpha) * q_old + alpha * (reward + gamma * max_q)
     ```
   - Measures the total time taken for the software computation.

3. **Hardware Calculation**:
   - Converts the inputs to fixed-point representation using the `to_fixed` function.
   - Passes the inputs to the hardware implementation via the `hw_batch_q_update` function in `hw_q_update.py`.
   - Measures the total time taken for the hardware computation.

4. **Comparison**:
   - Compares the results from the software and hardware implementations.
   - Counts the number of matches and mismatches within a specified precision (`epsilon`).

5. **Reporting**:
   - Prints the total inputs, matches, mismatches, and the time taken by both implementations.

---

## Hardware Implementation (Verilog)

### Overview
The hardware implementation of the Q-value update formula is written in Verilog. It performs the following computation:
```
new_q = (1 - alpha) * q_old + alpha * (reward + gamma * max_q)
```

### q_update_q16_16.v
The `q_update_q16_16.v` file contains the Verilog implementation of the Q-value update formula. It is designed to compute the updated Q-value (`new_q`) using fixed-point arithmetic with 16-bit precision for both integer and fractional parts (Q16.16 format). This ensures efficient hardware implementation while maintaining numerical accuracy.

#### Key Features:
- **Inputs**: 
  - `q_old`: The previous Q-value.
  - `reward`: The immediate reward.
  - `max_q`: The maximum Q-value from the next state.
  - `alpha`: The learning rate.
  - `gamma`: The discount factor.
- **Output**:
  - `new_q`: The updated Q-value.
- **Fixed-Point Arithmetic**: The module uses Q16.16 fixed-point representation to handle fractional values efficiently in hardware.
- **Pure Combinational Design**: The implementation may include pipelining to optimize performance and meet timing constraints in hardware.

This module is a critical component of reinforcement learning hardware accelerators, enabling efficient computation of Q-value updates in real-time.

---

## Other Files in the Project

### `Frozen_Lake_Q_Learning.py`
This file implements the Q-learning algorithm for the Frozen Lake environment using the `gymnasium` library. It includes:
- A random map generator for the Frozen Lake environment.
- The Q-value update function (`update_q_value`).
- The training loop (`train_q_learning`).
- Profiling functionality to measure the runtime of the `update_q_value` and `train_q_learning` functions.

### `hw_q_update.py`
This file provides a Python interface to the hardware implementation. It includes:
- The `hw_q_update` function for single Q-value updates.
- The `hw_batch_q_update` function for batch processing of Q-value updates.
- Integration with the Verilog simulation environment.

### `test_q_update_hw.py`
This file contains a testbench for the hardware implementation using the `cocotb` framework. It verifies the correctness of the hardware by comparing its output with the expected results.

### `compare_q_update.py`
This file benchmarks the software and hardware implementations of the Q-value update formula. It generates random inputs, computes the results using both implementations, and compares the outputs.

---

## Conclusion

This project demonstrates the acceleration of Q-learning using hardware. By implementing the Q-value update formula in Verilog, the project achieves significant speedup compared to the software implementation. The provided Python scripts enable easy benchmarking, validation, and integration of the hardware with reinforcement learning algorithms.