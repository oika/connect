############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2017 Xilinx, Inc. All Rights Reserved.
############################################################
open_project task_manager_prj
#set_top task_manager
#add_files task_manager.cpp -cflags "-I../../resources/hls_include/"
#add_files -tb task_manager_tb.cpp -cflags "-I../../resources/hls_include/"
open_solution "solution1"
#set_part {xc7a35ticsg324-1l} -tool vivado
#create_clock -period 10 -name default
#source "./task_manager_prj/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
