module top(
    input clk,
    input rst,
    dti.consumer top_din1, // u1 (1)
    dti.consumer top_din2, // u2 (2)
    dti.producer dout0, // u2 (2)
    dti.producer dout1 // u2 (2)

);

      dti #(.W_DATA(2)) fgear0_if_s(); // u2 (2)
      dti #(.W_DATA(2)) fgear0_if_s_bc[1:0](); // u2 (2)
    bc #(
                .SIZE(2)
    )
     bc_fgear0 (
        .clk(clk),
        .rst(rst),
        .din(fgear0_if_s),
        .dout(fgear0_if_s_bc)
    );

    connect connect_fgear0_if_s_0 (
        .clk(clk),
        .rst(rst),
        .din(fgear0_if_s_bc[0]),
        .dout(dout0)
    );


      dti #(.W_DATA(2)) top_din2_bc[1:0](); // u2 (2)
    bc #(
                .SIZE(2)
    )
     bc_top_din2 (
        .clk(clk),
        .rst(rst),
        .din(top_din2),
        .dout(top_din2_bc)
    );


    fgear0 fgear0_i (
        .clk(clk),
        .rst(rst),
        .arg1(top_din1),
        .arg2(top_din2_bc[0]),
        .ret(fgear0_if_s)
    );


    fgear1 fgear1_i (
        .clk(clk),
        .rst(rst),
        .arg1(fgear0_if_s_bc[1]),
        .arg2(top_din2_bc[1]),
        .ret(dout1)
    );



endmodule