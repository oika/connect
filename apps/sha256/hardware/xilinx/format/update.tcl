open_project sha256_format_prj
open_solution "solution1"
#source "./sha256_format_prj/solution1/directives.tcl"
#csim_design -compiler gcc
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
