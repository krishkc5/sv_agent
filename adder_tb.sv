module tb;
    logic [4:0] a;
    logic [4:0] b;
    logic [4:0] y;

    adder dut (.a(a), .b(b), .y(y));

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, tb);

        // Test 1: Normal case
        a = 5'd3;  b = 5'd4;  #1;
        if (y !== 5'd11) $fatal("FAIL: 3 + 2*4 != %0d", y);

        // Test 2: Saturation
        a = 5'd20; b = 5'd10; #1;
        if (y !== 5'd31) $fatal("FAIL: Saturation failed, y=%0d", y);

        // Test 3: Edge
        a = 5'd31; b = 5'd0; #1;
        if (y !== 5'd31) $fatal("FAIL: Edge case failed");

        $display("✅ ALL TESTS PASSED");
        $finish;
    end
endmodule
