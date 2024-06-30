# Vitis Platform for Vitis AI

***

## Generate platform

- build HW

```shell-session
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl
```

- PetaLinux project

```shell-session
$ export PRJ=petalinux
$ petalinux-config -p ${PRJ}

# Make additional configuration if necessary
$ petalinux-config -p ${PRJ} -c u-boot
$ petalinux-config -p ${PRJ} -c kernel
$ petalinux-config -p ${PRJ} -c rootfs

# Start build
$ petalinux-build -p ${PRJ}
```

- platform

```shell-session
$ vitis -s create_vitis_platform.py
```

### Generate device tree overlay

```shell-session
$ xsct -nodisp create_dtbo.tcl
```

## Create application (vector addition)

```shell-session
$ IDE_ZYNQMP_SYSROOT=<path to sysroot> vitis -s create_vadd_app.py
```

***

## How to create PetaLinux project from scratch

```shell-session
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
