open_project ../../../../platform/hardware/xilinx/stream_shell/stream_shell_prj/stream_shell_prj.xpr
update_compile_order -fileset sources_1
open_bd_design {../../../../platform/hardware/xilinx/stream_shell/stream_shell_prj/stream_shell_prj.srcs/sources_1/bd/design_1/design_1.bd}
delete_bd_objs [get_bd_intf_nets axis_register_slice_format2logic_M_AXIS] [get_bd_intf_nets sha256_0_resultOut_V_V] [get_bd_intf_nets axis_register_slice_prepare_start_M_AXIS] [get_bd_intf_nets sha256_0_prepare_done_V_V] [get_bd_cells sha256_0]
delete_bd_objs [get_bd_intf_nets axis_register_slice_rx_M_AXIS] [get_bd_intf_nets sha256_format_0_rxEventOut_V_V] [get_bd_intf_nets sha256_format_0_txDataOut_V] [get_bd_intf_nets axis_register_slice_logic2format_M_AXIS] [get_bd_cells sha256_format_0]
disconnect_bd_net /clk_wiz_0_clk_out1 [get_bd_pins axis_register_slice_logic2format/aclk]
disconnect_bd_net /rst_clk_wiz_0_100M_interconnect_aresetn [get_bd_pins axis_register_slice_logic2format/aresetn]
disconnect_bd_net /clk_wiz_0_clk_out1 [get_bd_pins axis_register_slice_format2logic/aclk]
disconnect_bd_net /rst_clk_wiz_0_100M_interconnect_aresetn [get_bd_pins axis_register_slice_format2logic/aresetn]
save_bd_design
exit
