# Generate Platform Quickly

- create Vitis platform without PetaLinux

## Download & extract BSP

- Download ``xilinx-kv260-starterkit-v2024.1-05230256.bsp`` from [AMD Website](https://www.xilinx.com/member/forms/download/xef.html?filename=xilinx-kv260-starterkit-v2024.1-05230256.bsp)

## Generate HW & platform

```shell-session
# HW
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl

# platform
$ tar xf xilinx-kv260-starterkit-v2024.1-05230256.bsp
$ vitis -s create_vitis_platform.py xilinx-kv260-starterkit-2024.1

# device tree
$ xsct -nodisp create_dtbo.tcl
```

## Create application (vector addition)


## Prepare SD card

- copy the following files from ``xilinx-kv260-starterkit-2024.1``
  - boot.scr
  - Image
  - ramdisk.cpio.gz.u-boot
  - system-zynqmp-sck-kv-g-revB.dtb
  - system.dtb

- copy ``pl.dtbo``, ``src/shell.json``, and .xclbin into SD card
- copy the application binary into home directory of SD card (``/home/petalinux``)

## Run the app

```shell-session
# install required packages (internet connection required)
$ sudo dnf install xrt

# run
$ sudo xmutil unloadapp k26-starter-kits
$ sudo xmutil loadapp vadd
$ ./vadd_host binary_container_1.xclbin
```

- result:

```shell-session
INFO: Reading binary_container_1.xclbin
Loading: 'binary_container_1.xclbin'
Trying to program device[0]: edge
Device[0]: program successful!
TEST PASSED
```
