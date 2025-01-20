#
# set kv260-vadd as default app
#

do_install:append () {
    sed -i 's/default_firmware/kv260-vadd/' ${D}${sysconfdir}/dfx-mgrd/daemon.conf
}
