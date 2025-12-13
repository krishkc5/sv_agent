module adder (
    input  logic [4:0] a,
    input  logic [4:0] b,
    output logic [4:0] y
);
    logic [5:0] sum;

    always_comb begin
        sum = a + (b << 1);   // y = a + 2*b

        if (sum > 6'd31)
            y = 5'd31;       // Saturate
        else
            y = sum[4:0];   // Truncate safely
    end
endmodule
