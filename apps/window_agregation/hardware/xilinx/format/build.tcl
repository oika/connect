open_project window_aggregation_format_prj
set_top window_aggregation_format
add_files window_aggregation_format.cpp -cflags "-I../../../../../platform/hardware/xilinx/resources/hls_include/"
add_files -tb window_aggregation_format_tb.cpp -cflags "-I../../../../../platform/hardware/xilinx/resources/hls_include/"
open_solution "solution1"
set_part {xc7a35ticsg324-1l} -tool vivado
create_clock -period 10 -name default
#source "./window_aggregation_format_prj/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
