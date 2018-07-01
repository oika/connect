open_hw
connect_hw_server
open_hw_target localhost:3121/xilinx_tcf/Digilent/$serial_id
set_property PROGRAM.FILE ./$bitfile [get_hw_devices xc7a35t_0]
current_hw_device [get_hw_devices xc7a35t_0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xc7a35t_0] 0]
set_property PROBES.FILE {} [get_hw_devices xc7a35t_0]
set_property FULL_PROBES.FILE {} [get_hw_devices xc7a35t_0]
set_property PROGRAM.FILE ./$bitfile [get_hw_devices xc7a35t_0]
program_hw_devices [get_hw_devices xc7a35t_0]
refresh_hw_device [lindex [get_hw_devices xc7a35t_0] 0]
close_hw_target localhost:3121/xilinx_tcf/Digilent/$serial_id
exit
