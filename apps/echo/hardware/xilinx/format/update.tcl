open_project echo_format_prj
open_solution "solution1"
#source "./echo_format_prj/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
