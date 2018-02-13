#-----------------------------------------------------------
# Vivado v2017.4 (64-bit)
# SW Build 2086221 on Fri Dec 15 20:54:30 MST 2017
# IP Build 2085800 on Fri Dec 15 22:25:07 MST 2017
# Start of session at: Fri Jan 12 12:33:29 2018
# Process ID: 20044
# Current directory: /home/efukuda/Projects/connect/xilinx/shell
# Command line: vivado
# Log file: /home/efukuda/Projects/connect/xilinx/shell/vivado.log
# Journal file: /home/efukuda/Projects/connect/xilinx/shell/vivado.jou
#-----------------------------------------------------------
create_project shell_prj /home/efukuda/Projects/connect/xilinx/shell/shell_prj -part xc7a35ticsg324-1L
set_property board_part digilentinc.com:arty:part0:1.1 [current_project]
add_files -fileset constrs_1 -norecurse /home/efukuda/Projects/connect/xilinx/resources/boards/arty_a7/eth_ref_clk.xdc
import_files -fileset constrs_1 /home/efukuda/Projects/connect/xilinx/resources/boards/arty_a7/eth_ref_clk.xdc
create_bd_design "shell_design"
update_compile_order -fileset sources_1
set_property  ip_repo_paths  {/home/efukuda/Projects/connect/xilinx/modules/axis_network_interface/axis_network_interface_prj/solution1/impl/ip /home/efukuda/Projects/connect/xilinx/modules/axis_timer/axis_timer_prj/solution1/impl/ip /home/efukuda/Projects/connect/xilinx/modules/data_router/data_router_prj/solution1/impl/ip /home/efukuda/Projects/connect/xilinx/modules/task_manager/task_manager_prj/solution1/impl/ip} [current_project]
update_ip_catalog
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:clk_wiz:5.4 clk_wiz_0
apply_board_connection -board_interface "sys_clock" -ip_intf "clk_wiz_0/clock_CLK_IN1" -diagram "shell_design" 
endgroup
startgroup
set_property -dict [list CONFIG.CLKOUT2_USED {true} CONFIG.CLKOUT2_REQUESTED_OUT_FREQ {25.000} CONFIG.RESET_TYPE {ACTIVE_LOW} CONFIG.MMCM_DIVCLK_DIVIDE {1} CONFIG.MMCM_CLKOUT1_DIVIDE {40} CONFIG.NUM_OUT_CLKS {2} CONFIG.RESET_PORT {resetn} CONFIG.CLKOUT2_JITTER {175.402} CONFIG.CLKOUT2_PHASE_ERROR {98.575}] [get_bd_cells clk_wiz_0]
endgroup
apply_bd_automation -rule xilinx.com:bd_rule:board -config {Board_Interface "reset ( System Reset ) " }  [get_bd_pins clk_wiz_0/resetn]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axi_ethernetlite:3.0 axi_ethernetlite_0
apply_board_connection -board_interface "eth_mii" -ip_intf "axi_ethernetlite_0/MII" -diagram "shell_design" 
endgroup
startgroup
set_property -dict [list CONFIG.C_RX_PING_PONG {0} CONFIG.C_TX_PING_PONG {0} CONFIG.C_INCLUDE_MDIO {0} CONFIG.C_S_AXI_PROTOCOL {AXI4} CONFIG.MDIO_BOARD_INTERFACE {Custom}] [get_bd_cells axi_ethernetlite_0]
endgroup
startgroup
create_bd_cell -type ip -vlnv xilinx.com:hls:axis_network_interface:1.0 axis_network_interface_0
endgroup
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/axis_network_interface_0/m_axi_base_V" intc_ip "Auto" Clk_xbar "Auto" Clk_master "Auto" Clk_slave "Auto" }  [get_bd_intf_pins axi_ethernetlite_0/S_AXI]
apply_bd_automation -rule xilinx.com:bd_rule:board -config {Board_Interface "reset ( System Reset ) " }  [get_bd_pins rst_clk_wiz_0_100M/ext_reset_in]
include_bd_addr_seg [get_bd_addr_segs -excluded axis_network_interface_0/Data_m_axi_base_V/SEG_axi_ethernetlite_0_Reg]
set_property offset 0x00000000 [get_bd_addr_segs {axis_network_interface_0/Data_m_axi_base_V/SEG_axi_ethernetlite_0_Reg}]
set_property range 8K [get_bd_addr_segs {axis_network_interface_0/Data_m_axi_base_V/SEG_axi_ethernetlite_0_Reg}]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:hls:data_router:1.0 data_router_0
endgroup
startgroup
create_bd_cell -type ip -vlnv xilinx.com:hls:task_manager:1.0 task_manager_0
endgroup
startgroup
create_bd_cell -type ip -vlnv xilinx.com:hls:axis_timer:1.0 axis_timer_0
endgroup
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_0
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_network_interface_0/rx_data] [get_bd_intf_pins axis_register_slice_0/S_AXIS]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_0/M_AXIS] [get_bd_intf_pins data_router_0/rxDataIn]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_1
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_network_interface_0/rx_meta_V] [get_bd_intf_pins axis_register_slice_1/S_AXIS]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_1/M_AXIS] [get_bd_intf_pins data_router_0/rxMetadataIn_V]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_2
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_network_interface_0/port_open_reply_V_V] [get_bd_intf_pins axis_register_slice_2/S_AXIS]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_2/M_AXIS] [get_bd_intf_pins task_manager_0/portReplyIn_V]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_3
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_network_interface_0/tx_data] [get_bd_intf_pins axis_register_slice_3/M_AXIS]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_3/S_AXIS] [get_bd_intf_pins data_router_0/txDataOut]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_4
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_network_interface_0/tx_meta_V] [get_bd_intf_pins axis_register_slice_4/M_AXIS]
connect_bd_intf_net [get_bd_intf_pins data_router_0/txMetadataOut_V] [get_bd_intf_pins axis_register_slice_4/S_AXIS]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_5
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_network_interface_0/tx_length_V_V] [get_bd_intf_pins axis_register_slice_5/M_AXIS]
connect_bd_intf_net [get_bd_intf_pins data_router_0/txLengthOut_V_V] [get_bd_intf_pins axis_register_slice_5/S_AXIS]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_6
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_network_interface_0/port_open_request_V_V] [get_bd_intf_pins axis_register_slice_6/M_AXIS]
connect_bd_intf_net [get_bd_intf_pins task_manager_0/portRequestOut_V_V] [get_bd_intf_pins axis_register_slice_6/S_AXIS]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_7
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_timer_0/intr_stream_V_V] [get_bd_intf_pins axis_register_slice_7/S_AXIS]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_7/M_AXIS] [get_bd_intf_pins axis_network_interface_0/cycle_cnt_intr_V_V]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_8
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_8/M_AXIS] [get_bd_intf_pins data_router_0/commandReplyIn_V]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_8/S_AXIS] [get_bd_intf_pins task_manager_0/commandReplyOut_V]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_9
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_9/M_AXIS] [get_bd_intf_pins task_manager_0/commandIn_V_V]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_9/S_AXIS] [get_bd_intf_pins data_router_0/commandOut_V_V]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_10
endgroup
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_10/M_AXIS] [get_bd_intf_pins task_manager_0/portsIn_V]
connect_bd_intf_net [get_bd_intf_pins axis_register_slice_10/S_AXIS] [get_bd_intf_pins data_router_0/portsOut_V]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_rx
endgroup
connect_bd_intf_net [get_bd_intf_pins data_router_0/rxDataOut] [get_bd_intf_pins axis_register_slice_rx/S_AXIS]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_tx
endgroup
connect_bd_intf_net [get_bd_intf_pins data_router_0/txDataIn] [get_bd_intf_pins axis_register_slice_tx/M_AXIS]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_command
endgroup
connect_bd_intf_net [get_bd_intf_pins task_manager_0/logicCommandOut_V_V] [get_bd_intf_pins axis_register_slice_command/S_AXIS]
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_register_slice:1.1 axis_register_slice_state
endgroup
connect_bd_intf_net [get_bd_intf_pins task_manager_0/logicStateIn_V_V] [get_bd_intf_pins axis_register_slice_state/M_AXIS]
startgroup
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/clk_wiz_0/clk_out1 (100 MHz)" }  [get_bd_pins data_router_0/ap_clk]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/clk_wiz_0/clk_out1 (100 MHz)" }  [get_bd_pins task_manager_0/ap_clk]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/clk_wiz_0/clk_out1 (100 MHz)" }  [get_bd_pins axis_timer_0/ap_clk]
endgroup
create_bd_port -dir O -type clk eth_ref_clk
connect_bd_net [get_bd_ports eth_ref_clk] [get_bd_pins clk_wiz_0/clk_out2]
make_wrapper -files [get_files /home/efukuda/Projects/connect/xilinx/shell/shell_prj/shell_prj.srcs/sources_1/bd/shell_design/shell_design.bd] -top
add_files -norecurse /home/efukuda/Projects/connect/xilinx/shell/shell_prj/shell_prj.srcs/sources_1/bd/shell_design/hdl/shell_design_wrapper.v
regenerate_bd_layout
save_bd_design
exit
