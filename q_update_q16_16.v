// q_update_q16_16.v
// Single-cycle Q-learning update module using Q16.16 fixed-point arithmetic

module q_update_q16_16 (
    input  wire [31:0] q_old,        // Q(s,a)
    input  wire [31:0] reward,       // r
    input  wire [31:0] max_q_next,   // max Q(s')
    input  wire [31:0] alpha,        // learning rate
    input  wire [31:0] gamma,        // discount factor
    output wire [31:0] q_new         // New Q(s,a)
);

    // Intermediate wires for each step
    wire [63:0] gamma_mul_max;
    wire [31:0] gamma_max_scaled;

    wire [31:0] reward_plus_gamma;

    wire [63:0] alpha_mul_sum;
    wire [31:0] weighted_sum;

    wire [31:0] one_minus_alpha;
    wire [63:0] scaled_q_old;
    wire [31:0] weighted_q_old;

    wire [31:0] q_new_internal;

    // Step 1: gamma * max_q_next
    assign gamma_mul_max = gamma * max_q_next;
    assign gamma_max_scaled = gamma_mul_max[47:16];  // Q16.16 -> shift by 16

    // Step 2: reward + (gamma * max_q_next)
    assign reward_plus_gamma = reward + gamma_max_scaled;

    // Step 3: alpha * (reward + gamma * max_q_next)
    assign alpha_mul_sum = alpha * reward_plus_gamma;
    assign weighted_sum = alpha_mul_sum[47:16];

    // Step 4: (1 - alpha)
    assign one_minus_alpha = 32'h00010000 - alpha;  // 1.0 in Q16.16 = 0x00010000

    // Step 5: (1 - alpha) * q_old
    assign scaled_q_old = one_minus_alpha * q_old;
    assign weighted_q_old = scaled_q_old[47:16];

    // Step 6: final result
    assign q_new_internal = weighted_q_old + weighted_sum;

    assign q_new = q_new_internal;

endmodule
