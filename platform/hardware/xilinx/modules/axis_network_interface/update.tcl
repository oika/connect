############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2017 Xilinx, Inc. All Rights Reserved.
############################################################
open_project axis_network_interface_prj
#uset_top axis_network_interface
#uadd_files axis_network_interface.cpp -cflags "-I../../resources/hls_include"
#uadd_files -tb axis_network_interface_tb.cpp
open_solution "solution1"
#uset_part {xc7a35ticsg324-1l} -tool vivado
#ucreate_clock -period 10 -name default
#source "./axis_network_interface_prj/solution1/directives.tcl"
#csim_design -compiler gcc
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
