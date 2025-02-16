# Vitis AI on KV260

- tool version:
    - Vitis: 2023.2
    - Vitis AI: v3.5.0

***

## Build HW & platform

```shell
# HW
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl

# Vitis platform
$ vitis -s create_vitis_platform.py
```

## Generate bitstream

```shell
$ tar xf DPUCZDX8G.tar.gz
$ cp src/dpu_conf.vh DPUCZDX8G/prj/Vitis/dpu_conf.vh
$ cp src/prj_config DPUCZDX8G/prj/Vitis/config_file/prj_config
$ export SDX_PLATFORM=$(pwd)/_pfm/kv260_vai/export/kv260_vai/kv260_vai.xpfm
$ pushd DPUCZDX8G/prj/Vitis
$ make all KERNEL=DPU DEVICE=kv260
$ popd

# get fingerprint value info
$ cp DPUCZDX8G/prj/Vitis/binary_container_1/link/vivado/vpl/prj/prj.gen/sources_1/bd/kv260/ip/kv260_DPUCZDX8G_1_0/arch.json .
```

- copy necessary files into PetaLinux project

```shell
$ bootgen -w -arch zynqmp -process_bitstream bin -image src/bootgen.bif -o dpu.bin
$ cp src/shell.json dpu.dtbo petalinux/project-spec/meta-user/recipes-firmware/kv260-dpu/files
$ cp DPUCZDX8G/prj/Vitis/binary_container_1/binary_container_1.xclbin \
petalinux/project-spec/meta-user/recipes-firmware/kv260-dpu/files/dpu.xclbin
$ cp DPUCZDX8G/prj/Vitis/binary_container_1/link/vivado/vpl/prj/prj.runs/impl_1/kv260_wrapper.bit.bin \
petalinux/project-spec/meta-user/recipes-firmware/kv260-dpu/files/dpu.bin
```

## Build PetaLinux project

```shell
# PetaLinux project
$ petalinux-config -p ${PRJ} --get-hw-description=hw.xsa
$ petalinux-build -p ${PRJ}
```

## Prepare SD card

- boot partition: copy the following files into boot paritition
  - ``boot.scr``
  - ``Image``
  - ``ramdisk.cpio.gz.u-boot``

- rootfs partition: use the command below to copy the rootfs contents

```shell
# rootfs
$ sudo tar xf petalinux/images/linux/rootfs.tar.gz -C <path to rootfs partition>
```

## Run

- install Python environment

```shell
$ pip3 install torch==2.4.1 torchvision==0.19.1 scipy tqdm
$ pip3 cache purge
```

- edit Vitis AI runtime config (location of ``dpu.xclbin``) if necessary

```shell
$ vi /etc/vart.conf
```
