# Vitis AI on KV260

- tool version:
    - Vitis: 2023.2
    - Vitis AI: v3.5.0

***

## Create HW

```shell
$ tar xf DPUCZDX8G.tar.gz 
$ cp src/dpu_conf.vh DPUCZDX8G/prj/Vitis/dpu_conf.vh 
$ cp src/prj_config DPUCZDX8G/prj/Vitis/config_file/prj_config
$ export SDX_PLATFORM=$(pwd)/_pfm/kv260/export/kv260/kv260.xpfm
$ pushd DPUCZDX8G/prj/Vitis
$ make all KERNEL=DPU DEVICE=kv260
$ popd
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

# device tree, xclbin, shell.json
$ sudo mkdir <path to rootfs partition>/lib/firmware/xilinx/dpu
$ sudo cp pl.dtbo <path to rootfs partition>/lib/firmware/xilinx/dpu/dpu.dtbo
$ sudo cp src/shell.json <path to rootfs partition>/lib/firmware/xilinx/dpu/
$ sudo cp DPUCZDX8G/prj/Vitis/binary_container_1/binary_container_1.xclbin <path to rootfs partition>s/lib/firmware/xilinx/dpu/dpu.bit.bin
$ sync
```

## Run

- install required packages

```shell
$ sudo dnf install -y xrt vart vitis-ai-library
```

- install Python environment

```shell
$ pip3 install torch==2.4.1 torchvision==0.19.1 scipy
$ pip3 cache purge
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
