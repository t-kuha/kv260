# Generate Platform Quickly

- create Vitis platform without PetaLinux

## Download sysroot

- Download SDK from [AMD Website](https://www.xilinx.com/member/forms/download/xef.html?filename=xilinx-zynqmp-common-v2024.1_05230256.tar.gz) & install sysroot

## Download & extract BSP

- Download ``xilinx-kv260-starterkit-v2024.1-05230256.bsp`` from [AMD Website](https://www.xilinx.com/member/forms/download/xef.html?filename=xilinx-kv260-starterkit-v2024.1-05230256.bsp)

## Generate HW & platform

```shell
# HW
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl

# platform
$ tar xf xilinx-kv260-starterkit-v2024.1-05230256.bsp
$ vitis -s create_vitis_platform.py xilinx-kv260-starterkit-2024.1

# device tree overlay
$ xsct -nodisp create_dtbo.tcl
```

## Create application (vector addition)

```shell
$ IDE_ZYNQMP_SYSROOT=<path to sysroot> vitis -s create_vadd_app.py
```

## Prepare SD card

- copy the the following files in  of ``quick/xilinx-kv260-starterkit-2024.1/pre-built/linux/images`` into boot partition:
  - ``Image``
  - ``boot.scr``
  - ``system-zynqmp-sck-kv-g-revB.dtb``
  - ``system.dtb``
  - ``ramdisk.cpio.gz.u-boot``
- extract ``quick/xilinx-kv260-starterkit-2024.1/pre-built/linux/images/rootfs.tar.gz`` into rootfs partition
- copy the application binary &.xclbin into home directory of SD card (``/home/petalinux``)
  ```shell
  $ cp _vitis-ws/vadd_host/build/hw/vadd_host <rootfs mount point>/home/petalinux/
  $ cp _vitis-ws/vadd/build/hw/hw_link/binary_container_1.xclbin <rootfs mount point>/home/petalinux/
  ```
- copy ``pl.dtbo``, ``src/shell.json``, and .xclbin into SD card as follows:
  ```shell
  $ sudo mkdir <rootfs mount point>/lib/firmware/xilinx/vadd
  $ sudo cp pl.dtbo <rootfs mount point>/lib/firmware/xilinx/vadd/vadd.dtbo
  $ sudo cp src/shell.json <rootfs mount point>/lib/firmware/xilinx/vadd/
  $ sudo cp _vitis-ws/vadd/build/hw/hw_link/binary_container_1.xclbin <rootfs mount point>/lib/firmware/xilinx/vadd/vadd.bin

  $ sync
  ```

## Run the app

- boot the board & run the following commands:

```shell
# install required packages (internet connection required)
$ sudo dnf install xrt

# run
$ sudo xmutil unloadapp k26-starter-kits
$ sudo xmutil loadapp vadd
$ ./vadd_host binary_container_1.xclbin
```

- result:

```shell
INFO: Reading binary_container_1.xclbin
Loading: 'binary_container_1.xclbin'
Trying to program device[0]: edge
Device[0]: program successful!
TEST PASSED
```
