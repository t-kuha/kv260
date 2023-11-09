# Building Vitis Application Acceleration Platform for Ubuntu

***

## Generate platform

```shell-session
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl
$ xsct -nodisp -sdx create_pfm.tcl
```

### Generate device tree overlay

```shell-session
$ xsct -nodisp create_dtbo.tcl
$ bootgen -w -arch zynqmp -process_bitstream bin -image src/bootgen.bif
```

***

## How to enable fan control

```shell-session
$ sudo systemctl enable fancontrol.service
$ sudo systemctl start fancontrol.service
```
