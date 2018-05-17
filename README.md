# Chiptip Connect
Chiptip Connect is a distributed computation framework for CPU-FPGA heterogeneous environment.
In this README, there are two tutorials.
- [Getting Started with One CPU](#getting-started-with-one-cpu)
- [Getting Started with 1 CPU and 1 FPGA](#getting-started-with-1-cpu-and-1-fpga)

## Getting Started with One CPU

Here, we will walk through the process of running a simple task on your local computer.

### Requirements
* Any computer with the following software installed.
  * Python 3.6.3 or higher
  * [Python PyYAML](https://pypi.python.org/pypi/PyYAML) 3.12 or higher
  * [Python networkx](https://networkx.github.io/) 2.0 or higher


### Clone the repository and set environment variables
```
$ git clone https://github.com/chiptiptech/connect.git
$ export MYSTR_HOME=<connect_dir>/platform/software
$ export PYTHONPATH=$MYSTR_HOME/lib/
```

### Set your JobManager and TaskManager's IP addresses to your local address.

```
$ vim <connect_dir>/platform/software/conf/cluster.yaml  # user your favorite editor to edit
```
On line 5, 11, 17, and 20, change the IP address to '127.0.0.1'.

You can also change the MAC address to your own one, but it has no effect as long as you are using only CPUs.

Save the change and close the file.

### Start JobManager and software TaskManager
```
$ cd <connect_dir>/platform/software/bin
$ ./JobManager
```

Open a new console and type the following.
```
$ cd <connect_dir>/platform/software/bin
$ ./TaskManager sv0
```

### Run app
Open a new console and type the following.
```
$ cd <connect_dir>/platform/software/bin
$ ./Client submit ThreeOpJob.py testjob
$ ./Client prepare testjob
$ ./Client run testjob
```

Open a new console and type the following.
```
$ tail -f /tmp/1.dat
$ tail -f /tmp/2.dat
$ tail -f /tmp/3.dat
```
You will see numbers flowing through the screen.

### Finish the app
```
$ ./Client pause testjob
$ ./Client cancel testjob
```
Check whether no more lines are added to /tmp/1.dat, 2.dat, or 3.dat.

## Getting Started with 1 CPU and 1 FPGA

Here, we will walk through the process of building a simple cluster that consists of one CPU and one FPGA.

### Requirements
* Any computer with a 100M Ethernet port and the following software installed.
  * Python 3.6.3 or higher
  * [Python PyYAML](https://pypi.python.org/pypi/PyYAML) 3.12 or higher
  * [Python networkx](https://networkx.github.io/) 2.0 or higher
  * [Python pySerial](https://pypi.python.org/pypi/pyserial) 3.4 or higher
  * [Xilinx Vivado 2017.4](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/2017-4.html)
* [Arty FPGA board](https://reference.digilentinc.com/reference/programmable-logic/arty/start)
* Ethernet cable connecting the computer and the FPGA board
  * IP address for the ethernet port on the computer should be set to 192.168.1.30

### Clone the repository and set environment variables
```
$ git clone https://github.com/chiptiptech/connect.git
$ export MYSTR_HOME=<connect_dir>/platform/software
$ export PYTHONPATH=$MYSTR_HOME/lib/
```

### Set your computer's MAC address in the shell
Change the MAC address (`tx_eth_dst_addr`) on line 74 in file
```
<connect_dir>/platform/hardware/xilinx/modules/axis_network_interface/axis_network_interface.cpp
```
to your computer's MAC address.

### ARP FPGA's MAC address
Associate the IP address and the MAC address of the FPGA.
```
$ sudo arp -i <eth interface on your computer> -s 192.168.1.10 10:00:5e:00:fa:ce
```

### Build FPGA shell
```
$ cd <connect_dir>/platform
$ ./build.sh all
```

### Integrate app logic to shell
We take the 'echo' app for example here. This app sends nubers from the computer and the FPGA just echoes them back.
```
$ cd <connect_dir>/apps/echo
$ ./build.sh
```

### Write bit stream to FPGA
```
$ cd ./hardware/xilinx
$ vivado -mode tcl -source program.tcl
```

### Set FPGA's MAC address
```
$ python3
```
In Python3's interactive shell,
```
>>> import serial
>>> import struct
>>> ser = serial.Serial('/dev/ttyUSB1', 115200) # ttyUSB1 might be ttyUSB2 or something else
>>> mac = struct.pack('<BBBBBB', 0x10, 0x00, 0x5e, 0x00, 0xfa, 0xce)
>>> ser.write(mac)
```

### Start JobManager and software TaskManager
```
$ cd <connect_dir>/platform/software/bin
$ ./JobManager
```

Open a new console and type the following.
```
$ cd <connect_dir>/platform/software/bin
$ ./TaskManager sv0
```

### Run app
Open a new console and type the following.
```
$ cd <connect_dir>/platform/software/bin
$ ./Client submit FPGAJob.py testjob
$ ./Client prepare testjob
$ ./Client run testjob
```

Open a new console and type the following.
```
$ tail -f /tmp/fpga.out
```
You will see the numbers echoed back from the FPGA in the console. To finish, type ^C in the TaskManager console.
