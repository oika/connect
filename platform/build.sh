#!/usr/bin/env bash

if ! [ $# -eq 1 ]; then
    echo "Use \"all\" or \"clean\""
    exit 1
fi

if [ $1 = "all" ]; then
    cd ./hardware/xilinx/modules
    if [ -e build.log ]; then
        mv build.log build.bak.log
    fi
    
    files="./*"
    for modulepath in $files; do
        cd $modulepath
        if [ -e "${modulepath}_prj" ]; then
            cd ..
            continue
        fi
        vivado_hls -f build.tcl 2>&1 | tee -a ../../../../build.log
        if ! [ "${PIPESTATUS[0]}" -eq 0 ]; then
            echo "ERROR: Build for $modulepath failed. Exiting..."
            rm -rf ${modulepath}_prj
            exit 1
        fi
        cd ..
    done
    
    cd ../stream_shell
    vivado -mode tcl -source build.tcl 2>&1 | tee -a ../../../build.log
    if ! [ "${PIPESTATUS[0]}" -eq 0 ]; then
        echo "ERROR: build for stream_shell failed. Exiting..."
        rm -rf stream_shell_prj
        exit 1
    fi
elif [ $1 = "clean" ]; then
    if [ -e build.log ]; then
        rm build.log
    fi
    cd ./hardware/xilinx/modules
    files="./*"
    for modulepath in $files; do
        cd $modulepath
        if [ -e "${modulepath}_prj" ]; then
            rm -rf ${modulepath}_prj
        fi
        if [ -e "*.log" ]; then
            rm vivado_hls.log
        fi
        cd ..
    done

    cd ../stream_shell
    rm -rf stream_shell_prj
    if [ -e "*.log" ]; then
        rm *.log
    fi
    if [ -e "*.jou" ]; then
        rm *.jou
    fi
    if [ -e "*.bak" ]; then
        rm *.bak
    fi
fi
