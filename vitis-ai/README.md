# Vitis AI on KV260

- tool version:
    - Vitis: 2023.2
    - Vitis AI: v3.5.0

***

## Build platform

```shell
# HW
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl

# PetaLinux project
$ petalinux-config -p ${PRJ} --get-hw-description=hw.xsa
$ petalinux-build -p ${PRJ}

# Vitis platform
$ vitis -s create_vitis_platform.py
```

***

## Create HW

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

## Prepare SD card

- boot partition: copy the following files into boot paritition
  - ``boot.scr``
  - ``Image``
  - ``ramdisk.cpio.gz.u-boot``
  - ``system.dtb``

- rootfs partition: use the command below to copy the rootfs contents

```shell
# rootfs
$ sudo tar xf xilinx-kv260-starterkit-2023.2/pre-built/linux/images/rootfs.tar.gz -C <path to rootfs partition>

# copy bitstream, xclbin, device tree, shell.json
$ export ROOTFS_PART=<path to rootfs partition>
$ bootgen -w -arch zynqmp -process_bitstream bin -image src/bootgen.bif -o dpu.bit.bin
$ cp DPUCZDX8G/prj/Vitis/binary_container_1/binary_container_1.xclbin <path to boot partition>/dpu.xclbin
$ sudo mkdir ${ROOTFS_PART}/lib/firmware/xilinx/dpu
$ sudo cp DPUCZDX8G/prj/Vitis/binary_container_1/link/vivado/vpl/prj/prj.runs/impl_1/kv260_wrapper.bit.bin ${ROOTFS_PART}/lib/firmware/xilinx/dpu/dpu.bit.bin
$ sudo cp dpu.dtbo ${ROOTFS_PART}/lib/firmware/xilinx/dpu/dpu.dtbo
$ sudo cp src/shell.json ${ROOTFS_PART}/lib/firmware/xilinx/dpu/
$ sync
```

## Run

- install required packages

```shell
$ sudo dnf install -y xrt vart vitis-ai-library
```

- install Python environment

```shell
$ pip3 install torch==2.4.1 torchvision==0.19.1 scipy tqdm
$ pip3 cache purge
```

- edit Vitis AI runtime config if necessary

```shell
$ vi /etc/vart.conf
```

- set up

```shell
xilinx-kv260-starterkit-20232:~$ sudo xmutil listapps
Password: 
                   Accelerator      Accel_type                          Base Pid       Base_type  #slots(PL+AIE)     Active_slot
                           dpu        XRT_FLAT                           dpu  ok        XRT_FLAT           (0+0)              -1
              k26-starter-kits        XRT_FLAT              k26-starter-kits  ok        XRT_FLAT           (0+0)              0,
xilinx-kv260-starterkit-20232:~$ sudo xmutil unloadapp
remove from slot 0 returns: 0 (Ok)
xilinx-kv260-starterkit-20232:~$ sudo xmutil loadapp dpu
dpu: loaded to slot 0
```
