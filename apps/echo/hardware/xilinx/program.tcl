open_project ../../../../platform/hardware/xilinx/stream_shell/stream_shell_prj/stream_shell_prj.xpr
update_compile_order -fileset sources_1
open_hw
connect_hw_server
open_hw_target
set_property PROGRAM.FILE {../../../../platform/hardware/xilinx/stream_shell/stream_shell_prj/stream_shell_prj.runs/impl_1/design_1_wrapper.bit} [get_hw_devices xc7a35t_0]
current_hw_device [get_hw_devices xc7a35t_0]
refresh_hw_device -update_hw_probes false [lindex [get_hw_devices xc7a35t_0] 0]
set_property PROBES.FILE {} [get_hw_devices xc7a35t_0]
set_property FULL_PROBES.FILE {} [get_hw_devices xc7a35t_0]
set_property PROGRAM.FILE {../../../../platform/hardware/xilinx/stream_shell/stream_shell_prj/stream_shell_prj.runs/impl_1/design_1_wrapper.bit} [get_hw_devices xc7a35t_0]
program_hw_devices [get_hw_devices xc7a35t_0]
refresh_hw_device [lindex [get_hw_devices xc7a35t_0] 0]
exit
