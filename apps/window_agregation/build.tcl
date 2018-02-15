############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2017 Xilinx, Inc. All Rights Reserved.
############################################################
open_project window_aggregation_prj
set_top window_aggregation
add_files window_aggregation.cpp -cflags "-I../../resources/hls_include/"
add_files -tb window_aggregation_tb.cpp -cflags "-I../../resources/hls_include/"
open_solution "solution1"
set_part {xc7a35ticsg324-1l} -tool vivado
create_clock -period 10 -name default
#source "./window_aggregation_prj/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
