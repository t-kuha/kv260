# Vitis Embedded Acceleration Platform

## Generate platform

- build HW

```shell
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl
```

- PetaLinux project

```shell
$ export PRJ=petalinux
$ petalinux-config -p ${PRJ} --get-hw-description=hw.xsa

# Make additional configuration if necessary
$ petalinux-config -p ${PRJ} -c u-boot
$ petalinux-config -p ${PRJ} -c kernel
$ petalinux-config -p ${PRJ} -c rootfs

# Start build
$ petalinux-build -p ${PRJ}
```

- platform

```shell
$ vitis -s create_vitis_platform.py
```

- Generate device tree overlay

```shell
$ xsct -nodisp create_dtbo.tcl
```

## Run

```shell
$ sudo xmutil listapps
$ sudo xmutil unloadapp 
$ sudo xmutil loadapp kv260-vadd

$ kv260-vadd /usr/lib/firmware/xilinx/kv260-vadd/kv260-vadd.bin
INFO: Reading /usr/lib/firmware/xilinx/kv260-vadd/kv260-vadd.bin
Loading: '/usr/lib/firmware/xilinx/kv260-vadd/kv260-vadd.bin'
Trying to program device[0]: edge
Device[0]: program successful!
TEST PASSED
```

***

## How to create application (vector addition)

```shell
$ IDE_ZYNQMP_SYSROOT=<path to sysroot> vitis -s create_vadd_app.py
```

## How to create PetaLinux project from scratch

```shell
$ export PRJ=petalinux
$ petalinux-create project -n ${PRJ} --template zynqMP
$ petalinux-config -p ${PRJ} --get-hw-description=hw.xsa

# do some configuration
$ petalinux-config -p ${PRJ} -c kernel
$ petalinux-config -p ${PRJ} -c u-boot
$ petalinux-config -p ${PRJ} -c rootfs

# build project
$ petalinux-build -p ${PRJ}
```
