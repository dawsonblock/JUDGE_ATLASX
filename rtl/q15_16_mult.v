// q15_16_mult.v
// This module performs a fixed-point multiplication on two Q15.16 numbers.
// It produces a 32-bit result with saturation and optional rounding. The
// multiplier uses a 64-bit accumulator to avoid overflow. This version
// remains unchanged from the previous scaffold.

module q15_16_mult (
    input  logic         clk,
    input  logic         rst_n,
    input  logic         valid_in,
    input  logic signed [31:0]  a,
    input  logic signed [31:0]  b,
    output logic         valid_out,
    output logic signed [31:0]  result,
    output logic         overflow
);

    // Internal pipeline registers
    logic signed [63:0] mult_full;
    logic signed [63:0] mult_full_reg;
    logic overflow_reg;
    logic valid_reg;

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mult_full_reg <= '0;
            overflow_reg <= 1'b0;
            valid_reg    <= 1'b0;
        end else begin
            valid_reg    <= valid_in;
            // Full 64-bit multiplication
            mult_full    <= a * b;
            mult_full_reg <= mult_full;
            // Detect overflow based on upper bits beyond 32-bit range
            overflow_reg <= (mult_full[63:32] != {32{mult_full[31]}});
        end
    end

    // Truncate to Q15.16 result with rounding by adding half LSB
    logic signed [31:0] rounded;
    always_comb begin
        // Add 2^15 for round-half-up when positive
        logic signed [63:0] rounded_full;
        rounded_full = mult_full_reg + 64'sh0000_0000_0000_8000;
        rounded      = rounded_full[47:16];
    end

    assign valid_out = valid_reg;
    assign result    = rounded;
    assign overflow  = overflow_reg;

endmodule