############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2017 Xilinx, Inc. All Rights Reserved.
############################################################
open_project mac_uart_prj
#set_top mac_uart
#add_files mac_uart.cpp
open_solution "solution1"
#set_part {xc7a35ticsg324-1l} -tool vivado
#create_clock -period 10 -name default
#source "./mac_uart_prj/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
