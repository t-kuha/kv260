#
# set dpu as default app
#

do_install:append () {
    sed -i 's/default_firmware/dpu/' ${D}${sysconfdir}/dfx-mgrd/daemon.conf
}
