# Generate Platform Quickly

- create Vitis platform without PetaLinux

## Download & extract BSP

- Download ``xilinx-kv260-starterkit-v2023.2-10140544.bsp`` from [AMD Website](https://www.xilinx.com/member/forms/download/xef.html?filename=xilinx-kv260-starterkit-v2023.2-10140544.bsp)

## Generate HW & platform

```shell-session
# HW
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl

# platform
$ tar xf xilinx-kv260-starterkit-v2023.2-10140544.bsp
$ vitis -s create_vitis_platform.py xilinx-kv260-starterkit-2023.2

# device tree
$ xsct -nodisp create_dtbo.tcl
```

## Create application

- copy ``pl.dtbo``, ``src/shell.json``, application binary, and .xclbin into SD card

## Preparation

- install required packages (_internet connection required_)

```shell-session
$ sudo dnf install xrt
```

- create app

```shell-session

```
