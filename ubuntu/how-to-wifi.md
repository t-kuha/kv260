# How to add support for TL-WN725N

## Prerequisite

- [Ubuntu (22.04) image](https://ubuntu.com/download/amd-xilinx)
- connection to internet (maybe via wired LAN)

## Build Kernel module & install firmware

```shell-session
# build
$ git clone https://github.com/ivanovborislav/rtl8188eu.git
$ sudo make install ARCH=arm64 -j4

# copy firmware
$ wget https://github.com/lwfinger/rtl8188eu/raw/master/rtl8188eufw.bin
$ sudo mkdir /lib/firmware/rtlwifi/
$ sudo cp rtl8188eufw.bin /lib/firmware/rtlwifi/
```

## Set up network info

- Edit ``/etc/netplan/50-cloud-init.yaml`` as follows:

```yaml
network:
    renderer: NetworkManager
    version: 2

    wifis:
        wlx5ca6e6364187:
            optional: true
            access-points:
                <SSID>:
                    password: <password>
            dhcp4: true
```

- Apply change & then reboot the board

```shell-session
$ sudo netplan apply
$ sudo reboot
```
