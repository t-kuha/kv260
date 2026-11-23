# Vitis Embedded Acceleration Platform

## Generate platform

- build HW

```shell
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl
```

- Build AMD EDF Linux from `hw.xsa` ([details](edf/README.md)):

```shell
$ cd edf
$ ./build.sh
$ cd ..
```

The EDF image uses a separate PL overlay for application hardware. The Vitis
platform script reads `edf/images`, stages the EDF firmware in `_boot` with the
filenames expected by Vitis, and stages `boot.scr`, `Image`, and `system.dtb` in
`_sd_dir`. Build EDF before running the platform script.

Write the EDF `edf-linux-disk-image-kria-*.wic.xz` image to the microSD card as
described in [the EDF instructions](edf/README.md). Its boot script loads the
kernel from `/boot/Image` on root partition 3; copying `_sd_dir` to a blank card
does not provide that partition or the root filesystem. EDF does not use the
PetaLinux ramdisk.

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
