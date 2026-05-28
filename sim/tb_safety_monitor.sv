`timescale 1ns/1ps

module tb_safety_monitor;
    localparam int ADC_WIDTH = 16;

    logic                         clk;
    logic                         rst_n;
    logic signed [ADC_WIDTH-1:0]  adc_in;
    logic [ADC_WIDTH-1:0]         kill_threshold;
    logic                         clear_faults;
    logic                         safety_kill;
    logic                         fault_latched;

    int errors;

    safety_monitor #(
        .ADC_WIDTH(ADC_WIDTH)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .adc_in(adc_in),
        .kill_threshold(kill_threshold),
        .clear_faults(clear_faults),
        .safety_kill(safety_kill),
        .fault_latched(fault_latched)
    );

    initial begin
        clk = 1'b0;
        forever #5 clk = ~clk;
    end

    task automatic drive_and_expect(
        input logic signed [ADC_WIDTH-1:0] sample,
        input logic expected_latched,
        input string label
    );
        begin
            adc_in = sample;
            @(posedge clk);
            #1;
            if (fault_latched !== expected_latched) begin
                errors = errors + 1;
                $display(
                    "TB_ERROR %s sample=%0d expected_latched=%0b got=%0b",
                    label,
                    sample,
                    expected_latched,
                    fault_latched
                );
            end
        end
    endtask

    initial begin
        errors = 0;
        rst_n = 1'b0;
        adc_in = '0;
        clear_faults = 1'b0;
        kill_threshold = 16'd100;

        repeat (2) @(posedge clk);
        rst_n = 1'b1;

        drive_and_expect(16'sd0, 1'b0, "zero");
        drive_and_expect(16'sd1, 1'b0, "plus_one");
        drive_and_expect(-16'sd1, 1'b0, "minus_one");
        drive_and_expect(16'sd100, 1'b0, "plus_threshold");
        drive_and_expect(-16'sd100, 1'b0, "minus_threshold");

        drive_and_expect(16'sd101, 1'b1, "plus_threshold_plus_one");
        drive_and_expect(16'sd0, 1'b1, "sticky_after_positive_trip");

        clear_faults = 1'b1;
        @(posedge clk);
        #1;
        clear_faults = 1'b0;
        if (fault_latched !== 1'b0) begin
            errors = errors + 1;
            $display("TB_ERROR clear_faults_did_not_clear");
        end

        drive_and_expect(-16'sd101, 1'b1, "minus_threshold_plus_one");

        clear_faults = 1'b1;
        @(posedge clk);
        #1;
        clear_faults = 1'b0;
        drive_and_expect(-16'sh8000, 1'b1, "most_negative_value");

        if (safety_kill !== fault_latched) begin
            errors = errors + 1;
            $display("TB_ERROR safety_kill_mismatch");
        end

        if (errors == 0) begin
            $display("TB_PASS tb_safety_monitor");
            $finish(0);
        end else begin
            $display("TB_FAIL tb_safety_monitor errors=%0d", errors);
            $finish(1);
        end
    end
endmodule
