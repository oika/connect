#!/usr/bin/env bash

shell_prj="../../platform/hardware/xilinx/stream_shell/stream_shell_prj"

if ! [ -e $shell_prj ]; then
    echo "ERROR: Build the shell first. Exiting..."
    exit 1
fi

if [ -e build.log ]; then
    rm build.log
    touch build.log
fi

cd hardware/xilinx/logic
if ! [ -e echo_prj ]; then
    vivado_hls -f build.tcl 2>&1 | tee -a build.log
    if ! [ "${PIPESTATUS[0]}" -eq 0 ]; then
        echo "ERROR: build for echo failed. Exiting..."
        rm -rf echo_prj
        exit 1
    fi
fi
cd ..

cd format
if ! [ -e echo_format_prj ]; then
    vivado_hls -f build.tcl 2>&1 | tee -a build.log
    if ! [ "${PIPESTATUS[0]}" -eq 0 ]; then
        echo "ERROR: build for echo_format failed. Exiting..."
        rm -rf echo_format_prj
        exit 1
    fi
fi
cd ..

vivado -mode tcl -source ./build.tcl 2>&1 | tee -a build.log
if ! [ "${PIPESTATUS[0]}" -eq 0 ]; then
    echo "ERROR: build for stream_shell failed. Exiting..."
    exit 1
fi

cp ../../$shell_prj/stream_shell_prj.runs/impl_1/design_1_wrapper.bit .

vivado -mode tcl -source ./finalize.tcl 2>&1 | tee -a build.log
if ! [ "${PIPESTATUS[0]}" -eq 0 ]; then
    echo "ERROR: finalization for stream_shell failed. Exiting..."
fi
