# Vitis Platform for Vitis AI

***

## Generate platform

- build HW

```shell
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl
```

- build PetaLinux

```shell
$ export PRJ=petalinux
$ petalinux-config -p ${PRJ}

# Make additional configuration if necessary
$ petalinux-config -p ${PRJ} -c u-boot
$ petalinux-config -p ${PRJ} -c kernel
$ petalinux-config -p ${PRJ} -c rootfs

# Start build
$ petalinux-config -p ${PRJ} --get-hw-description=hw.xsa
```

- create platform

```shell
$ xsct -nodisp create_pfm.tcl
```

## Generate device tree overlay

```shell
$ xsct -nodisp create_dtbo.tcl
$ bootgen -w -arch zynqmp -process_bitstream bin -image src/bootgen.bif
```
