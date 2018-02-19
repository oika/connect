open_project window_aggregation_prj
open_solution "solution1"
#source "./window_aggregation_prj/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
exit
