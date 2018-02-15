############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2017 Xilinx, Inc. All Rights Reserved.
############################################################
open_project echo_format_prj
set_top echo_format
add_files echo_format.cpp -cflags "-I../../../../../platform/hardware/xilinx/resources/hls_include/"
add_files -tb echo_format_tb.cpp -cflags "-I../../resources/hls_include/"
open_solution "solution1"
set_part {xc7a35ticsg324-1l} -tool vivado
create_clock -period 10 -name default
#source "./echo_format_prj/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
