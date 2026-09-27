# Quick bring-up

- Uses `kv260_base` platform installed along with Vitis to skip platform creation process entirely.

## Board set-up

- BOOT firmware: v1.07
  - [Kria SOM Boot Firmware Update](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/3020685316/Kria+SOM+Boot+Firmware+Update)
- SD card image: Kria generic Starter Kit embedded Linux 2026.1
  - [Kria SOMs & Starter Kits](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/1641152513/Kria+SOMs+Starter+Kits)

## Get sysroot

- [Zynq MP common image](https://www.amd.com/en/support/downloads/adaptive-socs-and-fpgas/development-tools/2026-1.html#gd-group-0-heading)

```shell
$ tar xf xilinx-zynqmp-common-v2026.1_06092129.tar.gz ~/vitis
```

## Acceleration app

```shell
$ IDE_ZYNQMP_SYSROOT=~/vitis/sysroots/cortexa72-cortexa53-amd-linux/ vitis -s create_vadd_app.py
```

## Running the app

- Collect necessary files:

```shell
$ cp ${XILINX_VITIS}/base_platforms/kv260_base/sw/boot/pl.dtbo release/
$ cp _ws/vadd/build/hw/hw_link/vadd.xclbin release/
$ cp _ws/vadd_host/build/hw/vadd_host release/
$ cp _ws/vadd/build/hw/hw_link/vadd/vadd/int/system.bit release/
```

- Copy `release` folder via SSH or USB thumb drive

```shell
# copy data
$ cd ./release
$ sudo mkdir -p /lib/firmware/xilinx/vadd
$ sudo cp shell.json /lib/firmware/xilinx/vadd/
$ sudo cp pl.dtbo /lib/firmware/xilinx/vadd/vadd.dtbo
$ sudo cp vadd.xclbin /lib/firmware/xilinx/vadd/
$ sudo cp system.bit /lib/firmware/xilinx/vadd/vadd.bit

$ sudo xmutil unloadapp 
$ sudo xmutil listapps 
$ sudo xmutil loadapp vadd
# outputs something like:
# ID accelType   Base        slotLoc Accelerator
# -- ----------- ----------- ------- -----------
# ...
# 12 XRT_FLAT    vadd        0       vadd

# run
$ ./vadd_host -x vadd.xclbin
# outputs:
# Open the device0
# Load the xclbin vadd.xclbin
# Allocate Buffer in Global Memory
# synchronize input buffer data to device global memory
# Execution of the kernel
# Get the output data from the device
# TEST PASSED
```