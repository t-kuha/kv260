# Vitis Platform for Vitis AI

***

## Generate platform

```shell-session
$ vivado -notrace -nojournal -mode batch -source create_xsa.tcl
```

### Generate device tree overlay

```shell-session
$ xsct -nodisp create_dtbo.tcl
$ bootgen -w -arch zynqmp -process_bitstream bin -image src/bootgen.bif
```
