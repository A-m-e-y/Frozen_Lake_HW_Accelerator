// q_update_fp_top.sv
// Floating-point Q-value update using FPnew FPU blocks

// `include "/mnt/d/PSU/HW_For_AI_teuscher/cvfpu/src/fpnew_pkg.sv"

module q_update_fp_top (
    input  logic         clk,
    input  logic         rst,
    input  logic         start,

    input  logic [31:0]  old_value,
    input  logic [31:0]  reward,
    input  logic [31:0]  next_max,
    input  logic [31:0]  learning_rate,
    input  logic [31:0]  discount_factor,

    output logic [31:0]  new_value,
    output logic         done
);

    import fpnew_pkg::*;

    // Configuration parameters
    localparam Features_t Features = '{
        FpFmtMask: FP32,
        EnableFMA: 1'b0,
        EnableAddSub: 1'b1,
        EnableMul: 1'b1,
        EnableDivSqrt: 1'b0,
        EnableCompare: 1'b0,
        EnableMinMax: 1'b0,
        EnableConversions: 1'b0,
        EnableClassify: 1'b0
    };

    localparam Implementation_t Implementation = DEFAULT;
    typedef logic [0:0] TagType;

    // Signals for intermediate values
    logic [31:0] mul1_result, add1_result, sub1_result, mul2_result, mul3_result;
    logic [31:0] final_result;

    logic valid_in, valid_out1, valid_out2, valid_out3, valid_out4, valid_out5, final_valid;
    assign valid_in = start;

    // Stage 1: gamma * next_max
    fpnew_top #(
        .Features(Features),
        .Implementation(Implementation),
        .TagType(TagType)
    ) mul1 (
        .clk_i(clk),
        .rst_ni(~rst),
        .operands_i({discount_factor, next_max}),
        .op_i(OP_MUL),
        .op_mod_i('0),
        .src_fmt_i(FP32),
        .dst_fmt_i(FP32),
        .int_fmt_i(0),
        .vectorial_op_i(1'b0),
        .simd_mask_i(1'b1),
        .tag_i('0),
        .in_valid_i(valid_in),
        .in_ready_o(),
        .flush_i(1'b0),
        .result_o(mul1_result),
        .status_o(),
        .tag_o(),
        .out_valid_o(valid_out1),
        .out_ready_i(1'b1),
        .busy_o()
    );

    // Stage 2: reward + (gamma * next_max)
    fpnew_top #(
        .Features(Features),
        .Implementation(Implementation),
        .TagType(TagType)
    ) add1 (
        .clk_i(clk),
        .rst_ni(~rst),
        .operands_i({reward, mul1_result}),
        .op_i(OP_ADD),
        .op_mod_i('0),
        .src_fmt_i(FP32),
        .dst_fmt_i(FP32),
        .int_fmt_i(0),
        .vectorial_op_i(1'b0),
        .simd_mask_i(1'b1),
        .tag_i('0),
        .in_valid_i(valid_out1),
        .in_ready_o(),
        .flush_i(1'b0),
        .result_o(add1_result),
        .status_o(),
        .tag_o(),
        .out_valid_o(valid_out2),
        .out_ready_i(1'b1),
        .busy_o()
    );

    // Stage 3: 1.0 - learning_rate
    fpnew_top #(
        .Features(Features),
        .Implementation(Implementation),
        .TagType(TagType)
    ) sub1 (
        .clk_i(clk),
        .rst_ni(~rst),
        .operands_i({32'h3f800000, learning_rate}),
        .op_i(OP_SUB),
        .op_mod_i('0),
        .src_fmt_i(FP32),
        .dst_fmt_i(FP32),
        .int_fmt_i(0),
        .vectorial_op_i(1'b0),
        .simd_mask_i(1'b1),
        .tag_i('0),
        .in_valid_i(valid_in),
        .in_ready_o(),
        .flush_i(1'b0),
        .result_o(sub1_result),
        .status_o(),
        .tag_o(),
        .out_valid_o(valid_out3),
        .out_ready_i(1'b1),
        .busy_o()
    );

    // Stage 4: (1 - lr) * old_value
    fpnew_top #(
        .Features(Features),
        .Implementation(Implementation),
        .TagType(TagType)
    ) mul2 (
        .clk_i(clk),
        .rst_ni(~rst),
        .operands_i({sub1_result, old_value}),
        .op_i(OP_MUL),
        .op_mod_i('0),
        .src_fmt_i(FP32),
        .dst_fmt_i(FP32),
        .int_fmt_i(0),
        .vectorial_op_i(1'b0),
        .simd_mask_i(1'b1),
        .tag_i('0),
        .in_valid_i(valid_out3),
        .in_ready_o(),
        .flush_i(1'b0),
        .result_o(mul2_result),
        .status_o(),
        .tag_o(),
        .out_valid_o(valid_out4),
        .out_ready_i(1'b1),
        .busy_o()
    );

    // Stage 5: learning_rate * (reward + gamma * next_max)
    fpnew_top #(
        .Features(Features),
        .Implementation(Implementation),
        .TagType(TagType)
    ) mul3 (
        .clk_i(clk),
        .rst_ni(~rst),
        .operands_i({learning_rate, add1_result}),
        .op_i(OP_MUL),
        .op_mod_i('0),
        .src_fmt_i(FP32),
        .dst_fmt_i(FP32),
        .int_fmt_i(0),
        .vectorial_op_i(1'b0),
        .simd_mask_i(1'b1),
        .tag_i('0),
        .in_valid_i(valid_out2),
        .in_ready_o(),
        .flush_i(1'b0),
        .result_o(mul3_result),
        .status_o(),
        .tag_o(),
        .out_valid_o(valid_out5),
        .out_ready_i(1'b1),
        .busy_o()
    );

    // Final Stage: mul2_result + mul3_result
    fpnew_top #(
        .Features(Features),
        .Implementation(Implementation),
        .TagType(TagType)
    ) add2 (
        .clk_i(clk),
        .rst_ni(~rst),
        .operands_i({mul2_result, mul3_result}),
        .op_i(OP_ADD),
        .op_mod_i('0),
        .src_fmt_i(FP32),
        .dst_fmt_i(FP32),
        .int_fmt_i(0),
        .vectorial_op_i(1'b0),
        .simd_mask_i(1'b1),
        .tag_i('0),
        .in_valid_i(valid_out4 & valid_out5),
        .in_ready_o(),
        .flush_i(1'b0),
        .result_o(final_result),
        .status_o(),
        .tag_o(),
        .out_valid_o(final_valid),
        .out_ready_i(1'b1),
        .busy_o()
    );

    assign new_value = final_result;
    assign done = final_valid;

endmodule
