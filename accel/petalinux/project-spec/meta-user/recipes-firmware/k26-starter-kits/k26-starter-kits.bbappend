FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI += " \
    file://binary_container_1.xclbin \
    file://pl.dtbo \
    file://shell.json \
    file://vadd \
    file://vadd_host \
"

do_install:append () {
    rm -r ${D}${sysconfdir}/dfx-mgrd/${PN} ${D}${libdir}/firmware/xilinx/${PN}

    # add vadd
    install -d ${D}${sysconfdir}/dfx-mgrd
    install -m 0644 ${WORKDIR}/vadd ${D}${sysconfdir}/dfx-mgrd/kv260-vadd
    install -d ${D}${libdir}/firmware/xilinx/kv260-vadd
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/vadd_host ${D}${bindir}/kv260-vadd
    install -m 0644 ${WORKDIR}/binary_container_1.xclbin ${D}${libdir}/firmware/xilinx/kv260-vadd/kv260-vadd.bin
    install -m 0644 ${WORKDIR}/shell.json ${D}${libdir}/firmware/xilinx/kv260-vadd/shell.json
    install -m 0644 ${WORKDIR}/pl.dtbo ${D}${libdir}/firmware/xilinx/kv260-vadd/kv260-vadd.dtbo
}

FILES:${PN} = " \
    ${sysconfdir}/dfx-mgrd/kv260-vadd \
    ${bindir}/kv260-vadd \
    ${libdir}/firmware/xilinx/kv260-vadd/kv260-vadd.dtbo \
    ${libdir}/firmware/xilinx/kv260-vadd/shell.json \
    ${libdir}/firmware/xilinx/kv260-vadd/kv260-vadd.bin \
"

INSANE_SKIP:${PN} = "file-rdeps"
